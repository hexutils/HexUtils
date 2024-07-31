import matplotlib.pyplot as plt
import matplotlib as mpl
import mplhep as hep
import numpy as np
import uproot
import inspect
import warnings
from matplotlib.ticker import MaxNLocator
from typing import Union

def ratioPlot(
    list_of_counts:list, bins:list, names:list=None, reference:int=0, histtype:str="step",
    list_of_count_errors:list=None, lw:Union[float, list]=None,
    xlabel:str=None, colors:list=None, legend_fontsize:float=15,
    xlabel_fontsize:float=20, xtick_labelsize:float=20, ytick_labelsize:float=20,
    reference_color:str='black', include_errors:bool=True, normTo:Union[float, list]=None,
    stack=False, do_not_stack_at:list=None, zorder:list=None, draw_as_line:list=None
    ):

    prop_cycle = [
        "#3f90da",
        "#ffa90e",
        "#bd1f01",
        "#94a4a2",
        "#832db6",
        "#a96b59",
        "#e76300",
        "#b9ac70",
        "#717581",
        "#92dadd",
    ]
    if colors is None:
        colors = prop_cycle
    elif len(colors) != len(list_of_counts) - 1:
        raise ValueError("If providing colors, len(colors)=len(data) - 1 (minus 1 for the reference)!")

    colors.insert(reference, reference_color)

    if names is not None and len(names) != len(list_of_counts):
        raise ValueError("Names and data should be the same length!")
    elif names is None:
        names = [i for i in range(len(list_of_counts))]

    if isinstance(normTo, float) or isinstance(normTo, int):
        normTo = np.full(len(names), normTo, dtype=np.float64)

    if zorder is None:
        zorder = list(range(len(names)))

    if draw_as_line is None:
        draw_as_line = [reference]

    reference_arr = np.copy(list_of_counts[reference])
    reference_arr = reference_arr.astype(float)
    reference_err = np.sqrt(reference_arr)
    if normTo is not None:
        reference_fac = normTo[reference]/reference_arr.sum()
        reference_arr *= reference_fac
        reference_err *= reference_fac

    if list_of_count_errors is not None:
        if len(list_of_count_errors) != len(list_of_counts):
            raise ValueError("Errors and data should be the same length!")
        elif np.any([len(err_lst) != len(count_lst) for err_lst, count_lst in zip(list_of_count_errors, list_of_counts)]):
            raise ValueError("Errors and data should be of the same length!")
        else:
            reference_err = list_of_count_errors[reference]

    if do_not_stack_at is None:
        do_not_stack_at = {reference}
    else:
        do_not_stack_at = set(do_not_stack_at)

    fig, axs = plt.subplots(2,1, figsize=(15,10), facecolor='white', gridspec_kw={'height_ratios': [3, 1], "hspace":0.05}, sharex=True, dpi=200)

    axs[0].set_xlim(bins[0], bins[-1])


    stack_list = []
    for n, (data, name) in enumerate(zip(list_of_counts, names)):
        data = data.astype(float)
        color = colors[n]

        if normTo is not None:
            factor = normTo[n]/data.sum()
            data = data*factor
        else:
            factor = 1

        if stack and n not in do_not_stack_at:
            stack_list.append((data, name, color, zorder[n]))
        elif stack:
            hep.histplot(data, bins, label=name, ax=axs[0], histtype="step", color=color, lw=lw+1, zorder=zorder[n])
        else:
            hep.histplot(data, bins, label=name, ax=axs[0], histtype=histtype, color=color, lw=lw, zorder=zorder[n])

        if list_of_count_errors is None:
            data_err = np.sqrt(data/factor)*factor
        else:
            data_err = list_of_count_errors[n]

        ratio = np.copy(data)/reference_arr
        ratio_error = np.sqrt( (data_err/data)**2 + (data*reference_err/(reference_arr**2))**2)


        if n not in draw_as_line:
            if include_errors:
                rat_plot = hep.histplot(ratio, bins, color=color, xerr=True, yerr=ratio_error, ax=axs[1], histtype='errorbar')
                plotline, capline, barline = rat_plot[0][0]
                for line in capline:
                    line.zorder = plotline.zorder
                for line in barline:
                    line.zorder = plotline.zorder
            else:
                hep.histplot(ratio, bins, color=color, xerr=False, yerr=False, ax=axs[1], histtype='errorbar')

        else:
            centers = (bins[1:] + bins[:-1])/2
            xvals = np.linspace(bins[0], bins[-1], len(bins)*100)
            yvals_lower = np.interp(xvals, centers[np.isfinite(ratio_error)], ratio[np.isfinite(ratio_error)] - ratio_error[np.isfinite(ratio_error)])
            yvals_upper = np.interp(xvals, centers[np.isfinite(ratio_error)], ratio[np.isfinite(ratio_error)] + ratio_error[np.isfinite(ratio_error)])

            axs[1].fill_between(x=xvals, y1=yvals_lower, y2=yvals_upper, color=color, alpha=0.25, zorder=zorder[n])
            axs[1].plot(xvals, yvals_lower, color=color, zorder=zorder[n])
            axs[1].plot(xvals, yvals_upper, color=color, zorder=zorder[n])

    axs[1].set_ylabel(f"Ratio to {names[reference]}", fontsize=20)

    if stack:
        data, name, color, zorder = list(zip(*stack_list))
        ordering = np.argsort(zorder)
        data = [data[i] for i in ordering]
        name = [name[i] for i in ordering]
        color = [color[i] for i in ordering]

        print("total stacked sum:", np.sum([i.sum() for i in data]))

        hep.histplot(data, bins, label=name, ax=axs[0], color=color, histtype=histtype, lw=lw, stack=True)

    if xlabel is not None:
        axs[1].set_xlabel(xlabel, fontsize=xlabel_fontsize)
    axs[0].legend(fontsize=legend_fontsize)
    fig.tight_layout()
    return fig, axs

def plotScan(
    files:Union[str,list], variable:str, variable2:str='deltaNLL',
    label:str=None, x_var_name:str=None, y_var_name:str=None, unit:str=None,
    use_tex_x_axis:bool=False, use_tex_y_axis:bool=False, axis_label_fontsize:int=40,
    min_yval:float=None, max_yval:float=None, min_xval:float=None, max_xval:float=None,
    kill_index:Union[int, list]=None, x_transform=None, y_transform=None, ax:mpl.axes._axes.Axes=None, linestyle= "solid",
    last_step:bool=False, color:str=None, linewidth:float=3, markerstyle:str="",
    margin_mult_x:float=0.95, margin_add_y:float=0.3, legend_loc:str="best", killpoints:bool=False,
    bound_in_name:bool=False, decimal_places:int=1, cmstext:str="Preliminary", lumitext:str=r"138 $fb^{-1}$ (13 TeV)", labelspacing:float=2,
    zorder:int=None, get_confidence_interval:bool=False, output_bounds_as_tex:bool=False,
    include_obs_exp_labels:bool=False, legend_bbox_to_anchor:tuple=(0,0,1,0.95)
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
    x_var_name : str, optional
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

    linestyle_str = {
        'solid': 'solid',      # Same as (0, ()) or '-'
        'dotted': 'dotted',    # Same as (0, (1, 1)) or ':'
        'dashed': 'dashed',    # Same as '--'
        'dashdot': 'dashdot',   # Same as '-.'
        'loosely dotted':        (0, (1, 10)),
        'densely dotted':        (0, (1, 1)),
        'long dash with offset': (5, (10, 3)),
        'loosely dashed':        (0, (5, 10)),
        'densely dashed':        (0, (5, 1)),
        'loosely dashdotted':    (0, (3, 10, 1, 10)),
        'dashdotted':            (0, (3, 5, 1, 5)),
        'densely dashdotted':    (0, (3, 1, 1, 1)),
        'dashdotdotted':         (0, (3, 5, 1, 5, 1, 5)),
        'loosely dashdotdotted': (0, (3, 10, 1, 10, 1, 10)),
        'densely dashdotdotted': (0, (3, 1, 1, 1, 1, 1))
    }

    if isinstance(linestyle, str):
        if linestyle not in linestyle_str.keys():
            print(f"possible choices for line styles are: {' '.join(list(linestyle_str.keys()))}")
            raise KeyError(f"Linestyle {linestyle} not found!")
        linestyle = linestyle_str[linestyle]

    ax.set_autoscale_on(True)
    if x_transform is None:
        pass
    elif not callable(x_transform):
        raise TypeError(f"x_transform must be a function with 1 input!")
    elif len(inspect.signature(x_transform).parameters) != 1:
        raise TypeError(f"x_transform must be a function with 1 input!")

    if y_transform is None:
        pass
    elif not callable(y_transform):
        raise TypeError(f"y_transform must be a function with 1 input!")
    elif len(inspect.signature(y_transform).parameters) != 1:
        raise TypeError(f"y_transform must be a function with 1 input!")

    if ax is None:
        ax = plt.gca()

    data = {}
    if isinstance(files, str):
        files = [files]
    for file in files:
        data_temp = uproot.open(file)['limit'].arrays([variable, variable2], library='np')
        if variable in data.keys():
            data[variable] = np.concatenate( (data[variable], data_temp[variable]) )
            data[variable2] = np.concatenate( (data[variable2], data_temp[variable2]) )
        else:
            data[variable] = data_temp[variable]
            data[variable2] = data_temp[variable2]

    indices = np.argsort(data[variable])

    if x_transform is not None:
        x_data = np.array([x_transform(i) for i in data[variable][indices]])
    else:
        x_data = data[variable][indices]

    if y_transform is not None:
        y_data = np.array([y_transform(i) for i in data[variable2][indices]])
    elif variable2 == 'deltaNLL':
        y_data = 2*data[variable2][indices]
    else:
        y_data = data[variable2][indices]

    minimized_value = np.argmin(y_data)
    convergence_point = x_data[minimized_value]

    if kill_index is not None:
        if isinstance(kill_index, int):
            kill_index = [kill_index]
        kill_index = np.array(kill_index, dtype=int)
        x_data = np.delete(x_data, kill_index)
        y_data = np.delete(y_data, kill_index)
            # print(f"killing index {index}")
    if killpoints == 1:
        i = 1
        while i < len(x_data) - 1:
            if (
                (y_data[i - 1] < y_data[i] and y_data[i + 1] < y_data[i])
                and
                (i != minimized_value)
            ):
                y_data = np.delete(y_data, i)
                x_data = np.delete(x_data, i)
                i = 1
            i += 1
    elif killpoints == 2:
        i = 1
        while i < len(x_data) - 1:
            if (
                (y_data[i - 1] > y_data[i] and y_data[i + 1] > y_data[i])
                and
                (i != minimized_value)
            ):
                y_data = np.delete(y_data, i)
                x_data = np.delete(x_data, i)
                i = 1
            i += 1

    if variable2 == 'deltaNLL' or get_confidence_interval:
        max_point_on_line = max(y_data)
        values_before = (y_data[:minimized_value][::-1], x_data[:minimized_value][::-1])
        values_after =  (y_data[minimized_value:], x_data[minimized_value:])

        do_before = len(values_before[0]) > 0
        do_after = len(values_after[0]) > 0
        uncertainty1 = np.nan
        uncertainty2 = np.nan
        conf1 = np.nan
        conf2 = np.nan

        if max_point_on_line > 1: #1 sigma
            if do_before:
                uncertainty1 = np.abs(
                    convergence_point - np.interp(1, *values_before, left=np.nan, right=np.nan)
                    )

            if do_after:
                uncertainty2 = np.abs(
                    convergence_point - np.interp(1, *values_after, left=np.nan, right=np.nan)
                    )

            if max_point_on_line > 3.84: #2 sigma
                if do_before:
                    conf1 = (
                        np.interp(3.84, *values_before, left=np.nan, right=np.nan)
                        )
                if do_after:
                    conf2 = (
                        np.interp(3.84, *values_after, left=np.nan, right=np.nan)
                        )



    if label is None:
        if x_var_name is None:
            x_var_name = ""
        label = f"${x_var_name.replace('$', '')}={convergence_point:.{decimal_places}f}^{{+{uncertainty2:.{decimal_places}f}}}_{{-{uncertainty1:.{decimal_places}f}}}$"
    elif bound_in_name:
        label += f"(${label.replace('$', '')}={convergence_point:.{decimal_places}f}^{{+{uncertainty2:.{decimal_places}f}}}_{{-{uncertainty1:.{decimal_places}f}}}$)"

    if zorder is None:
        zorder = max([child.zorder for child in ax.get_children()]) + 1
    if color is not None:
        ax.plot(
            x_data,
            y_data,
            lw=linewidth,
            label=label,
            color=color,
            ls=linestyle,
            zorder=zorder,
            marker=markerstyle
        )
    else:
        ax.plot(
            x_data,
            y_data,
            lw=linewidth,
            label=label,
            ls=linestyle,
            zorder=zorder,
            marker=markerstyle
        )

    if last_step:
        ax.margins(0, 0)
        if max_xval is None:
            max_xval = max([max(line.get_xdata()) for line in ax.lines if not np.isnan(line.get_xdata()).all()])
        if min_xval is None:
            min_xval = min([min(line.get_xdata()) for line in ax.lines if not np.isnan(line.get_xdata()).all()])
        ax.set_xlim(min_xval, max_xval)

        if max_yval is None:
            max_yval = max([max(line.get_ydata()) for line in ax.lines if not np.isnan(line.get_ydata()).all()])
        if min_yval is None:
            min_yval = min([min(line.get_ydata()) for line in ax.lines if not np.isnan(line.get_ydata()).all()])
        ax.set_ylim(min_yval, max_yval)

        hep.cms.text(cmstext, ax=ax)
        hep.cms.lumitext(lumitext, ax=ax)

        if variable2 == 'deltaNLL':
            ax.set_ylabel(r"$-2\Delta\ln L$", loc='center', fontsize=axis_label_fontsize, usetex=use_tex_y_axis)
        elif y_var_name is not None:
            ylabel = r'$' + y_var_name.replace('$', '') + r"$"
            ax.set_ylabel(ylabel, fontsize=axis_label_fontsize, loc='center', usetex=use_tex_y_axis)

        if x_var_name is not None:
            xlabel = r'$' + x_var_name.replace('$', '')
            if unit is not None:
                xlabel +="  \mathrm{(" + unit + ")}"
            xlabel += r"$"
            ax.set_xlabel(xlabel, fontsize=axis_label_fontsize, loc='center', usetex=use_tex_x_axis)

        if 1 < max_yval and variable2 == 'deltaNLL': #1 sigma
            ax.axhline(1, ls='dashed', color='black', lw=2, dashes=(8, 5))
            ax.text(max_xval*margin_mult_x, 1+margin_add_y, "68% CL", horizontalalignment="right")
            if 3.84 < max_yval: #2 sigma
                ax.axhline(3.84, ls='dashed', color='black', lw=2, dashes=(8, 5))
                ax.text(max_xval*margin_mult_x, 3.84+margin_add_y, "95% CL", horizontalalignment="right")

        if include_obs_exp_labels:
            ax.plot(np.nan, np.nan, linestyle='solid', color='gray', label='Observed')
            ax.plot(np.nan, np.nan, linestyle='dashed', color='gray', label='Expected')

        ax.legend(loc=legend_loc, labelspacing=labelspacing, bbox_to_anchor=legend_bbox_to_anchor)

        plt.style.use(hep.style.CMS)
        ax.tick_params(axis='both', which='both', labelsize=20, reset=True)
    else:
        if x_var_name is not None:
            print("WARNING: Need to set both last_step and x_var_name to make label!")
    if variable2 == 'deltaNLL' or get_confidence_interval:
        if output_bounds_as_tex:
            tex_str = f"{convergence_point}^{{+{np.abs(uncertainty2)}}}_{{-{np.abs(uncertainty1)}}}"
            tex_str += f"[{conf1} < {variable} < {conf2}]"
            return ax, tex_str

        return ax, (convergence_point, np.abs(convergence_point - uncertainty1), np.abs(convergence_point + uncertainty2), np.abs(convergence_point - conf1), np.abs(convergence_point + conf2))
    else:
        return ax

