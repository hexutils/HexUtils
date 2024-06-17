import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import uproot
import inspect
import warnings
from matplotlib.ticker import MaxNLocator

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

def ratioPlot(list_of_counts, bins, names=None, reference=0, histtype="step", list_of_count_errors = None, xlabel=None):
    plt.style.use(hep.style.CMS)
    mpl.rcParams['axes.labelsize'] = 40
    mpl.rcParams['xaxis.labellocation'] = 'center'
    mpl.rcParams['xtick.labelsize'] = 20
    mpl.rcParams['ytick.labelsize'] = 20
    mpl.rcParams['mathtext.fontset'] = 'stix'
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

def plotScan(
    file:str, variable:str, 
    label:str=None, var_name:str=None, max_yval:float=10, 
    x_transform=None, ax:mpl.axes._axes.Axes=None, dashed:bool=False, 
    last_step:bool=False, color:str=None, linewidth:float=3,
    margin_mult_x:float=0.95, margin_add_y:float=0.3
    ):
    """Plots a scan for you. Run as follows:
    fig = plt.figure()
    plotScan(*parameters*)
    plotScan(*parameters*)
    plotScan(*parameters*, last_step=True)
    fig.savefig(*filename*)

    Parameters
    ----------
    file : str
        The name of the combine ROOT file you are plotting
    variable : str
        The name of the variable on the x axis in the ROOT file
    label : str, optional
        The label on the legend for the line, by default None
    var_name : str, optional
        The label on the x axis (can use LaTeX here), by default None
    max_yval : float, optional
        The maximum y value on the plot, by default 10
    x_transform : function, optional
        A function takes in one variable that transforms the x value so it can be plotted
        (for example, lambda x: x*4.14 when plotting the width), by default None
    ax : matplotlib.axes._axes.Axes, optional
        The axis that you are plotting on. If None, pick the one chosen by plt.gca(), by default None
    dashed : bool, optional
        Whether you would like to plot a dashed line or not, by default False
    last_step : bool, optional
        If set, creates the confidence bound lines as well as the labels/legend.
        Set to true the last time you run the function, by default False
    color : str, optional
        Sets the color of the line. If None, use the default colorscheme, by default None
    linewidth : float, optional
        Sets the width of the plotted lines, by default 3
    margin_mult_x : float, optional
        Sets the multiplier for the x location of the confidence text relative to the last point on the axis,
        by default 0.95
    margin_add_y : float, optional
        Sets the value to be added to 1 and 4 to place the confidence text for the y value,
        by default 0.3

    Returns
    -------
    matplotlib.axes._axes.Axes
        A matplotlib axis with the new plot added

    Raises
    ------
    TypeError
        If x_transform is set improperly, throw an error
    TypeError
        If x_transform is set improperly, throw an error
    """
    if x_transform is None:
        pass
    elif not callable(x_transform):
        raise TypeError(f"x_transform must be a function with 1 input!")
    elif len(inspect.signature(x_transform).parameters) != 1:
        raise TypeError(f"x_transform must be a function with 1 input!")
    
    if ax is None:
        ax = plt.gca()

    data = uproot.open(file)['limit'].arrays([variable, 'deltaNLL'], library='np')
    indices = np.argsort(data[variable])
    
    if x_transform is not None:
        x_data = [x_transform(i) for i in data[variable][indices]]
    else:
        x_data = data[variable][indices]
    y_data = 2*data['deltaNLL'][indices]

    if color is not None:
        ax.plot(
            x_data,
            y_data,
            lw=linewidth,
            label=label,
            color=color,
            ls="dashed" if dashed else "solid"
        )
    else:
        ax.plot(
            x_data,
            y_data,
            lw=linewidth,
            label=label,
            ls="dashed" if dashed else "solid"
        )

    if last_step:
        ax.margins(0, 0)
        max_xval = max(ax.get_xlim())
        ax.set_ylim(0, max_yval)
        hep.cms.text("Preliminary", ax=ax)
        hep.cms.lumitext(r"138 $fb^{-1}$ (13 TeV)")
        ax.set_ylabel(r"-2 $\Delta\ln L$", loc='center', fontsize=30)

        if var_name is not None:
            ax.set_xlabel(var_name, fontsize=40, loc='center')

        ax.axhline(1, ls='dashed', color='black', lw=2, dashes=(8, 5))
        ax.text(max_xval*margin_mult_x, 1+margin_add_y, "68% CL", horizontalalignment="right")
        ax.axhline(4, ls='dashed', color='black', lw=2, dashes=(8, 5))
        ax.text(max_xval*margin_mult_x, 4+margin_add_y, "95% CL", horizontalalignment="right")
        ax.set_xlim(0, max_xval)
        ax.legend()

        plt.style.use(hep.style.CMS)
        ax.tick_params(axis='both', which='both', labelsize=20, reset=True)
        mpl.rcParams['mathtext.fontset'] = 'stix'
    else:
        if var_name is not None:
            print("WARNING: Need to set both last_step and var_name to make label!")

    return ax

