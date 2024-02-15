import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
from collections.abc import Iterable

plt.style.use(hep.style.ROOT)
mpl.rcParams['axes.labelsize'] = 40
mpl.rcParams['xaxis.labellocation'] = 'center'
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
import warnings
warnings.filterwarnings("ignore")
from matplotlib.ticker import MaxNLocator

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

def ratioPlot(list_of_counts, bins, names=None, reference=0, histtype="step", list_of_count_errors = None, xlabel=None):
    
    if names is not None and len(names) != len(list_of_counts):
        raise ValueError("Names and data should be the same length!")
    
    if list_of_count_errors is not None and len(list_of_count_errors) != len(list_of_counts):
        raise ValueError("Errors and data should be the same length!")
    
    fig, axs = plt.subplots(2,1, figsize=(15,10), facecolor='white', gridspec_kw={'height_ratios': [3, 1], "hspace":0.01}, sharex=True, dpi=200)
    
    axs[0].set_xlim(bins[0], bins[-1])
    
    reference_arr = list_of_counts[reference].copy()
    
    if list_of_count_errors is None:
        reference_err = np.sqrt(reference_arr)
    else:
        reference_err = list_of_count_errors[reference]
    
    color_num = 0
    for n, (data, name) in enumerate(zip(list_of_counts, names)):
        if n != reference:
            color = colors[color_num]
            color_num += 1
        else:
            color = 'black'
        
        hep.histplot(data, bins, label=name, ax=axs[0], histtype=histtype, color=color)
        if list_of_count_errors is None:
            data_err = np.sqrt(data)
        else:
            data_err = list_of_count_errors[n]
        
        ratio = data.copy()/reference_arr
        ratio_error = np.sqrt( (data_err/data)**2 + (data*reference_err/(reference_arr**2))**2)
        
        if n != reference:
            rat_plot = hep.histplot(ratio, bins, color=color, xerr=True, yerr=ratio_error, ax=axs[1], histtype='errorbar')
            plotline, capline, barline = rat_plot[0][0]
            for line in capline:
                line.zorder = plotline.zorder
            for line in barline:
                line.zorder = plotline.zorder
            
        else:
            centers = (bins[1:] + bins[:-1])/2
            xvals = np.linspace(bins[0], bins[-1], len(bins)*100)
            yvals_lower = np.interp(xvals, centers[np.isfinite(ratio_error)], 1 - ratio_error[np.isfinite(ratio_error)])
            yvals_upper = np.interp(xvals, centers[np.isfinite(ratio_error)], 1 + ratio_error[np.isfinite(ratio_error)])
            
            axs[1].fill_between(x=xvals, y1=yvals_lower, y2=yvals_upper, color='k', alpha=0.25, zorder=-np.inf)
            axs[1].plot(xvals, yvals_lower, color='k', zorder=-np.inf)
            axs[1].plot(xvals, yvals_upper, color='k', zorder=-np.inf)
            axs[1].set_ylabel(f"sig/({names[reference]})", fontsize=10)

    if xlabel is not None:
        axs[1].set_xlabel(xlabel)
    axs[0].legend()
    fig.tight_layout()
    return fig, axs