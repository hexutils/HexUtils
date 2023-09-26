import os
import re
import uproot
import pandas as pd
import numpy as np
import mplhep as hep
import useful_funcs_and_constants
import lhe_reader
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings

plt.style.use(hep.style.ROOT)
mpl.rcParams['axes.labelsize'] = 40
mpl.rcParams['xaxis.labellocation'] = 'center'

def scale(scaleto, counts, bins=[]):
    """This function scales histograms according to their absolute area under the curve (no negatives allowed!)

    Parameters
    ----------
    scaleto : float
        The absolute area to scale to
    counts : list[Union[int,float]]
        A list of bin counts
    bins : list[float]
        The bins you want to use; use this option if you are passing a numpy histogram in, by default []
    Returns
    -------
    list[float]
        The scaled histogram
    """
    counts = counts.astype(float)
    signs = np.sign(counts) #makes sure to preserve sign
    counts = np.abs(counts)
    
    if any(bins):
        return signs*counts*scaleto/np.sum(counts), bins
    
    return signs*counts*scaleto/np.sum(counts)


def recursively_convert(env, current_directory, output_directory, argument, other_args=[], clean=False, verbose=False, exceptions=set(), 
                        outfile_prefix='LHE', cut_down_to=-1, write=""):
    """This function will recurse through every directory and subdirectory in the place you call it, 
    and attempt to convert those files to ROOT files using lhe2root

    Parameters
    ----------
    env : dict
        This contains the lhe2root environment variables by doing dict(os.environ) in a main method
    current_directory : str
        The directory to start recursing downwards from
    output_directory : str
        The directory to output results to
    argument : str
        the lhe2root conversion option to use (see lhe_2_root_options in useful_funcs_and_constants)
    other_args : list[str]
        The other lhe2root arguments that can be used (see lhe_2_root_args in useful_funcs_and_constants), by default []
    clean : bool, optional
        If True, this function will wipe any old conversion and re-convert the files, by default False
    verbose : bool, optional
        If true, the function will be verbose, by default False
    exceptions : set, optional
        Any absolute path with this string in it will be ignored, by default set()
        NOTE: This is the case for any string in the path! folders of path <exception>/<other folder> will be ignored
        The same goes for folders where a substring of the folder matches the name in the exception - useful for catching multiple folders!
        Name your folders carefully!
    outfile_prefix : str, optional
        The prefix to attach to the generated ROOT files, by default "LHE"
    cut_down_to : int, optional
        The number of events you want in the LHE file before converting. Negative numbers mean all events will be kept, by default -1
    write : str, optional
        If a string, this will be the file that you will write the cross sections to. The file will be comma-separated, by default ""

    Returns
    -------
    dict
        Returns a dictionary with the cross section/uncertainty pairs for every file

    Raises
    ------
    FileNotFoundError
        If the output directory is not found/not a directory raises an error
    """
    if output_directory[-1] != '/':
        output_directory += '/'
    
    if not os.path.isdir(output_directory):
        raise FileNotFoundError(output_directory + " is not a directory!")
    
    cross_sections = {}
    
    for candidate in os.listdir(current_directory):
        # print(candidate)
        candidate = os.fsdecode(candidate)
        
        candidate = current_directory + '/' + candidate
        # print(candidate)
        
        is_exempt = False
        for exemption in exceptions: #check all the exempted folders
            if exemption in candidate: #if the keyword is ANYWHERE in the file path, ignore it!
                is_exempt = True
        
        
        if (os.path.isdir(candidate)) and (not is_exempt): #convert all the LHE files in every directory below you that are not exempt
            one_folder_below = recursively_convert(env, candidate, output_directory, argument, other_args, clean, verbose, exceptions)
            cross_sections.update(one_folder_below) #updates the dictionary
        
        if candidate.split('.')[-1] != 'lhe':
        #     if clean and candidate.split['.'][-1] == '.root':
        #         useful_funcs_and_constants.print_msg_box("Removing " + candidate, title="Cleaning directory " + current_directory)
        #         os.remove(candidate)
                
            continue
        
        else:            
            reader = lhe_reader.lhe_reader(candidate)
            cut_down_filename = candidate.split('.')[0] + "_cut_down_to" + str(cut_down_to) + '.lhe'
            if cut_down_to > 0 and not os.path.isfile(candidate.split('.')[0] + "_cut_down_to" + str(cut_down_to) + '.lhe'):
                candidate = cut_down_filename
                if verbose:
                    print("Cutting down file to", cut_down_to, "events in file", candidate)
                
                with open(candidate, 'w+') as f:
                    f.write(reader.cut_down_to_size(cut_down_to))
                
                reader = lhe_reader.lhe_reader(candidate)#reset the reader and the candidate to the new cut down file
                
            outfile = reader.to_ROOT(argument, env, other_args, output_directory, outfile_prefix, verbose, clean)
            cross_sections[outfile] = reader.cross_section
    
    if write:
        print("Dumping Cross Sections to", output_directory + write)
        with open(output_directory + write, "w+") as f:
            f.write("Filename, Cross Section, Uncertainty\n")
            for fname, (crosssection, uncertainty) in cross_sections.items():
                f.write(fname + ', ' + "{:e}".format(crosssection) + ', ' + "{:e}".format(uncertainty) + '\n')
                
    return cross_sections



def plot_one_quantity(filenames, attribute, xrange, nbins=100, labels=[], norm=False, title="", 
                      cuts={}, perFile=False):
    """This function plots one quantity of your choice from ROOT files!

    Parameters
    ----------
    filenames : list[str]
        The ROOT files you are plotting from
    attribute : str
        The TBranch you are plotting (the files should have the same names for branches)
    xrange : tuple[float, float]
        The range for your x axis for this attribute
    nbins : int, optional
        The number of bins. This can either be a number or a list, by default 100
    labels : list, optional
        The labels for each file plotted, by default []
    norm : bool, optional
        Whether to normalize the plotting areas to 1 for easier comparison, by default False
    title : str, optional
        An extra "title" on the x label that is concatenated, by default ""
    cuts : dict
        A dictionary containing the upper and lower level cuts that you are making on each quantity, by default {}
    perFile : bool
        Whether you want to have a single plot for each file, by default False
        
    Returns
    -------
    dict
        A dictionary of NumPy style histogram tuple of counts and bins with the filename as the key

    Raises
    ------
    ValueError
        If your list of labels and list of filenames are not the same length
    ValueError
        If you choose a column that is undefined
    """
    if labels and len(labels) != len(filenames):
        raise ValueError("labels and files should be the same length!")
    
    histograms = {}
    
    for n, file in enumerate(filenames):
        with uproot.open(file) as f:
            keys = f.keys()
            f = f[keys[0]].arrays(library='pd')
            
            try:
                for quan, cut in cuts.items():
                    # print(cut)
                    # print(f.query(quan + ' > @cut[0]'))
                    f = f.query(quan + ' > @cut[0] & ' + quan + ' < @cut[1]')
                value = f[attribute]
            except:
                raise ValueError("You can only choose from these attributes:\n" + str(list(f.columns)))
            
            hist_counts, hist_bins = np.histogram(value, range=xrange, bins=nbins)
            
            histograms[file] = (hist_counts, hist_bins)
            
            if norm:
                hist_counts = scale(1, hist_counts)
                
            if labels:
                hep.histplot(hist_counts, hist_bins, lw=2, label=labels[n])
            else:
                hep.histplot(hist_counts, hist_bins, lw=2)
                
            plt.xlim(xrange)
            
            if attribute in useful_funcs_and_constants.beautified_title:
                plt.xlabel(useful_funcs_and_constants.beautified_title[attribute] + title, horizontalalignment='center', fontsize=30)
            else:
                plt.xlabel(attribute + title, horizontalalignment='center', fontsize=30)
        
        if perFile:
            if labels:
                plt.legend()
            plt.tight_layout()
            file = file.split('/')[-1].split('.')[0]
            plt.savefig(attribute + "_" + file + '.png')
            plt.cla()
    
    if not perFile:            
        if labels:
            plt.legend()
            
        plt.tight_layout()
        plt.savefig(attribute + '.png')
    
    return histograms


def plot_interference(mixed_file, pure1, pure2, pure1Name, pure2Name, attribute, cross_sections, nbins=100, title=""):
    """Plots the interference between two samples given a file containing a mixture of the two, and two "pure" samples

    Parameters
    ----------
    mixed_file : str
        The ROOT file containing a simulation of pure1 and pure2 together
    pure1 : str
        ROOT file for one of the two items (no mixing)
    pure2 : str
        ROOT file for the other of the two items (no mixing)
    pure1Name : str
        The name for what this sample is called
    pure2Name : str
        The name for what this sample is called
    attribute : str
        The thing you are plotting (i.e. M4L, phi, etc.)
    cross_sections : dict
        A dictionary containing the cross sections of each file in the following format: {filename: cross section}
    nbins : int, optional
        The number of bins for your plot. This can either be an integer or a list of bins, by default 100
    title : str, optional
        An extra "title" on the x label that is concatenated, by default ""

    Returns
    -------
    Tuple(numpy.array)
        The interference portion between the three plots
        
    Raises
    ------
    ValueError
        If there is a column listed that is not found
    """
    
    mixed_file = os.path.abspath(mixed_file)
    pure1 = os.path.abspath(pure1)
    pure2 = os.path.abspath(pure2)
    
    interf_sample = BW1_sample = BW2_sample = pd.DataFrame()
    
    with uproot.open(mixed_file) as interf: #Opening all of these in the same statement might cause memory issues. So here we are!
        interf_sample = interf[interf.keys()[0]].arrays(library='pd')
        
    if attribute not in interf_sample.columns:
        raise ValueError(attribute + " not in file!")
        
    with uproot.open(pure1) as rawBW1:
        BW1_sample = rawBW1[rawBW1.keys()[0]].arrays(library='pd')
        
    with uproot.open(pure2) as rawBW2:
        BW2_sample = rawBW2[rawBW2.keys()[0]].arrays(library='pd')
        
    
    interf_hist, bins = np.histogram(interf_sample[attribute], range=useful_funcs_and_constants.ranges[attribute], bins=nbins) #edit these ranges to your heart's desire!
    BW1_hist, _ = np.histogram(BW1_sample[attribute], range=useful_funcs_and_constants.ranges[attribute], bins=bins)
    BW2_hist, _ = np.histogram(BW2_sample[attribute], range=useful_funcs_and_constants.ranges[attribute], bins=bins)
    
    # print('%E' % CrossSections[pure1][0], '%E' % CrossSections[pure2][0], '%E' % np.sqrt(CrossSections[pure1][0]*CrossSections[pure2][0])
    #     , '%E' % CrossSections[mixed_file][0])
    
    interf_hist = scale(cross_sections[mixed_file], interf_hist)
    BW1_hist = scale(cross_sections[pure1], BW1_hist)
    BW2_hist = scale(cross_sections[pure2], BW2_hist)
    
    interf_actual = interf_hist - BW1_hist - BW2_hist
    
    plt.figure()
    plt.gca().axhline(lw=3, linestyle='--', color='black', zorder=0)
    
    hep.histplot(BW1_hist, bins, label=pure1Name, lw=2)
    hep.histplot(BW2_hist, bins, label=pure2Name, lw=2)
    hep.histplot(interf_hist, bins, label=pure1Name + '/' + pure2Name, lw=2)
    # print(interf_hist)
    
    hep.histplot(interf_actual, bins, label=pure1Name + '/' + pure2Name + ' Interference', lw=2)
    plt.xlabel(useful_funcs_and_constants.beautified_title[attribute] + " " + title, horizontalalignment='center', fontsize=20)
    plt.xlim(useful_funcs_and_constants.ranges[attribute])
    plt.legend()
    plt.tight_layout()
    plt.savefig('Interference_between_2.png')
    # plt.show()
    
    return interf_actual, bins


def cut_ranges_to_dict(cut_ranges):
    """Takes in cut ranges of triples of style <name>, <upper bound>, <lower bound>
    singular plotting can use. Styled such that a dot indicates that there is no cut.

    Parameters
    ----------
    cut_ranges : list[list[Union[str, float]]]
        the list of triples generated by args.cut

    Returns
    -------
    dict
        A dictionary of style <cut name>: (<upper bound>, <lower bound>)
    """
    cut_dict = {}
    for key, lower, upper in cut_ranges:
        if lower == '.':
            lower = -np.inf
        if upper == '.':
            upper = np.inf
        
        cut_dict[key] = (lower, upper)
    
    return cut_dict