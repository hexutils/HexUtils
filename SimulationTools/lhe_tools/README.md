# LHE2ROOT Helpers
This contains lhe2root, a script for converting lhe files to root files using JHUGenMELA that is focused on 4l Higgs decays.

## Installation Location

This package should be installed within an instance of JHUGenMELA. The recommended location, which would require no edits, would be the same directory as, or a directory below, `mela.py` and `pythonmelautils.py` within the main HexUtils repo. These are normally under HexUtils/AnalysisTools/JHUGenMELA/MELA/python. However, as long as `LD_LIBRARY_PATH` is set, which can be checked using the `check_for_MELA` function, python should be able to find MELA's location.

## Programs Within This Package

- `convert_all_to_ROOT.py`
  - This program will take in command line arguments and convert all the files within your working directory, as well as any subdirectories below, to a ROOT file using lhe2root.py
  
- `plot_one_quantity.py`
  - This program will take in command line arguments and plot a single attribute from a list of ROOT files given

- `plot_interference.py`
  - Given a series of ROOT file interference triplets (one mixed sample file and 2 pure sample files i.e. AB, A, and B) as command line arguments, this program will plot their interference and compare the interference terms for each triplet against each other

- `lhe_reader.py`
  - Given a series of LHE files as command line arguments and an integer number of events this program will cut all of the files given down to the number of events requested

## Useful Functions

All of the programs simply use the functions stored within `lhe2root_methods.py` or `lhe_reader.py` by taking in command line arguments. Should you desire to use any of these functions individually, that is very easy. Simply import `lhe2root_methods` or `lhe_reader` and continue. 

The following functions are included in `lhe2root_methods.py`:

```python 
scale(counts, scaleto)
get_cross_section_from_LHE_file(LHE_file_path)
check_for_MELA()
recursively_convert(current_directory, argument, clean=False, verbose=False, exceptions=set(), write="")
plot_one_quantity(filenames, attribute, xrange, nbins=100, labels=[], norm=False, title="")
plot_interference(mixed_file, pure1, pure2, pure1Name, pure2Name, attribute, cross_sections, nbins=100, title="")
```

These functions have associated docstrings available to look at.


The following functions are included in the `lhe_reader` class in `lhe_reader.py`:
```python
lhe_reader.cross_section()
lhe_reader.all_events()
lhe_reader.non_event_portions()
lhe_reader.cut_down_to_size(n, verbose=False)
lhe_reader.to_ROOT(argument, env, output_directory='./', output_prefix='LHE', verbose=False, replace=False)
```

The lhe_reader class also has associated documentation, visible either in the class or on the documentation site.

## Useful Defined Constants

There are also some useful defined constants within `uesful_funcs_and_constants.py`. There are currently 3 of these such constants:

- `lhe_2_root_options`
  - This is a list of all the possible options that are available to `lhe2root.py`
- `lhe_2_root_args`
  - This is a list of all the possible other arguments that are not mutually exclusive in `lhe2root.py`
- `beautified_title`
  - This dictionary provides a conversion between the shorthand for an attribute (i.e. M4L) and the beautified version suitable for matplotlib (i.e. $m_{4\mu}$) __You should edit this dictionary if you want to change the depiction of certain parameters!__
- `ranges`
  - This dictionary does the same as beautified_title, except it converts the shorthand to the commonly defined ranges (i.e. phi $\in [-\pi, \pi ]$). __You should edit this dictionary if you want to change the ranges of certain parameters!__
- `event_selection_regex`
  - This is the regex that selects events in an LHE file

The following functions are also in the file:
- ```python
  print_msg_box(msg, indent=1, width=None, title=None)
  safely_run_process(running_str, env={})
  check_for_MELA(env)
  ```

## Dependencies

### Dependencies Requiring Installation

You will need following packages. Some packages have dependencies (which are not listed). I would recommend using conda to do any package installations, as it will automatically download any secondary dependencies you may need. For packages that require a conda installation, the conda webpage for each package required is linked below:
  - [numpy](https://anaconda.org/anaconda/numpy)
  - [matplotlib](https://anaconda.org/conda-forge/matplotlib)
  - [pandas](https://anaconda.org/anaconda/pandas)
  - [ROOT](https://anaconda.org/conda-forge/root/)
  - [uproot](https://anaconda.org/conda-forge/uproot)
  - [mplhep](https://anaconda.org/conda-forge/mplhep)


### Dependencies That Come Default with Python

Some of the packages are also packages that come with a default installation of Python. These packages, alongside their documentation, are listed below:
  - [os](https://docs.python.org/3/library/os.html)
  - [re](https://docs.python.org/3/library/re.html)
  - [argparse](https://docs.python.org/3/library/argparse.html)
  - [subprocess](https://docs.python.org/3/library/subprocess.html)
