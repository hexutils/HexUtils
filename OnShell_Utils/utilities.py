import abc
import collections
import contextlib
import cPickle
import datetime
import errno
import getpass
import glob
import inspect
import itertools
import logging
import math
import operator
import json
import os
import pipes
import pprint
import re
import shutil
import subprocess
import sys
import tempfile
import time

from functools import wraps
from itertools import tee, izip

import ROOT

class KeyDefaultDict(collections.defaultdict):
    """
    http://stackoverflow.com/a/2912455
    """
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret

class TFilesDict(KeyDefaultDict):
    def __init__(self):
        return super(TFilesDict, self).__init__(ROOT.TFile.Open)
    def __delitem__(self, key):
        self[key].Close()
        return super(TFilesDict, self).__delitem__(key)
    def clear(self):
        for key in self.keys(): del self[key]
        return super(TFilesDict, self).clear()

tfiles = TFilesDict()

class MultiplyCounter(collections.Counter):
    def __init__(self, *args, **kwargs):
        self.__frozen = False
        super(MultiplyCounter, self).__init__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        if self.__frozen: raise TypeError("MultiplyCounter is already frozen!")
        super(MultiplyCounter, self).__setitem__(*args, **kwargs)

    def __add__(self, other):
        if self.__frozen: raise TypeError("MultiplyCounter is already frozen!")
        return type(self)(super(MultiplyCounter, self).__add__(other))
    def __sub__(self, other):
        if self.__frozen: raise TypeError("MultiplyCounter is already frozen!")
        return type(self)(super(MultiplyCounter, self).__sub__(other))
    def __mul__(self, other):
        if self.__frozen: raise TypeError("MultiplyCounter is already frozen!")
        return type(self)({k: v*other for k, v in self.iteritems()})
    def __rmul__(self, other):
        if self.__frozen: raise TypeError("MultiplyCounter is already frozen!")
        return type(self)({k: other*v for k, v in self.iteritems()})
    def __div__(self, other):
        if self.__frozen: raise TypeError("MultiplyCounter is already frozen!")
        return type(self)({k: v/other for k, v in self.iteritems()})

    def __imul__(self, other):
        if self.__frozen: raise TypeError("MultiplyCounter is already frozen!")
        for key in self:
            self[key] *= other
        return self
    def __idiv__(self, other):
        if self.__frozen: raise TypeError("MultiplyCounter is already frozen!")
        for key in self:
            self[key] /= other
        return self

    def freeze(self):
        self.__frozen = True

def cache(function):
    cache = {}
    @wraps(function)
    def newfunction(*args, **kwargs):
        try:
            return cache[args, tuple(sorted(kwargs.iteritems()))]
        except TypeError:
            print args, tuple(sorted(kwargs.iteritems()))
            raise
        except KeyError:
            cache[args, tuple(sorted(kwargs.iteritems()))] = function(*args, **kwargs)
            return newfunction(*args, **kwargs)
    return newfunction

def cache_keys(*argkeys, **kwargkeys):
    def inner_cache_keys(function):
        cache = {}
        @wraps(function)
        def newfunction(*args, **kwargs):
            argsforcache = tuple(key(arg) for key, arg in itertools.izip_longest(argkeys, args, fillvalue=lambda x: x))
            kwargsforcache = {kw: kwargkeys.get(kw, lambda x: x)(kwargs[kw]) for kw in kwargs}
            keyforcache = argsforcache, tuple(sorted(kwargsforcache.iteritems()))
            try:
                return cache[keyforcache]
            except TypeError:
                pprint.pprint(keyforcache)
                for _ in keyforcache:
                  for _2 in _: print _2, hash(_2)
                raise
            except KeyError:
                cache[keyforcache] = result = function(*args, **kwargs)
                return result
        return newfunction
    return inner_cache_keys

def cacheall(function):
    cache = []
    @wraps(function)
    def newfunction(*args, **kwargs):
        cache.append(function(*args, **kwargs))
        return cache[-1]
    return newfunction

def cache_instancemethod(function):
    """
    This one can't take arguments.
    But the cache clears when self is deleted (as opposed to the cache keeping self alive).
    Probably could be modified to take arguments without too much trouble.
    """
    @wraps(function)
    def newfunction(self):
        if not hasattr(self, "__cache_instancemethod_{}".format(function.__name__)):
            setattr(self, "__cache_instancemethod_{}".format(function.__name__), function(self))
        return getattr(self, "__cache_instancemethod_{}".format(function.__name__))

def cache_file(filename, *argkeys, **kwargkeys):
    def inner_cache_file(function):
        try:
            with OneAtATime(filename+".tmp", 5), open(filename, "rb") as f:
                cache = cPickle.load(f)
        except IOError:
            cache = {}
        @wraps(function)
        def newfunction(*args, **kwargs):
            argsforcache = tuple(key(arg) for key, arg in itertools.izip_longest(argkeys, args, fillvalue=lambda x: x))
            kwargsforcache = {kw: kwargkeys.get(kw, lambda x: x)(kwargs[kw]) for kw in kwargs}
            keyforcache = argsforcache, tuple(sorted(kwargsforcache.iteritems()))
            try:
                return cache[keyforcache]
            except TypeError:
                print keyforcache
                raise
            except KeyError:
                result = function(*args, **kwargs)
                with OneAtATime(filename+".tmp", 5):
                    try:
                        with open(filename, "rb") as f:
                            cache.update(cPickle.load(f))
                    except IOError:
                        pass
                    cache[keyforcache] = result
                    with open(filename, "wb") as f:
                        cPickle.dump(cache, f)
                return newfunction(*args, **kwargs)
        return newfunction
    return inner_cache_file

def multienumcache(function, haskwargs=False, multienumforkey=None):
    from enums import MultiEnum
    if multienumforkey is None:
        multienumforkey = function
    assert issubclass(function, MultiEnum)
    assert issubclass(multienumforkey, MultiEnum)
    cache = {}
    def newfunction(*args, **kwargs):
        if kwargs and not haskwargs:
            raise TypeError("{} has no kwargs!".format(function.__name__))
        key = multienumforkey(*args)
        try:
            oldkwargs, result = cache[key]
            if kwargs and kwargs != oldkwargs:
                raise ValueError("{}({}, **kwargs) called with 2 different kwargs:\n{}\n{}".format(function.__name__, ", ".join(repr(_) for _ in args), oldkwargs, kwargs))
            return result
        except KeyError:
            if haskwargs and not kwargs:
                raise ValueError("Have to give kwargs the first time you call {}({}, **kwargs)".format(function.__name__, ", ".join(repr(_) for _ in args)))
            cache[key] = kwargs, function(*args, **kwargs)
            return newfunction(*args, **kwargs)
    newfunction.__name__ = function.__name__
    return newfunction


def cache_instancemethod(function):
    """
    for when self doesn't support __hash__
    """
    cachename = "__cache_{}".format(function.__name__)
    def newfunction(self, *args, **kwargs):
        try:
            return getattr(self, cachename)[args, tuple(sorted(kwargs.iteritems()))]
        except AttributeError:
            setattr(self, cachename, {})
            return newfunction(self, *args, **kwargs)
        except KeyError:
            getattr(self, cachename)[args, tuple(sorted(kwargs.iteritems()))] = function(self, *args, **kwargs)
            return newfunction(self, *args, **kwargs)
    newfunction.__name__ = function.__name__
    return newfunction

@contextlib.contextmanager
def cd(newdir):
    """http://stackoverflow.com/a/24176022/5228524"""
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

class KeepWhileOpenFile(object):
    def __init__(self, name, message=None):
        logging.debug("creating KeepWhileOpenFile {}".format(name))
        self.filename = name
        if message is None: message = LSB_JOBID
        self.__message = message
        self.pwd = os.getcwd()
        self.fd = self.f = None
        self.bool = False

    @property
    def wouldbevalid(self):
        if self: return True
        with self:
            return bool(self)

    @property
    def runningjobid(self):
        try:
            with open(self.filename) as f:
                return int(f.read())
        except (IOError, ValueError):
            return None

    def __open(self):
        self.fd = os.open(self.filename, os.O_CREAT | os.O_EXCL | os.O_WRONLY)

    def __enter__(self):
        logging.debug("entering KeepWhileOpenFile {}".format(self.filename))
        with cd(self.pwd):
            logging.debug("does it exist? {}".format(os.path.exists(self.filename)))
            try:
                logging.debug("trying to open")
                self.__open()
            except OSError:
                logging.debug("failed: it already exists")
                if self.__message == LSB_JOBID:
                    logging.debug("message is a jobid: check if the job died")
                    try:
                        with open(self.filename) as f:
                            oldjobid = int(f.read())
                        logging.debug("job is {}".format(oldjobid))
                    except IOError:
                        logging.debug("tried to read the jobid, but the file doesn't exist anymore")
                        try:
                            self.__open()
                            logging.debug("opened successfully this time")
                        except OSError:
                            logging.debug("and now it exists again, giving up")
                            return None
                    except ValueError:
                        logging.debug("the file contents are not an int --> probably being run interactively")
                        return None
                    else:
                        if jobexists(oldjobid):
                            logging.debug("and that job is still running")
                            return None
                        else:
                            logging.debug("and that job is no longer running, trying to remove")
                            try:
                                os.remove(self.filename)
                                logging.debug("removed successfully")
                            except OSError:   #another job removed it already
                                logging.debug("too late, it's already gone")
                            try:
                                logging.debug("trying to open again")
                                self.__open()
                                logging.debug("opened successfully")
                            except OSError:
                                logging.debug("and now it exists again, giving up")
                                return None
                else:
                    return None

            logging.debug("succeeded: it didn't exist")
            logging.debug("does it now? {}".format(os.path.exists(self.filename)))
            if not os.path.exists(self.filename):
                logging.warning("{} doesn't exist!??".format(self.filename))
            self.f = os.fdopen(self.fd, 'w')

            logging.debug("{}".format(self.__message))
            if self.__message == LSB_JOBID:
                self.__message = self.__message()
            try:
                if self.__message is not None:
                    logging.debug("writing message")
                    self.f.write(self.__message+"\n")
                    logging.debug("wrote message")
            except IOError:
                logging.debug("failed to write message")
                pass
            try:
                logging.debug("trying to close")
                self.f.close()
                logging.debug("closed")
            except IOError:
                logging.debug("failed to close")
                pass
            self.bool = True
            return True

    def __exit__(self, *args):
        logging.debug("exiting")
        if self:
            try:
                with cd(self.pwd):
                    logging.debug("trying to remove")
                    os.remove(self.filename)
                    logging.debug("removed")
            except OSError:
                logging.debug("failed")
                pass #ignore it
        self.fd = self.f = None
        self.bool = False

    def __nonzero__(self):
        return self.bool

@contextlib.contextmanager
def KeepWhileOpenFiles(*filenames):
  if not filenames:
    yield []
    return
  with KeepWhileOpenFile(filenames[0]) as kwof, KeepWhileOpenFiles(*filenames[1:]) as kwofs:
    yield [kwof] + kwofs

class Tee(object):
    """http://stackoverflow.com/a/616686/5228524"""
    def __init__(self, *openargs, **openkwargs):
        self.openargs = openargs
        self.openkwargs = openkwargs
    def __enter__(self):
        self.file = open(*self.openargs, **self.openkwargs)
        self.stdout = sys.stdout
        sys.stdout = self
        return self
    def __exit__(self, *args):
        sys.stdout = self.stdout
        self.file.close()
    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

class OneAtATime(KeepWhileOpenFile):
    def __init__(self, name, delay, message=None, printmessage=None, task="doing this"):
        super(OneAtATime, self).__init__(name, message=message)
        self.delay = delay
        if printmessage is None:
            printmessage = "Another process is already {task}!  Waiting {delay} seconds."
        printmessage = printmessage.format(delay=delay, task=task)
        self.__printmessage = printmessage

    def __enter__(self):
        while True:
            result = super(OneAtATime, self).__enter__()
            if result:
                return result
            print self.__printmessage
            time.sleep(self.delay)

def jsonloads(jsonstring):
    try:
        return json.loads(jsonstring)
    except:
        print jsonstring
        raise

def pairwise(iterable):
    """
    https://docs.python.org/2/library/itertools.html#recipes
    """
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def callclassinitfunctions(*names):
    def callfunctions(cls):
        for name in names:
            getattr(cls, name)()
        return cls
    return callfunctions

def product(iterable):
    return reduce(operator.mul, iterable, 1)

def LoadMacro(filename):
    done = False
    while not done:
        with KeepWhileOpenFile(filename.rstrip("+")+".tmp") as kwof:
            if not kwof:
                print "Another process is already loading {}, waiting 5 seconds...".format(filename)
                time.sleep(5)
                continue
            error = ROOT.gROOT.LoadMacro(filename)
            if error:
                raise IOError("Couldn't load "+filename+"!")
            done = True

def tlvfromptetaphim(pt, eta, phi, m):
    result = ROOT.TLorentzVector()
    result.SetPtEtaPhiM(pt, eta, phi, m)
    return result

def sign(x):
    return cmp(x, 0)

def generatortolist(function):
    return generatortolist_condition(lambda x: True)(function)

def generatortolist_condition(condition):
    def generatortolist(function):
        def newfunction(*args, **kwargs):
            return [_ for _ in function(*args, **kwargs) if condition(_)]
        newfunction.__name__ = function.__name__
        return newfunction
    return generatortolist


def rreplace(s, old, new, occurrence):
    """http://stackoverflow.com/a/2556252/5228524"""
    li = s.rsplit(old, occurrence)
    return new.join(li)

def mkdir_p(path):
    """http://stackoverflow.com/a/600612/5228524"""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def is_almost_integer(flt):
    if isinstance(flt, (int, long)) or flt.is_integer(): return True
    if float("{:.8g}".format(flt)).is_integer(): return True
    return False

class JsonDict(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def keys(self): pass

    @property
    def default(self):
        return JsonDict.__nodefault

    @abc.abstractmethod
    def dictfile(self):
        """should be a member, not a method"""





    __nodefault = object()
    __dictscache = collections.defaultdict(lambda: None)

    def setvalue(self, value):
        if isinstance(value, list): value = tuple(value)
        self.setnesteddictvalue(self.getdict(), *self.keys, value=value)
        assert self.value == value, (self.value, value)

    def getvalue(self):
        try:
            return self.getnesteddictvalue(self.getdict(), *self.keys, default=self.default)
        except:
            print "Error while getting value of\n{!r}".format(self)
            raise

    def delvalue(self):
        self.delnesteddictvalue(self.getdict(), *self.keys)

    @property
    def value(self):
        return self.getvalue()

    @value.setter
    def value(self, value):
        self.setvalue(value)

    @classmethod
    def getdict(cls, trycache=True):
      import globals
      if cls.__dictscache[cls] is None or not trycache:
        try:
          with open(cls.dictfile) as f:
            jsonstring = f.read()
        except IOError:
          try:
            os.makedirs(os.path.dirname(cls.dictfile))
          except OSError:
            pass
          with open(cls.dictfile, "w") as f:
            f.write("{}\n")
            jsonstring = "{}"
        cls.__dictscache[cls] = json.loads(jsonstring)
      return cls.__dictscache[cls]

    @classmethod
    def writedict(cls):
      dct = cls.getdict()
      jsonstring = json.dumps(dct, sort_keys=True, indent=4, separators=(',', ': '))
      with open(cls.dictfile, "w") as f:
        f.write(jsonstring)

    @classmethod
    def getnesteddictvalue(cls, thedict, *keys, **kwargs):
        hasdefault = False
        for kw, kwarg in kwargs.iteritems():
           if kw == "default":
               if kwarg is not JsonDict.__nodefault:
                   hasdefault = True
                   default = kwarg
           else:
               raise TypeError("Unknown kwarg {}={}".format(kw, kwarg))

        if len(keys) == 0:
            return thedict

        if hasdefault and keys[0] not in thedict:
            if len(keys) == 1:
                thedict[keys[0]] = default
            else:
                thedict[keys[0]] = {}

        return cls.getnesteddictvalue(thedict[keys[0]], *keys[1:], **kwargs)

    @classmethod
    def setnesteddictvalue(cls, thedict, *keys, **kwargs):
        for kw, kwarg in kwargs.iteritems():
            if kw == "value":
                value = kwarg
            else:
                raise TypeError("Unknown kwarg {}={}".format(kw, kwarg))

        try:
            value
        except NameError:
            raise TypeError("Didn't provide value kwarg!")

        if len(keys) == 1:
            thedict[keys[0]] = value
            return

        if keys[0] not in thedict:
            thedict[keys[0]] = {}

        return cls.setnesteddictvalue(thedict[keys[0]], *keys[1:], **kwargs)

    @classmethod
    def delnesteddictvalue(cls, thedict, *keys):
        if len(keys) == 1:
            del thedict[keys[0]]
            return

        cls.delnesteddictvalue(thedict[keys[0]], *keys[1:])
        if not thedict[keys[0]]:
            del thedict[keys[0]]

def LSB_JOBID():
    import config
    if config.host == "lxplus":
        return os.environ.get("LSB_JOBID", None)
    if config.host == "MARCC":
        return os.environ.get("SLURM_JOBID", None)
    assert False, config.host

def jobexists(jobid):
    import config
    if config.host == "lxplus":
        return "is not found" not in subprocess.check_output(["bjobs", str(jobid)])
    if config.host == "MARCC":
        try:
            return str(jobid) in subprocess.check_output(["squeue", "--job", str(jobid)], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            if "slurm_load_jobs error: Invalid job id specified" in e.output:
                return False
            print e.output
            raise
    assert False, config.host

class Fake_LSF_creating(object):
    def basename(self, filename): return filename

class LSF_creating(object):
    def __init__(self, *files, **kwargs):
        self.files = files
        self.inputfiles = ()

        self.jsonfile = None
        self.ignorefailure = False
        self.skipifexists = False
        for kw, kwarg in kwargs.iteritems():
            if kw == "jsonfile":
                self.jsonfile = kwarg
                if not self.jsonfile.startswith("/"): raise ValueError("jsonfile={} should be an absolute path!".format(self.jsonfile))
            elif kw == "ignorefailure":
                self.ignorefailure = kwarg
            elif kw == "skipifexists":
                self.skipifexists = kwarg
            elif kw == "inputfiles":
                self.inputfiles = tuple(kwarg)
            else:
                raise TypeError("Unknown kwarg {}={}!".format(kw, kwarg))

        for filename in files+self.inputfiles:
            if not filename.startswith("/"):
                raise ValueError("{} should be an absolute path!".format(filename))

    def __enter__(self):
        if not LSB_JOBID(): return self
        import config
        if self.jsonfile is not None:
            shutil.copy(self.jsonfile, "./")
            self.jsonfile = os.path.basename(self.jsonfile)
            if len(self.files) != 1: raise ValueError("only know how to handle 1 file")

            with open(os.path.basename(self.jsonfile)) as f:
                content = f.read()

            if content.count(self.files[0]) != 1:
                raise ValueError("{} is not in {}".format(self.files[0], self.jsonfile))
            content = content.replace(self.files[0], os.path.basename(self.files[0]))

            with open(os.path.basename(self.jsonfile), "w") as f:
                f.write(content)

        for inputfile in self.inputfiles:
            if not os.getcwd().startswith("/tmp") and not (hasattr(config, "scratchdir") and os.getcwd().startswith(config.scratchdir)):
                raise RuntimeError("Have to run this from /tmp")
            shutil.copy(inputfile, os.getcwd())

        return self

    def basename(self, filename):
        if filename not in self.files+self.inputfiles: raise ValueError("Unknown filename {}!".format(filename))
        if LSB_JOBID():
            return os.path.basename(filename)
        else:
            return filename

    def __exit__(self, *errorinfo):
        if not LSB_JOBID(): return

        notcreated = []

        for filename in self.files:
            if os.path.exists(filename) and self.skipifexists: continue
            if os.path.exists(os.path.basename(filename)):
                shutil.move(os.path.basename(filename), filename)
            else:
                notcreated.append(os.path.basename(filename))

        if notcreated and not self.ignorefailure:
            raise RuntimeError("\n".join("{} was not created!".format(os.path.basename(filename)) for filename in filenames))

def RooArgList(*args, **kwargs):
    name = None
    for kw, kwarg in kwargs.iteritems():
        if kw == "name":
            name = kwarg
        else:
            raise TypeError("Unknown kwarg {}={}!".format(kw, kwarg))
    args = list(args)
    if name is None and isinstance(args[-1], basestring):
        name = args[-1]
        args = args[:-1]

    if len(args) < 4:
        if name is not None:
            args.append(name)
        return ROOT.RooArgList(*args)

    nameargs = [name] if name is not None else []
    result = ROOT.RooArgList(*nameargs)
    for arg in args:
        result.add(arg)
    return result

def inscreen():
    return bool(os.environ.get("STY"))

class DummyContextManager(object):
    def __enter__(self): return self
    def __exit__(*stuff): pass

class mkdtemp(object):
  def __init__(self, **kwargs):
    import config
    if "dir" not in kwargs:
      if LSB_JOBID() is not None:
        if config.host == "lxplus":
          kwargs["dir"] = os.environ["LSB_JOB_TMPDIR"]
        elif config.host == "MARCC":
          kwargs["dir"] = config.scratchdir
        else:
          assert False, config.host
    self.kwargs = kwargs

  def __enter__(self):
    self.tmpdir = tempfile.mkdtemp(**self.kwargs)
    if LSB_JOBID():
      with open(os.path.join(self.tmpdir, "JOBID"), "w") as f:
        f.write(LSB_JOBID())
    return self.tmpdir

  def __exit__(self, *error):
    shutil.rmtree(self.tmpdir)

def cleanupscratchdir():
  import config
  if not hasattr(config, "scratchdir"): return
  for folder in glob.iglob(os.path.join(config.scratchdir, "*", "")):
    try:
      with open(os.path.join(folder, "JOBID")) as f:
        jobid = f.read().strip()
        if not jobexists(jobid):
          print "job {} was using {}, but died --> deleting the folder".format(jobid, folder)
          try:
            shutil.rmtree(folder)
          except:
            print "failed to remove it, see if it's still there"
    except IOError:
      print "please check on {}, it has no JOBID file".format(folder)
    except subprocess.CalledProcessError:
      print "squeue failed, can't check if job {} is still running".format(jobid)

def getmembernames(*args, **kwargs):
    return [_[0] for _ in inspect.getmembers(*args, **kwargs)]

lastcmsswbase = None

"""
this doesn't work
def cmsenv(folder="."):
    global lastcmsswbase
    #pythonpath needs special handling
    oldpythonpath = os.environ["PYTHONPATH"].split(":")
    indexinsyspath = sys.path.index(oldpythonpath[0])
    with cd(folder):
        scram = subprocess.check_output(["scram", "ru", "-sh"])
        for line in scram.splitlines():
            potentialerror = ValueError("Unknown scram b output:\n{}".format(line))
            if line.split()[0] == "unset":
                if line[-1] != ';': raise potentialerror
                line = line[:-1]
                for variable in line.split()[1:]:
                    del os.environ[variable]
            elif line.split()[0] == "export":
                afterexport = line.split(None, 1)[1]
                variable, value = afterexport.split("=", 1)
                if value[0] != '"' or value[-2:] != '";': raise potentialerror
                value = value[1:-2]
                if "\\" in value or '"' in value or "'" in line: raise potentialerror
                os.environ[variable] = value
            else:
                raise potentialerror
    newpythonpath = os.environ["PYTHONPATH"].split(":")
    for _ in oldpythonpath: sys.path.remove(_)
    sys.path[indexinsyspath:indexinsyspath] = newpythonpath
    if lastcmsswbase is not None and os.environ["CMSSW_BASE"] != lastcmsswbase:
        raise ValueError("Can't cmsenv in both {} and {}!".format(lastcmsswbase, os.environ["CMSSW_BASE"]))
    lastcmsswbase = os.environ["CMSSW_BASE"]
"""

def requirecmsenv(folder):
    needcmsswbase = subprocess.check_output("cd {} && eval $(scram ru -sh) >& /dev/null && echo $CMSSW_BASE".format(pipes.quote(folder)), shell=True).strip()
    cmsswbase = os.environ["CMSSW_BASE"]
    if cmsswbase != needcmsswbase:
        raise ValueError("Need to cmsenv in {}!".format(needcmsswbase))

def deletemelastuff():
    if os.path.exists("Pdfdata"):
        shutil.rmtree("Pdfdata")
    for thing in "br.sm1", "br.sm2", "ffwarn.dat", "input.DAT", "process.DAT":
        if os.path.exists(thing):
            os.remove(thing)

@contextlib.contextmanager
def cdtemp():
  with mkdtemp() as tmpdir, cd(tmpdir):
    yield

def cdtemp_slurm():
  import config
  if config.host == "MARCC" and LSB_JOBID() is not None:
    return cdtemp()
  return DummyContextManager()

def recursivesubclasses(cls):
    result = [cls]
    for subcls in cls.__subclasses__():
        result += recursivesubclasses(subcls)
    return result

class TFile(object):
  def __init__(self, filename, *args, **kwargs):
    self.__filename = filename
    self.__args = args
    self.__deleteifbad = kwargs.pop("deleteifbad", False)
    self.__entered = False
    self.__contextmanager = kwargs.pop("contextmanager", True)
    assert not kwargs
    
    if not self.__contextmanager: self.__enter__()

  def __enter__(self):
    if self.__entered: raise ValueError("Trying to enter {} twice!".format(self))
    import ROOT
    self.__bkpdirectory = ROOT.gDirectory.GetDirectory(ROOT.gDirectory.GetPath())
    self.__f = ROOT.TFile.Open(self.__filename, *self.__args)
    self.__entered = True
    if not self.__f:
      raise IOError(self.__filename+" is a null pointer, see above for details.")
    if self.IsZombie():
      self.__exit__()
      raise IOError(self.__filename+" is a zombie, see above for details.")

    try:
      openoption = self.__args[0].upper()
    except IndexError:
      openoption = ""

    self.__write = {
      "": False,
      "READ": False,
      "NEW": True,
      "CREATE": True,
      "RECREATE": True,
      "UPDATE": True,
    }[openoption]

    return self.__f

  def __exit__(self, *errorstuff):
    if self.__write and (not any(errorstuff) or not self.__deleteifbad):
      self.Write()
    self.Close()
    self.__bkpdirectory.cd()
    if self.__write and self.__deleteifbad and any(errorstuff):
      os.remove(self.__filename)

  def __repr__(self):
    return "{.__name__}('{}', deleteifbad={}, contextmanager={})".format(type(self), self.__filename, deleeteifbad, self.__contextmanager)

  def __getattr__(self, attr):
    if not self.__entered:
      raise AttributeError("Trying to get {} from {!r} before entering it".format(attr, self))
    return getattr(self.__f, attr)

def setname(name):
    def decorator(function):
        function.__name__ = name
        return function
    return decorator

def deprecate(thing, *datetimeargs, **datetimekwargs):
    when = datetime.datetime(*datetimeargs, **datetimekwargs)
    if datetime.datetime.now() >= when:
        raise RuntimeError("fix this!")
    return thing

def sgn(number):
  return math.copysign(1, number)

class TCanvas(ROOT.TCanvas):
    def __init__(self, *args, **kwargs):
        self.__plotcopier = kwargs.pop("plotcopier", None)
        return super(TCanvas, self).__init__(*args, **kwargs)
    def SaveAs(self, filename="", *otherargs, **kwargs):
        absfilename = os.path.abspath(filename)
        if self.__plotcopier:
            self.__plotcopier.copy(filename)
        return super(TCanvas, self).SaveAs(filename, *otherargs, **kwargs)

class PlotCopier(object):
    import config

    def __init__(
      self,
      copyfromconfig=config.getconfiguration("login-node", config.marccusername),
      copytoconfig=config.getconfiguration("lxplus", config.lxplususername),
      copyfromfolder=None,
      copytofolder=None,
      copyfromhost=None,
      copytoconnect=None,
    ):

        if copyfromfolder is None: copyfromfolder = copyfromconfig["plotsbasedir"]
        if copytofolder is None: copytofolder = copytoconfig["plotsbasedir"]
        if copyfromhost is None: copyfromhost = copyfromconfig["host"]
        if copytoconnect is None: copytoconnect = copytoconfig["connect"]

        self.__tocopy = set()
        self.__copyfromfolder = os.path.join(os.path.abspath(copyfromfolder), "")
        self.__copytofolder = os.path.join(os.path.abspath(copytofolder), "")
        self.__copyfromhost = copyfromhost
        self.__copytoconnect = copytoconnect

    @property
    def copyfromfolder(self): return self.__copyfromfolder
    @property
    def copytofolder(self): return self.__copytofolder
    @property
    def copyfromhost(self): return self.__copyfromhost
    @property
    def copytoconnect(self): return self.__copytoconnect

    def __enter__(self):
        return self

    def __exit__(self, *error):
        import config
        if config.host != self.copyfromhost or not self.__tocopy: return

        command = ["rsync", "-azvP", self.copyfromfolder, self.copytoconnect + ":" + self.copytofolder] + [
          "--include="+_ for _ in self.__tocopy
        ] + ["--exclude=*", "--delete"]

        if LSB_JOBID():
            print
            print "To copy plots, try:"
            print
            print " ".join(pipes.quote(_) for _ in command)
            print
            return

        #getpass instead of raw_input in case you accidentally type your password here
        answer = None
        while answer not in ("", "no"):
            answer = getpass.getpass("press enter when you're ready to rsync, or type no if you don't want to: ")
        try:
            if answer != "no":
                subprocess.check_call(command)
        except:
            print
            print "Failed to copy plots.  To do it yourself, try:"
            print
            print " ".join(pipes.quote(_) for _ in command)
            print
            if all(_ is None for _ in error): raise

    def TCanvas(self, *args, **kwargs):
        return TCanvas(plotcopier=self, *args, **kwargs)

    def copy(self, filename):
        absfilename = os.path.abspath(filename)
        if not self.copyfromfolder in absfilename: return
        relativefilename = "/"+absfilename.replace(self.copyfromfolder, "")
        for i in range(relativefilename.count("/")):
            self.__tocopy.add(relativefilename.rsplit("/", i)[0])

    def open(self, filename, *args, **kwargs):
        self.copy(filename)
        return open(filename, *args, **kwargs)

    def remove(self, filename, *args, **kwargs):
        os.remove(filename, *args, **kwargs)
        self.copy(filename)

def existsandvalid(filename, *shouldcontain):
  with KeepWhileOpenFile(filename+".tmp") as kwof:
    if not kwof: return True  #it may be valid when the job is done
    if not os.path.exists(filename): return False

    if filename.endswith(".root"):
      try:
        with TFile(filename) as f:
          for _ in shouldcontain:
            getattr(f, _)
      except (AttributeError, ReferenceError):
        os.remove(filename)

    elif filename.endswith(".json"):
      with open(filename) as f:
        try:
          json.load(f)
        except ValueError:
          os.remove(filename)

    else:
      raise ValueError("Don't know what to do with:\n"+filename)

    return os.path.exists(filename)

def writeplotinfo(txtfilename, *morestuff, **kwargs):
  plotcopier = kwargs.pop("plotcopier", ROOT)
  assert not kwargs, kwargs
  assert txtfilename.endswith(".txt")
  with open(txtfilename, "w") as f:
    f.write(" ".join(["python"]+[pipes.quote(_) for _ in sys.argv]))
    f.write("\n\n\n")
    for thing in morestuff:
      f.write(thing)
    f.write("\n\n\n\n\n\ngit info:\n\n")
    f.write(subprocess.check_output(["git", "rev-parse", "HEAD"]))
    f.write("\n")
    f.write(subprocess.check_output(["git", "status"]))
    f.write("\n")
    f.write(subprocess.check_output(["git", "diff"]))
  if plotcopier != ROOT:
    plotcopier.copy(txtfilename)

def debugfunction(function):
  @wraps(function)
  def newfunction(*args, **kwargs):
    result = function(*args, **kwargs)
    print "{.__name__}({}{}{})={}".format(function, ", ".join(str(_) for _ in args), ", " if args and kwargs else "", ", ".join("{}={}".format(k, v) for k, v in kwargs.iteritems()), result)
    return result
  return newfunction

def reiglob(path, exp, invert=False, verbose=False, hastomatch=False, okifnofolder=False):
  "https://stackoverflow.com/a/17197678/5228524"
  print path, exp

  if verbose: print "reiglobbing "+os.path.join(path, exp)

  m = re.compile(exp)

  n = 0

  try:
    for f in os.listdir(path):
      if bool(m.match(f)) != bool(invert):
        n += 1
        if verbose and n % 100 == 0: print "Found {} files so far".format(n)
        yield os.path.join(path, f)
  except OSError:
    if not okifnofolder: raise

  if hastomatch and n == 0:
    raise ValueError(exp + " didn't match anything in " + path)

def reglob(*args, **kwargs):
  return list(reiglob(*args, **kwargs))

@cache
def withdiscriminantsfileisvalid(filename):
  if not os.path.exists(filename):
    return False
  with TFile(filename) as f:
    if (not f) or (f.candTree.GetEntries() == 0):
      return False
  return True

class WriteOnceDict(dict):
    def __init__(self, messagefmt="{key} has already been set"):
        self.messagefmt = messagefmt
    def __setitem__(self, key, value):
        if key in self:
            if value == self[key]: return
            raise KeyError(self.messagefmt.format(key=key, newvalue=value, oldvalue=self[key]))
        super(WriteOnceDict, self).__setitem__(key, value)

