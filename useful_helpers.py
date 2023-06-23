import os
import numpy as np
import pandas as pd
import uproot
from collections.abc import Iterable

def print_msg_box(msg, indent=1, width=0, title=""):
    """returns message-box with optional title.
    Ripped from https://stackoverflow.com/questions/39969064/how-to-print-a-message-box-in-python
    
    Parameters
    ----------
    msg : str
        The message to use
    indent : int, optional
        indent size, by default 1
    width : int, optional
        box width, by default 0
    title : str, optional
        box title, by default ""
    """
    
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    return box

def recurse_through_folder(folder_path, extension="", verbose=False):
    """_summary_

    Parameters
    ----------
    folder_path : _type_
        _description_
    extension : str, optional
        _description_, by default ""
    verbose : bool, optional
        _description_, by default False

    Returns
    -------
    _type_
        _description_

    Raises
    ------
    FileNotFoundError
        _description_
    """
    folder_path = folder_path.strip()
    
    if not os.path.exists(folder_path):
        msg = print_msg_box(folder_path + "\nDoes Not Exist!", title="ERROR")
        raise FileNotFoundError("\n"+msg)
    
    if folder_path[-1] != '/':
        folder_path += '/'
    
    if extension != "" and extension[0] == ".":
        extension = extension[1:]
    
    paths_in_folder = os.listdir(folder_path)
    folders_wanted = []
    for path in paths_in_folder:
        path = folder_path + path
        if not os.path.isdir(path):
            if (path.split('/')[-1].split(".")[-1] == extension) or (extension == ""):
                folders_wanted.append(path)
            elif verbose:
                print("Looking for", extension.split('/')[-1].split(".")[-1])
                print("ignoring", path, "due to incorrect file extension")
        else:
            folders_wanted += recurse_through_folder(path, extension, verbose)
        
    return folders_wanted

def Unroll_2D_histogram(counts, xbins, ybins, bkg=False):
    """Based off of code written by Jeffrey Davis of happy hour cocktail fame to unroll a 2 dimensional histogram

    Parameters
    ----------
    counts : list[float]
        a list of counts for your 2D histogram in 2D array form
    xbins : list[float]
        the bins for your x dimension
    ybins : list[float]
        the bins for your y dimension
    bkg : bool, optional
        if the sample you are unrolling is a background sample, by default False

    Returns
    -------
    Tuple[ list[float], list[int] ]
        A one dimensional unrolled histogram to be used in any templates you'd like
    """
    integral = np.sum(counts)
    nx, ny = len(xbins), len(ybins)
    filler = integral/(10*nx*ny)
    one_D_counts = np.zeros(nx*ny)
    _, bins = np.histogram([], nx*ny, [0, nx*ny])
    
    indk = 0
    for i, row in enumerate(counts):
        for j, bin_count in enumerate(row):
            if bin_count <= 0 and bkg:
                counts[i][j] = filler
            elif bin_count < 0 and not bkg:
                counts[i][j] = 0
                
            
            one_D_counts[indk] = counts[i][j]
            indk += 1
    
    return one_D_counts, bins

def uproot_ROOTs(filename, keys="all", treeName=None, is_hist=False, output_style='np'):
    if not os.path.isfile(filename):
        errortext = filename + " Not found!"
        raise FileNotFoundError("\n" + print_msg_box(errortext, title="ERROR"))
    
    if output_style not in ['np', 'pd']:
        errortext = "Invalid array style of " + output_style
        errortext += "\n Please select from one of 'np' (numpy) or 'pd' (pandas)"
        raise ValueError("\n" + print_msg_box(errortext, title="ERROR"))
    
    with uproot.open(filename) as root_file:
        if treeName == None:
            treeName = list(root_file.keys())[0]
        elif treeName not in root_file.keys():
            errortext = treeName + " is not a valid ROOT tree name"
            raise KeyError("\n" + print_msg_box(errortext, title="ERROR"))
        
        tree = root_file[treeName]
        
        if is_hist:
            return tree.to_numpy() #histograms are stored directly in a file
        
        if keys == "all":
            keys = list(tree.keys())
        elif not isinstance(keys, Iterable) or isinstance(keys, str):
            errortext = "keys must be an iterable of some kind (that is not a string!), or 'all'!"
            raise TypeError("\n" + print_msg_box(errortext, title="ERROR"))
        else:
            keys = list(keys)
            keys_not_found = []
            for key in keys:
                if key not in tree.keys():
                    keys_not_found.append(key)

            if any(keys_not_found):
                errortext = "The following keys are not in the ROOT Tree: " + treeName + "\n"
                errortext += "\n".join(keys_not_found)
                raise KeyError("\n" + print_msg_box(errortext, title="ERROR"))
            
        return tree.arrays(keys, library=output_style)
        