import os
from collections.abc import Iterable
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import vector
import functools
import tqdm
import matplotlib.cm as cm
# import ROOT

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

def Freedman_Diaconis(data, lower=None, upper=None, only_bins=False):
    """https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule

    Parameters
    ----------
    data : _type_
        _description_
    """
    if lower == None:
        lower = data.min()
    if upper == None:
        upper = data.max()
    
    data = data[(data > lower) & (data < upper)]
    
    iqr = np.subtract(*np.percentile(data, [75, 25])) #the interquartile range
    width = 2*iqr/np.cbrt(len(data))
    
    bins = np.arange(lower, upper+width, width)
    
    if only_bins:
        return width, bins
    
    return width, np.histogram(data, bins, range=[lower, upper])

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


def make_legend_label_hist(bins, counts, name, extra_space=True):
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


def Unroll_ND_histogram(counts, *bins, bkg=False):
    counts = np.array(counts)
    integral = np.sum(counts)
    super_bin_count = 1
    for bin in bins:
        super_bin_count *= len(bin)
    
    filler = integral/(10*super_bin_count)
    one_D_counts = np.zeros(super_bin_count)
    _, bins = np.histogram([], super_bin_count, [0, super_bin_count])
    indk = 0
    for index, bin_count in np.ndenumerate(counts):
        fillable_value = bin_count
        if bin_count <= 0 and bkg:
            fillable_value = filler
        elif bin_count < 0 and not bkg:
            fillable_value = 0
        
        one_D_counts[indk] = fillable_value
        indk += 1
    
    return one_D_counts, bins

def uproot_ROOTs(filename, keys="all", treeName=None, is_hist=False, output_style='np'):
    import pandas as pd
    import uproot
    
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

def scale(scaleto, counts, bins=[], return_scale_factor=False):
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
    if any(bins):
        if return_scale_factor:
            return new_counts, bins, scaleto/np.sum(counts)
        
        return new_counts, bins
    
    elif return_scale_factor:
        return new_counts, scaleto/np.sum(counts)
    
    return new_counts


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

class angle_calculator(object):
    def __init__(self, pt, eta, phi, m, id, needStack=False,
                 name_override={}, range_override={}):
        
        pt, eta, phi, m, id = list(map(np.array, [pt, eta, phi, m, id]))

        if needStack:
            pt = np.stack(pt, axis=0)
            eta = np.stack(eta, axis=0)
            phi = np.stack(phi, axis=0)
            m = np.stack(m, axis=0)
            id = np.stack(id, axis=0)
            
        self.lep_1 = vector.array(
            {
                "pt":pt[:,0],
                "phi":phi[:,0],
                "eta":eta[:,0],
                "M":m[:,0]
            }
        )
        self.lep_1_id = id[:,0]
        
        self.lep_2 = vector.array(
            {
                "pt":pt[:,1],
                "phi":phi[:,1],
                "eta":eta[:,1],
                "M":m[:,1]
            }
        )
        self.lep_2_id = id[:,1]
        
        self.lep_3 = vector.array(
            {
                "pt":pt[:,2],
                "phi":phi[:,2],
                "eta":eta[:,2],
                "M":m[:,2]
            }
        )
        self.lep_3_id = id[:,2]
        
        self.lep_4 = vector.array(
            {
                "pt":pt[:,3],
                "phi":phi[:,3],
                "eta":eta[:,3],
                "M":m[:,3]
            }
        )
        self.lep_4_id = id[:,3]
        
        
        Z1_sort_mask = (
            (self.lep_2_id!=-9000)
            &
            (
                (#for OS pairs, lep1 is the particle.
                    (self.lep_1_id*self.lep_2_id<0)
                    & 
                    (self.lep_1_id<0) 
                )
                |
                ( #for SS pairs, a random deterministic convention is used.
                    (
                        (self.lep_1_id*self.lep_2_id>0)
                        |
                        (
                            (self.lep_1_id==0) 
                            & 
                            (self.lep_2_id==0)
                        )
                    )
                    &
                    (self.lep_1.phi <= self.lep_2.phi)
                )
            )
        )
        np.where(Z1_sort_mask, self.lep_2, self.lep_1) #swap leptons if the mask is true
        self.Z1 = self.lep_1 + self.lep_2
        
        
        Z2_sort_mask = (
            (self.lep_4_id!=-9000)
            &
            (
                (#for OS pairs, lep1 is the particle.
                    (self.lep_3_id*self.lep_4_id<0)
                    & 
                    (self.lep_3_id<0) 
                )
                |
                ( #for SS pairs, a random deterministic convention is used.
                    (
                        (self.lep_3_id*self.lep_4_id>0)
                        |
                        (
                            (self.lep_3_id==0) 
                            & 
                            (self.lep_4_id==0)
                        )
                    )
                    &
                    (self.lep_3.phi <= self.lep_4.phi)
                )
            )
        )
        np.where(Z2_sort_mask, self.lep_4, self.lep_3) #swap leptons if the mask is true
        self.Z2 = self.lep_3 + self.lep_4
        
        self.X = self.Z1 + self.Z2
        
        
        self.quantities = {
            "costhetastar":r'$\cos \theta^*$',
            "costheta1":r'$\cos \theta_1$',
            "costheta2":r'$\cos \theta_2$',
            "phi":r'$\phi$',
            "phi1":r'$\phi_1$',
            "pt":r'$p_T(X)$',
            "px":r'$p_x(X)$',
            "py":r'$p_y(X)$',
            "pz":r'$p_z(X)$',
        }
        
        self.ranges = {
            "costhetastar":(-1,1),
            "costheta1":(-1,1),
            "costheta2":(-1,1),
            "phi":(-np.pi, np.pi),
            "phi1":(-np.pi, np.pi),
            "pt":None,
            "px":None,
            "py":None,
            "pz":None,
        }
        
        for i in name_override.keys():
            if i not in self.quantities.keys():
                errortext = i + " not a quantity!"
                errortext += "\nQuantities are the following:\n"
                errortext += "\n".join(list(self.quantities.keys()))
                errortext = print_msg_box(errortext, title="ERROR")
                raise KeyError("\n" + errortext)
            self.quantities[i] = name_override[i]
        
        for i in range_override.keys():
            if i not in self.quantities.keys():
                errortext = i + " not a quantity!"
                errortext += "\nQuantities are the following:\n"
                errortext += "\n".join(list(self.quantities.keys()))
                errortext = print_msg_box(errortext, title="ERROR")
                raise KeyError("\n" + errortext)
            self.ranges[i] = range_override[i]
        
        plt.cla()
    
    @classmethod
    def from_xyz_leptons(cls, 
                         x1, y1, z1, e1, id1,
                         x2, y2, z2, e2, id2,
                         x3, y3, z3, e3, id3,
                         x4, y4, z4, e4, id4,
                         name_override={}, range_override={}):
        lepton1 = vector.array(
            {
                "px":x1,
                "py":y1,
                "pz":z1,
                "E":e1
            }
        )

        lepton2 = vector.array(
            {
                "px":x2,
                "py":y2,
                "pz":z2,
                "E":e2
            }
        )
        
        lepton3 = vector.array(
            {
                "px":x3,
                "py":y3,
                "pz":z3,
                "E":e3
            }
        )
        
        lepton4 = vector.array(
            {
                "px":x4,
                "py":y4,
                "pz":z4,
                "E":e4
            }
        )
        
        pt_array = np.stack(
            [
                lepton1.pt,
                lepton2.pt,
                lepton3.pt,
                lepton4.pt
            ], axis=1
        )
        
        phi_array = np.stack(
            [
                lepton1.phi,
                lepton2.phi,
                lepton3.phi,
                lepton4.phi
            ], axis=1
        )
        
        eta_array = np.stack(
            [
                lepton1.eta,
                lepton2.eta,
                lepton3.eta,
                lepton4.eta
            ], axis=1
        )
        
        m_array = np.stack(
            [
                lepton1.M,
                lepton2.M,
                lepton3.M,
                lepton4.M
            ], axis=1
        )
        
        
        id_array = np.stack(
            [
                id1,
                id2,
                id3,
                id4
            ], axis=1
        )
        
        return cls(
            pt_array, eta_array, phi_array, m_array, id_array,
            name_override=name_override, range_override=range_override
        )
    
    @functools.cached_property
    def costhetastar(self):
        boost_x = -self.X.to_beta3() #to_beta3 is equivalent to ROOT's TLorentzVector BoostVector
        Z1_in_x_frame = self.Z1.boost(boost_x)
        # Z2_in_x_frame = self.Z2.boost(boost_x)
        Z1_in_x_frame = get_spatial(Z1_in_x_frame)
        cos_theta_star = Z1_in_x_frame.z/Z1_in_x_frame.mag
        
        return cos_theta_star
    
    @functools.cached_property 
    def costheta1(self):
        boost_v1 = -1*self.Z1.to_beta3()
        np.where(boost_v1.mag>=1, boost_v1*0.9999/boost_v1.mag, boost_v1)
        
        l1_boosted = self.lep_1.boost(boost_v1)
        l3_boosted = self.lep_3.boost(boost_v1)
        l4_boosted = self.lep_4.boost(boost_v1)
        
        v2_boosted = l3_boosted + l4_boosted
        
        v2_boosted = get_spatial(v2_boosted)
        
        l1_boosted = get_spatial(l1_boosted)
        
        cos_theta_1 = -1*v2_boosted.unit().dot(l1_boosted.unit())
        
        cos_theta_1 = np.where(np.abs(self.lep_1_id)!=21, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_2_id)!=21, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_3_id)!=21, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_4_id)!=21, cos_theta_1, 0)
        
        cos_theta_1 = np.where(np.abs(self.lep_1_id)!=22, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_2_id)!=22, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_3_id)!=22, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_4_id)!=22, cos_theta_1, 0)
        
        return cos_theta_1
    
    @functools.cached_property 
    def costheta2(self):
        boost_v2 = -1*self.Z2.to_beta3()
        
        l1_boosted = self.lep_1.boost(boost_v2)
        l2_boosted = self.lep_2.boost(boost_v2)
        l3_boosted = self.lep_3.boost(boost_v2)
        
        v1_boosted = l1_boosted + l2_boosted
        
        v1_boosted = get_spatial(v1_boosted)
        
        l3_boosted = get_spatial(l3_boosted)
        
        cos_theta_2 = -1*v1_boosted.unit().dot(l3_boosted.unit())
        
        cos_theta_2 = np.where(np.abs(self.lep_1_id)!=21, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_2_id)!=21, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_3_id)!=21, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_4_id)!=21, cos_theta_2, 0)
        
        cos_theta_2 = np.where(np.abs(self.lep_1_id)!=22, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_2_id)!=22, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_3_id)!=22, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_4_id)!=22, cos_theta_2, 0)
        
        return cos_theta_2
    
    @functools.cached_property 
    def phi(self):
        boost_x = -1*self.X.to_beta3()
        l1_boosted = self.lep_1.boost(boost_x)
        l2_boosted = self.lep_2.boost(boost_x)
        l3_boosted = self.lep_3.boost(boost_x)
        l4_boosted = self.lep_4.boost(boost_x)
        
        v1_boosted = get_spatial(l1_boosted + l2_boosted).unit()
        
        normal_1_boosted = (get_spatial(l1_boosted).cross(get_spatial(l2_boosted))).unit()
        normal_2_boosted = (get_spatial(l3_boosted).cross(get_spatial(l4_boosted))).unit()
        
        temp_sign_phi = v1_boosted.dot(normal_1_boosted.cross(normal_2_boosted))
        sign_phi = np.where(np.abs(temp_sign_phi)>0,temp_sign_phi/np.abs(temp_sign_phi), 0)
        
        dot_boosted = normal_1_boosted.dot(normal_2_boosted)
        dot_boosted = np.where(np.abs(dot_boosted) >= 1, dot_boosted/np.abs(dot_boosted), dot_boosted)
        
        phi = sign_phi*np.arccos(-1*dot_boosted)
        
        return phi
    
    @functools.cached_property
    def phi1(self):
        boost_x = -1*self.X.to_beta3()
        l1_boosted = self.lep_1.boost(boost_x)
        l2_boosted = self.lep_2.boost(boost_x)
        
        v1_boosted = get_spatial(l1_boosted + l2_boosted).unit()
        
        beam_axis = vector.array([(0,0,1)], dtype=[("x", float), ("y", float), ("z", float)])

        normal_1_boosted = (get_spatial(l1_boosted).cross(get_spatial(l2_boosted))).unit()
        normal_SC_boosted = (beam_axis.cross(v1_boosted)).unit()
        
        temp_sign_phi = v1_boosted.dot(normal_1_boosted.cross(normal_SC_boosted))
        sign_phi = np.where(np.abs(temp_sign_phi)>0,temp_sign_phi/np.abs(temp_sign_phi), 0)
        
        dot_boosted = normal_1_boosted.dot(normal_SC_boosted)
        dot_boosted = np.where(np.abs(dot_boosted) >= 1, dot_boosted/np.abs(dot_boosted), dot_boosted)
        
        phi1 = sign_phi*np.arccos(dot_boosted)
        
        return phi1
    
    @functools.cached_property
    def pT_X(self):
        return self.X.pt
    
    @functools.cached_property
    def pz_X(self):
        return self.X.pz
    
    @functools.cached_property
    def py_X(self):
        return self.X.py
    
    @functools.cached_property
    def px_X(self):
        return self.X.px
    
    
    def plot_quantity(self, quantity, fname, bins=20, clear_after=True, save=True, identifier="", norm=False,
                      abs=False, ax=None, color=None, fontsize=10, spacer=True, lw=2, loc='upper right',
                      show_stats=True, noplot=False, fig=None):
        import matplotlib as mpl
        plt.style.use(hep.style.ROOT)
        mpl.rcParams['axes.labelsize'] = 40
        mpl.rcParams['xaxis.labellocation'] = 'center'
        quantity = quantity.lower()
        
        if quantity not in self.quantities.keys():
            errortext = quantity + " not defined as a quantity in self.quantities!"
            errortext += "\nUse the name_override keyword to define quanties not predefined!"
            errortext += "self.quantities:\n "
            errortext += "\n".join(list(self.quantities.keys()))
            errortext = print_msg_box(errortext, title="ERROR")
            raise KeyError("\n"+errortext)
        
        if quantity not in self.ranges.keys():
            errortext = quantity + " not defined as a quantity in self.ranges!"
            errortext += "\nUse the range_override keyword to define ranges not predefined!"
            errortext += "self.ranges:\n "
            errortext += "\n".join(self.ranges.keys())
            errortext = print_msg_box(errortext, title="ERROR")
            raise KeyError("\n"+errortext)

        
        conversion = {
            "costhetastar":self.costhetastar,
            "costheta1":self.costheta1,
            "costheta2":self.costheta2,
            "phi":self.phi,
            "phi1":self.phi1,
            "pt":self.pT_X,
            "px":self.px_X,
            "py":self.py_X,
            "pz":self.pz_X
        }
        
        if abs:
            values = np.abs(conversion[quantity])
        else:
            values = conversion[quantity]
        
        
        if self.ranges[quantity] == None:
                variable_range = [values.min(), values.max()]
                
        else:
            variable_range = self.ranges[quantity]
        
        if isinstance(bins, int):
            _, bins = np.histogram([], bins, range=variable_range)
            
        

        hist, bins = np.histogram(values, bins=bins)
        hist = hist.astype(float)
        if norm:
            hist = scale(norm, hist)
        
        if identifier == "":
            identifier = self.quantities[quantity]
        
        if show_stats:
            labelstr = make_legend_label_hist(bins, hist, identifier, extra_space=spacer)
        else:
            labelstr = identifier
        
        if noplot:
            return hist, bins, labelstr
        
        if ax == None:
            ax = plt.gca()
        
        if color:
            hep.histplot(hist, bins, label=labelstr, lw=lw, ax=ax, color=color)
        else:
            hep.histplot(hist, bins, label=labelstr, lw=lw, ax=ax,)
        
        ax.set_xlabel(self.quantities[quantity])
        ax.legend(loc=loc, fontsize=fontsize)
        ax.set_xlim(variable_range)
        
        if fig == None:
            fig = plt.gcf()
        
        fig.tight_layout()
        if save:
            fig.savefig(fname)
        if clear_after:
            plt.cla()
            plt.close(fig)
            
        return hist, bins, labelstr


def merge_bins(counts, bins, target=0, ab_val=True, drop_first=False):
    """Merges a set of bins that are given based off of the counts provided
    Eliminates any bin with a corresponding count that is less than the target
    Useful to do merge_bins(*np.histogram(data), ...)
    
    
    Parameters
    ----------
    counts : numpy.ndarray
        The counts of a histogram
    bins : numpy.ndarray
        The bins of a histogram
    target : int, optional
        The target value to achieve - any counts below this will be merged, by default 0
    ab_val : bool, optional
        If on, the target will consider the absolute value of the counts, not the actual value, by default True
    drop_first : bool, optional
        If on, the function will not automatically include the first bin edge, by default False

    Returns
    -------
    Tuple(numpy.ndarray, numpy.ndarray)
        A np.histogram object with the bins and counts merged

    Raises
    ------
    ValueError
        If the bins and counts are not sized properly the function will fail
    """
    
    if len(bins) != len(counts) + 1:
        errortext = "Length of bins is {:.0f}, length of counts is {:.0f}".format(len(bins), len(counts))
        errortext = "\nlen(bins) should be len(counts) + 1!"
        raise ValueError("\n" + print_msg_box(errortext, title="ERROR"))
    
    new_counts = []
    if not drop_first:
        new_bins = [bins[0]] #the first bin edge is included automatically if not explicitly stated otherwise
    else:
        new_bins = []
        
    if ab_val:
        counts = np.abs(counts)
    
    
    i = 0
    while i < len(counts):
        start = i
        summation = 0
        while (summation <= target) and (i < len(counts)):
            summation += counts[i]
            i += 1
        end = i
        
        if drop_first and len(new_bins) == 0:
                first_bin = max(end - 1, 0)
                new_bins += [bins[first_bin]]
                
        if not( (summation <= target) and (end == len(counts)) ):
            new_counts += [np.sum(counts[start:end])]
            new_bins += [bins[end]]
        else:
            new_counts[-1] += np.sum(counts[start:end])
            new_bins[-1] = bins[end]
            
    return np.array(new_counts), np.array(new_bins)

def merge_bins_2d(data_x, data_y, counts_2d, bins_x, bins_y, 
                  target_x=0, target_y=0,
                  merge_x=True, merge_y=True):
    
    if (not merge_x) and (not merge_y):
        errortext = "Function is merging nothing!\nBoth merge_x and merge_y set to False"
        raise ValueError("\n"+print_msg_box(errortext, title="ERROR"))
    
    if merge_x:
        counts_x = np.sum(counts_2d, axis=1)
        _, new_bins_x = merge_bins(counts_x, bins_x, target_x)
    else:
        new_bins_x = bins_x.copy()
    
    if merge_y:
        counts_y = np.sum(counts_2d, axis=0)
        _, new_bins_y = merge_bins(counts_y, bins_y, target_y)
    else:
        new_bins_y = bins_y.copy()
    
    return np.histogram2d(data_x, data_y, [new_bins_x, new_bins_y])

def ROC_curve(sample1, sample2, bins=100, lower=0, upper=1):
    """This function produces a ROC curve from an attribute like phi, cos(theta1), D_{0-}, etc.

    Parameters
    ----------
    sample1 : numpy.ndarray
        The first data sample for your attribute. This is your "True" data
    sample2 : numpy.ndarray
        The second data sample for your attribute. This if your "False" data
    bins : int or numpy.ndarray, optional
        The number of bins for the ROC calculation. Can also be given a list of bins., by default 100
    lower : float
        The lower end of your sample range
    upper : float
        The upper end of your sample range
    

    Returns
    -------
    tuple(numpy.ndarray, numpy.ndarray, float)
        returns the true rate, the false rate, and the area under the curve (assuming true rate is the x value)
    """
    
    sample1 = np.array(sample1)
    sample2 = np.array(sample2)
    
    if isinstance(bins, int):
        _, bins = np.histogram([], bins=bins, range=[lower, upper])
    
    hypo2_counts, bins = merge_bins(*scale(1, *np.histogram(sample2, bins=bins)))
    hypo1_counts, _ = scale(1, *np.histogram(sample1, bins=bins))
    
    # print(list(g1_phi_counts))
    # print()
    # print(list(g4_phi_counts))
    
    ratios = sorted(
        list(enumerate(hypo1_counts/hypo2_counts)), key=lambda x: x[1], reverse=True
    )
    # print(ratios)
    ratios = np.array(ratios)[:,0].astype(int) #gets the bin indices only for the ordered ratio pairs
    ratios = nan_to_value(ratios)
    # print(ratios)
    # print()
    length = len(ratios) + 1
    
    PAC = np.zeros(length) #"positive" above cutoff
    PBC = np.zeros(length) #"positive" below cutoff
    NAC = np.zeros(length) #"negative" above cutoff
    NBC = np.zeros(length) #"negative" below cutoff
    
    
    for n in range(length):
        above_cutoff = ratios[n:]
        below_cutoff = ratios[:n]
        
        PAC[n] = hypo1_counts[above_cutoff].sum() #gets the indices listed
        PBC[n] = hypo1_counts[below_cutoff].sum()
        
        NAC[n] = hypo2_counts[above_cutoff].sum()
        NBC[n] = hypo2_counts[below_cutoff].sum()
        
        # for bin_index in above_cutoff: #The above lines are the same as this commented code but vectorized
        #     PAC += g1_phi_counts[bin_index]
        #     NAC += g4_phi_counts[bin_index]
        
        # for bin_index in below_cutoff:
        #     PBC += g1_phi_counts[bin_index]
        #     NBC += g4_phi_counts[bin_index]
        # TPR.append(1 - PAC/(PAC + PBC))
        # FPR.append(1 - NAC/(NAC + NBC))
        
        
    TPR = 1 - PAC/(PAC + PBC) #vectorized calculation
    FPR = 1 - NAC/(NAC + NBC)
    
    TPR = nan_to_value(TPR)
    FPR = nan_to_value(FPR)
    
    return TPR, FPR, np.trapz(TPR, FPR)

def plot_2d_histogram_with_projection(counts, binsx, binsy, xlabel, ylabel, fname=""):
    fig = plt.figure(figsize=(12,12))
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left+width+0.05 #bottom of the top histogram and the left of the right histogram
    
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h+0.04, bottom, 0.15, height]
    
    # add the axes to the figure
    ax2d = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    # nullfmt = NullFormatter()
    # axHistx.xaxis.set_major_formatter(nullfmt)
    # axHisty.yaxis.set_major_formatter(nullfmt)
    
    hep.hist2dplot(counts, binsx, binsy, ax=ax2d, cmap=cm.coolwarm, cbarpos="right", cbarpad=0)
    ax2d.set_xlabel(xlabel, fontsize=40, loc='center')
    ax2d.set_ylabel(ylabel, fontsize=40, loc='center')
    # fig.colorbar(ax2d)
    
    hep.histplot(np.sum(counts, axis=1), binsx, ax=axHistx, color='black', lw=3)
    axHistx.set_xlim(ax2d.get_xlim()) # x-limits match the 2D plot
    
    hep.histplot(np.sum(counts, axis=0), binsy, ax=axHisty, orientation="horizontal", lw=3)
    axHisty.set_ylim(ax2d.get_ylim())
    
    fig.savefig(fname)