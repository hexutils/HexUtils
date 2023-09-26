import re
import os
import functools
import numpy as np
import useful_funcs_and_constants
import warnings

class lhe_reader(object):
    def __init__(self, lhefile) -> None:
        """A class to read LHE files and perform cursory operations like 
        cutting down to size, checking equality, and ROOT conversion

        Parameters
        ----------
        lhefile : str
            the .lhe file you are using

        Raises
        ------
        FileNotFoundError
            Filename should have the .lhe extension
        """
        if lhefile.split('.')[-1] != 'lhe':
            raise FileNotFoundError("LHE File Extension Required for file " + lhefile + "!")
        
        self.lhefile = os.path.abspath(lhefile)
        self.event_selection_regex = re.compile(r'(?s)(<event>(.*?)</event>)') #regular expression to find every event
        
        with open(self.lhefile) as f:
            self.text = f.read()
        
    @functools.cached_property 
    def cross_section(self):
        """Gets the cross section and its uncertainty using regular expressions
        https://docs.python.org/dev/library/functools.html#functools.cached_property
        Returns
        -------
        Tuple[str, str]
            A tuple of strings containing the cross section and its uncertainty
        """
        
        cross_section = uncertainty = ""
        
        # with open(self.lhefile) as getting_cross_section:
        head = self.non_event_portions[0] #The part before the events contains the cross section
        
        #This regex was made by the very very helpful https://pythex.org/ (shoutout UVA professor Upsorn Praphamontripong)
        cross_finder = re.compile(r'<init>\n.+\n.+(\d+\.\d+E(\+|-)\d{2})\s+(\d+\.\d+E(\+|-)\d{2})\s+(\d+\.\d+E(\+|-)\d{2})(\d|\s)+</init>')
        cross_section_match = re.search(cross_finder,head)
        
        cross_section = cross_section_match.group(1)
        
        uncertainty = cross_section_match.group(3)
        
        return float(cross_section), float(uncertainty) #returns the cross section and its uncertainty
    
    @functools.cached_property 
    def all_events(self):
        """This function opens and collects every LHE event and puts them in a list to return
        Attribute is stored as a cached property
        https://docs.python.org/dev/library/functools.html#functools.cached_property
        
        Returns
        -------
        list[str]
            A list of every event sequence as strings from the file (everything between every <event> and </event>)
        """
        all_matches = re.findall(self.event_selection_regex, self.text)
        all_matches = [item[0] for item in all_matches]
        return all_matches
    
    @functools.cached_property
    def num_events(self):
        """Returns the number of events in the file as a cached property
        https://docs.python.org/dev/library/functools.html#functools.cached_property
        
        Returns
        -------
        int
            The number of events in the LHE file
        """
        return len(self.all_events)
        
    @functools.cached_property
    def non_event_portions(self):
        """This function gets everything in an LHE file that is not an event 
        (everything before the first <event> and everything after the last </event>)
        https://docs.python.org/dev/library/functools.html#functools.cached_property
        
        Returns
        -------
        Tuple[str, str]
            Two strings of everything before the first <event> and everything after the last </event>
        """
        f_start = self.text[:self.text.find("<event>")] #everything until the first event
        f_end = self.text[self.text.rfind("</event>") + len("</event>"):] #everything after the last event
        return f_start, f_end

    def __eq__(self, __o: object) -> bool:
        """Defines a metric for equality between two LHE files

        Parameters
        ----------
        __o : object
            Some other object - only useful if it's another LHE_reader class

        Returns
        -------
        bool
            Whether the events are the same
        """
        if isinstance(__o, lhe_reader):
            if self.all_events == __o.all_events:
                return True
        
        return False
     
    def __str__(self) -> str:
        """Function toString that displays the number of events and the cross section of an LHE file

        Returns
        -------
        str
            the string representation of the class
        """
        to_str = ""
        to_str += "LHE file " + self.lhefile
        to_str += "\n\tN: " + str(self.num_events)
        to_str += "\n\t\u03C3: " + "{:e}".format(self.cross_section[0]) + "\n" #\u03C3 is the unicode for sigma
        return to_str

    def cut_down_to_size(self, n, verbose=False, shuffled=False, dump=""):
        """Cuts the number of events in an LHE file down to n events while preserving other aspects of the file
        Outputs a string that should be placed in a file of your choice

        Parameters
        ----------
        n : int
            The number of events you want to keep
        verbose : bool, optional
            Whether you want the function to be verbose, by default False
        shuffled : bool, optional
            Whether you want the lhe files to be shuffled before sampling them, by default False
        dump : str, optional
            Place a filename here WITHOUT the .lhe extension if you want to dump the sliced file with the filename of dump, by default ""

        Returns
        -------
        str
            A string that should be passed to a file of the LHE file

        Raises
        ------
        TypeError
            n should have the ability to become an integer
        ValueError
            n must be > 0
        """
        start_of_file, end_of_file = self.non_event_portions
        
        orig_num = len(self.all_events) #this is a sneaky way to also enforce that all the events are precomputed here
        
        try:
            n = int(n)
        except:
            raise TypeError("n should be integer-like!")
        
        if n == orig_num:
            return start_of_file + ("\n".join(self.all_events)) + end_of_file
        elif n > orig_num:
            warnings.warn("The number of events selected is > the number of events in the file")
            return start_of_file + ("\n".join(self.all_events)) + end_of_file #just return the whole file
        elif n <= 0:
            raise ValueError("Selecting <= 0 events makes literally no sense")
        
        if verbose:
            print("{:.3e}".format(orig_num), "events ->", "{:.3e}".format(n), "events")
            print("Shuffling is turned", "on" if shuffled else "off")
            
        cut_down = np.random.choice(self.all_events, n) if shuffled else self.all_events[:n]
        
        written_file = start_of_file + ("\n".join(cut_down)) + end_of_file
        
        if dump and not os.path.isfile(dump + '.lhe'):
            with open(dump+'.lhe', 'w+') as f:
                f.write(written_file)
        elif os.path.isfile(dump + '.lhe'):
            warnings.warn('\n'+dump + '.lhe already exists! Not dumping file.\n', UserWarning)
        
        return written_file #this would be placed directly into a file
    
    
    def to_ROOT(self, argument, env, other_args=[], output_directory='./', output_prefix='LHE', verbose=False, replace=False,):
        """Converts a single LHE file to ROOT using the lhe2root tool
        This works best for Higgs->4l of some kind, as that is what lhe2root is made for

        Parameters
        ----------
        argument : str
            This should be one of the viable lhe2root options
        env : dict
            This contains the lhe2root environment variables by doing dict(os.environ) in a main method
        other_args : list[str]
            The other lhe2root arguments that can be used (see lhe_2_root_args in useful_funcs_and_constants), by default []
        output_directory : str, optional
            The directory to output the ROOT file to, by default './'
        output_prefix : str, optional
            The prefix attached to the ROOT file, by default 'LHE_'
        verbose : bool, optional
            If false, all output is suppressed, by default False
        replace : bool, optional
            If true, when an identical ROOT file is found it will overwrite the file, by default False

        Raises
        ------
        FileNotFoundError
            MELA pathways should be configured to use LHE2ROOT
        ValueError
            One of the specified lhe2root configurations should be used
        ValueError
            One of the specified lhe2root arguments should be used
        FileNotFoundError
            The output directory should be a valid directory
        TypeError
            The environment variables should be a dictionary
        """
        if not useful_funcs_and_constants.check_for_MELA(env):
            raise FileNotFoundError("MELA Path not found in given environment!")
        
        if argument not in useful_funcs_and_constants.lhe_2_root_options:
            raise ValueError("Invalid LHE2ROOT option!")
        
        if other_args:
            print("Other arguments being used:", other_args)
        for arg in other_args:
            if arg not in useful_funcs_and_constants.lhe_2_root_args:
                raise ValueError("Invalid LHE2ROOT option!")
        
        if not os.path.isdir(output_directory):
            raise FileNotFoundError("Output Directory is invalid!")
        
        if not isinstance(env, dict):
            raise TypeError("Environment should be a dictionary i.e. dict(os.environ)")
        
        output_directory = os.path.abspath(output_directory)
        
        if output_directory[-1] != '/':
            output_directory += '/'
        
        input_filename = self.lhefile.split('/')[-1]
        output_filename = output_prefix + '_' + input_filename[:input_filename.rfind('.')] + '.root'
        
        outfile = output_directory + output_filename
        if os.path.isfile(outfile):
            print(outfile, "already exists!")
            if replace:
                print("replacing", outfile)
                useful_funcs_and_constants.safely_run_process("rm " + output_directory + output_filename, env)
            else:
                return outfile
        
        titlestr = "Generating ROOT file for " + os.path.relpath(self.lhefile)
        
        useful_funcs_and_constants.print_msg_box("Input name: " + self.lhefile.split('/')[-1] + #This is the big message box seen per LHE file found
            "\nOutput: " + str(os.path.relpath(outfile)) + 
            "\nArguments: " + argument +
            (", " + ", ".join(other_args) if other_args else "") +
            "\n\u03C3: " + "{:.4e}".format(self.cross_section[0]) + " \u00b1 " + "{:.2e}".format(self.cross_section[1]) + 
            "\nN: " + "{:.4e}".format(self.num_events) + " events",
            title=titlestr, width=len(titlestr))
        
        import lhe2root
        
        argList = [output_directory + output_filename, self.lhefile, '--' + argument]
        argList += '--'.join(other_args)
        
        if not verbose:
            argList += ['--verbose']
        
        print(argList)
        lhe2root.main(argList)
        # running_str = "python3 lhe2root.py --" + argument + " " + output_directory + output_filename + ' '
        # running_str += self.lhefile #lhe2root takes in an argument, the outname, and the input file
        
        # if not verbose:
        #     running_str += ' > /dev/null 2>&1'
        
        
        # useful_funcs_and_constants.safely_run_process(running_str, env)
        
        return outfile