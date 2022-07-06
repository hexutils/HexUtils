# All targets with # symbol are self-documenting, i.e. make help or simply make will
# show the targets among available options
#
# User targets are at the bottom
#
ifndef ROOTSYS
all:
	@echo "ROOTSYS is not set. Please set ROOT environment properly"; echo
else
ifndef ROOFITSYS
all:
	@echo "ROOFITSYS is not set. Please set ROOT environment properly"; echo
else


RM  = /bin/rm

MELADIR = $(shell pwd)
MELASRCDIR = $(MELADIR)/src
MELADATADIR = $(MELADIR)/data
MELAOBJDIR = $(MELADIR)/obj
# Modify MELALIBDIR for the gcc version as needed
MELALIBDIR = $(MELADATADIR)/${SCRAM_ARCH}
# _melapkgpath_ should refer to the root compilation path just like MELADIR with an extra '/'.
# If environment variables need to be inserted without expansion for portability,
# you can use '.oODOLLAROo..oOOPEN_BRACKETOo.[YOUR_ENV_VARIABLE].oOCLOSE_BRACKETOo.',
# e.g. '.oODOLLAROo..oOOPEN_BRACKETOo.CMSSW_BASE.oOCLOSE_BRACKETOo.' in place of '${CMSSW_BASE}' as used in the CMS-specific compilation.
MELAPKGPATH = $(MELADIR)/
LIB = libJHUGenMELAMELA.so
LIBRULE = $(MELALIBDIR)/$(LIB)

ROOTCFLAGS = $(shell root-config --cflags)
ROOTLIBS = $(shell root-config --libs) -Lrootlib
NLIBS = $(ROOTLIBS)
NLIBS += -L$(ROOFITSYS)/lib -lMinuit -lRooFitCore -lRooFit -lgfortran
LIBS = $(filter-out -lNew, $(NLIBS))

ROOFITINC = -I$(ROOFITSYS)/include
ROOTINC = $(ROOFITINC)

CC = g++
CPPINC = -I$(MELADIR)/interface $(ROOTINC)
CPPLOAD = -L$(MELALIBDIR) -lmcfm_707 -ljhugenmela -lcollier $(LIBS)
CPPOPTS =  -fPIC -O2 -ftree-vectorize -fipa-pta -felide-constructors -fvisibility-inlines-hidden -fno-math-errno \
	--param vect-max-version-for-alias-checks=50 -fmessage-length=0 -fdiagnostics-show-option \
	-Werror=unused-value \
	 $(shell root-config --cflags) -D_melapkgpath_=$(MELAPKGPATH)
CPPFLAGS = $(CPPOPTS) $(CPPINC) $(CPPLOAD)

LINKER = g++
LINKERFLAGS = -Wl,-rpath=$(MELALIBDIR),-soname,$(LIB) $(CPPLOAD)

SOURCESCC = $(wildcard $(MELASRCDIR)/*.cc)
SOURCESCXX = $(wildcard $(MELASRCDIR)/*.cxx)
OBJECTSPRIM = $(SOURCESCC:.cc=.o) $(SOURCESCXX:.cxx=.o)
OBJECTS = $(subst $(MELASRCDIR),$(MELAOBJDIR),$(OBJECTSPRIM))

.PHONY: all help compile clean

.SILENT: alldirs $(OBJECTS) $(MELAOBJDIR)/LinkDef_out.o $(LIBRULE) python/__init__.py clean

all: $(LIBRULE) python/__init__.py

$(MELAOBJDIR)/%.d:	$(MELASRCDIR)/%.c* | alldirs
	echo "Checking dependencies for $<"; \
	$(CC) -MM -MT $@ -MT ${@:.d=.o} $(CPPFLAGS) $< > $@; \
                     [ -s $@ ] || rm -f $@

$(MELAOBJDIR)/%.o: 	$(MELASRCDIR)/%.c* | alldirs
	echo "Compiling $<"; \
	$(CC) $(CPPFLAGS) $< -c -o $@

$(MELAOBJDIR)/LinkDef_out.o: | alldirs
	echo "Making CINT dictionaries"; \
	rootcint -f $(MELASRCDIR)/LinkDef_out.cc -c -p $(CPPINC) $(MELASRCDIR)/LinkDef.h; \
	cat $(MELASRCDIR)/LinkDef.h $(MELASRCDIR)/LinkDef_out.cc > $(MELASRCDIR)/LinkDef_out.cxx; \
	rm $(MELASRCDIR)/LinkDef_out.cc; mv $(MELASRCDIR)/LinkDef_out_rdict.pcm $(MELALIBDIR)/LinkDef_out_rdict.pcm; \
	$(CC) $(CPPOPTS) $(CPPINC) -c $(MELASRCDIR)/LinkDef_out.cxx -o $(MELAOBJDIR)/LinkDef_out.o; \
	rm -f $(MELASRCDIR)/LinkDef_out.cxx

$(LIBRULE):	$(OBJECTS) $(MELAOBJDIR)/LinkDef_out.o | alldirs
	echo "Linking $(LIB)"; \
	$(LINKER) $(LINKERFLAGS) -shared $(OBJECTS) $(MELAOBJDIR)/LinkDef_out.o -o $@

alldirs:
	mkdir -p $(MELAOBJDIR)

python/__init__.py:
	touch python/__init__.py

clean:
	rm -v -r -f \
	$(MELAOBJDIR) $(MELASRCDIR)/LinkDef_out* $(MELALIBDIR)/$(LIB) $(MELALIBDIR)/LinkDef_out_rdict.pcm; \
	echo "Done cleaning MELA"


endif
endif
