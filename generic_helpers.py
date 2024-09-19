import os
import argparse
from collections.abc import Iterable
import numpy as np
import vector

def negative_part(array):
    array = np.array(array)
    return np.minimum(array, 0)

def positive_part(array):
    array = np.array(array)
    return np.maximum(array, 0)

def check_all_zero(array):
    array = np.array(array)
    return not np.any(array)

def check_one_nonzero(array):
    array = np.array(array)
    return np.any(array)

def check_nan_inf(array):
    array = np.array(array)
    return np.any( ~np.isfinite(array) )

def nan_to_value(array, value=0):
    array = np.array(array)
    array[~np.isfinite(array)] = value
    return array

def argparse_filepath_type(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"The path {path} is invalid!")
    else:
        return path

def get_spatial(four_vector):
    """Takes in a 4 vector and returns its spatial component. Identical to TLorentzVector.Vect()

    Parameters
    ----------
    four_vector : vector.array
        A 4 vector from the vector class

    Returns
    -------
    vector.array
        A 3 vector from the vector class
    """
    return vector.array(
        {
            "x":four_vector.x,
            "y":four_vector.y,
            "z":four_vector.z
        }
    )

def MELA_simpleParticle_toVector(simpleParticle):
    id = simpleParticle.id
    vec = simpleParticle.PxPyPzE_vector
    return id, vector.obj(px=vec[0], py=vec[1], pz=vec[2], E=vec[3])

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

def make_legend_label_hist(counts, bins, name, extra_space=True):
    x = (bins[1:]+bins[:-1])/2
    
    if x.shape != counts.shape:
        errortext = "Shapes do not match!"
        errortext += "\nx.shape != counts.shape"
        errortext += "\n"+str(x.shape)+"!="+str(counts.shape)
        raise ValueError("\n" + print_msg_box(errortext, title="ERROR"))
    
    avg = np.average(x, weights=counts)
    
    
    labelstr = name+"\n"
    labelstr += "Area={:.3f}\n".format(np.sum(counts))
    labelstr += r'$\mu=$' + "{:.2f}\n".format(avg)
    labelstr += r'$\sigma=$' + "{:.2f}".format(np.sqrt(np.average( (x - avg)**2, weights=counts )))
    if extra_space:
        labelstr += "\n"
    
    return labelstr

def make_legend_label(data, name, extra_space=True):
    avg = np.average(data)
    labelstr = name+"\n"
    labelstr += "N={:.0f}\n".format(len(data))
    labelstr += r'$\mu=$' + "{:.2f}\n".format(avg)
    labelstr += r'$\sigma=$' + "{:.2f}".format(np.std(data))
    if extra_space:
        labelstr += "\n"
    
    return labelstr

def scale(scaleto, counts, bins=None, return_scale_factor=False):
    """This function scales histograms according to their absolute area under the curve

    Parameters
    ----------
    scaleto : float
        The absolute area to scale to
    counts : list[Union[int,float]]
        A list of bin counts
    bins : list[float]
        The bins you want to use; use this option if you are passing a numpy histogram in (i.e. scale(1, *<numpy histogram>)), by default None
    return_scale_factor : bool
        Whether the scale factor being used will be returned
    
    Returns
    -------
    list[float] OR Tuple(list[float], list[float]) OR Tuple(list[float], float) OR Tuple(list[float], list[float], float)
        The scaled histogram bin counts or the scaled histogram, depending on whether you passed the bins in as well
    """
    counts = np.array(counts)
    counts = counts.astype(float)
    signs = np.sign(counts) #makes sure to preserve sign
    counts = np.abs(counts)
    
    if (scaleto == 0) or (np.sum(counts) == 0):
        return np.zeros(counts.shape)
    
    new_counts = signs*counts*scaleto/np.sum(counts)
    new_counts[~np.isfinite(new_counts)] = 0
    if bins is not None:
        if return_scale_factor:
            return new_counts, bins, scaleto/np.sum(counts)
        
        return new_counts, bins
    
    elif return_scale_factor:
        return new_counts, scaleto/np.sum(counts)
    
    return new_counts

def unroll_ND_histogram(N_dimension_counts, isbkg=False):
    unrolled_arr = N_dimension_counts.ravel()
    if isbkg:
        hist_integral = unrolled_arr.sum()
        fill_val = hist_integral*0.1/len(unrolled_arr)
        unrolled_arr[unrolled_arr <= 0] = fill_val

    pos_arr = np.where(unrolled_arr > 0, unrolled_arr, 0)
    neg_arr = -1*np.where(unrolled_arr < 0, unrolled_arr, 0)
    
    bins = np.arange(len(unrolled_arr) + 1)

    return (pos_arr, neg_arr), bins

def binary_search_on_array(
    array,
    upper_index,
    lower_index,
    target,
    search_function=None):
    """This is a simple function that conducts a binary search on an array
    You can give it a custom search function if you'd like

    Parameters
    ----------
    array : numpy.ndarray
        This is the array you are searching on. It should be sorted in descending order
    upper_index : int
        The upper index you are starting from
    lower_index : int
        The lower index you are starting from
    target : any
        This is what you are looking for
        NOTE: Some binary searches don't utilize targets (if you are looking for c constants for discriminants, for instance)
    search_function : function, optional
        This is a custom search function. If not provided, use the default, by default None

    Returns
    -------
    int
        The index that is found

    Raises
    ------
    ValueError
        The search function must return -1, 0, or 1
    """
    
    index = (upper_index + lower_index)//2
    if search_function == None:
        
        def search(index, array, target): #generate a default search function that works for arrays
            val = array[index]
            if val == target:
                return 0
            elif val < target:
                return 1
            elif val > target:
                return -1
            
        search_function = search
    
    was_it_found = search_function(index, array, target)
    
    if upper_index == lower_index or was_it_found== 0 or upper_index == lower_index + 1:
        return index
    
    if was_it_found == -1: #This should mean that the target is somewhere below the current index
        upper_index = index
    elif was_it_found == 1: #This should mean that the target is somewhere above the current index
        lower_index = index
    else:
        errortext = print_msg_box("Search function should return 0, 1, or -1!", title="ERROR")
        raise ValueError("\n"+errortext)
    
    return binary_search_on_array(
        array,
        upper_index,
        lower_index,
        target,
        search_function)

def find_discr_c_constant(
    w1_1,
    w1_2,
    w2_1,
    w2_2,
    guess=None,
    statistics_limit=0,
    debug=False):
    """This function looks for a calibrated c constant for a given discriminant

    Parameters
    ----------
    w1_1 : numpy.ndarray
        The probabilities for hypothesis 1 from a sample generated with hypothesis 1
    w1_2 : numpy.ndarray
        The probabilities for hypothesis 2 from a sample generated with hypothesis 1
    w2_1 : numpy.ndarray
        The probabilities for hypothesis 1 from a sample generated with hypothesis 2
    w2_2 : numpy.ndarray
        The probabilities for hypothesis 2 from a sample generated with hypothesis 2
    guess : float, optional
        This is a guess for an initial c constant to make sure there is some crossing point. 
        If None, one will be made for you, by default None
    statistics_limit : int, optional
        This is a limiter for the minimum number of events you want in a calculation, by default 0
    """
    def search_function(index, array, target):
        fraction1 = np.sum(array[0][:index])/np.sum(array[0])
        fraction2 = np.sum(array[1][index:])/np.sum(array[1])
        
        fraction1 = np.round(fraction1, 3)
        fraction2 = np.round(fraction2, 3)
        
        if debug:
            print(fraction1, fraction2)
        
        if fraction1 == fraction2:
            if debug:
                print("found!")
                print()
            return 0
        elif fraction1 < fraction2:
            if debug:
                print("moving up!")
                print()
            return 1
        elif fraction1 > fraction2:
            if debug:
                print("moving down!")
                print()
            return -1
        else:
            print(fraction1, array[0])
            print(fraction2, array[1])
            raise ValueError("What the hell is going on!?")
    
    w1_1 = np.array(w1_1, float)
    w1_2 = np.array(w1_2, float)
    
    w2_1 = np.array(w2_1, float)
    w2_2 = np.array(w2_2, float)
    
    if (not np.any(w1_1)) or (not np.any(w2_1)): #If all the elements are 0 then the fit has failed
        return "FAILED"
    
    if not guess:
        guess = np.mean(w1_1)/np.mean(w1_2)
    
    _, bins = np.histogram([], bins=100000, range=[0,1])
    
    values_1, _ = np.histogram(1/(1 + guess*(w1_2/w1_1)), bins=bins)
    values_2, _ = np.histogram(1/(1 + guess*(w2_2/w2_1)), bins=bins)
    
    if (np.sum(values_1) <= statistics_limit) or (np.sum(values_2) <= statistics_limit):
        return "FAILED"
    
    values_1 = scale(1, values_1)
    values_2 = scale(1, values_2)
    
    searchable = np.vstack((values_1, values_2))
    
    crossing = binary_search_on_array(
        searchable,
        len(bins) - 1,
        0,
        0.5,
        search_function
    )
    
    centers = (bins[1:] + bins[:-1])/2
    
    R = centers[crossing]
    
    c_constant = guess/( (1/R) - 1)
    
    return c_constant
