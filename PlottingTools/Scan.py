import abc
import matplotlib.pyplot as plt
import matplotlib as mpl
import mplhep as hep
import numpy as np
import uproot
import inspect
import warnings
from matplotlib.ticker import MaxNLocator
from typing import Union, Callable

conf_bounds_1d = {
    65 : 1,
    95 : 3.84
}

conf_bounds_2d = {
    65 : 2.3,
    95 : 5.99
}

class Scan(abc.ABC):
    def __init__(
        self,
        x_transform:Callable=None,
        y_transform:Callable=None,
        axis=None
    ):
        if axis is None:
            self.ax = plt.gca()
        else:
            self.ax = axis

        #https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
        self.linestyles = {
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
        #https://cms-analysis.docs.cern.ch/guidelines/plotting/colors/#categorical-data-eg-1d-stackplots
        self.prop_cycle = [
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

        self.n_lines = 0
        self.scans = {}
        self.x_transform = x_transform
        self.y_transform = y_transform
        self.likelihood_plot = False #if deltaNLL is the second variable

        if self.x_transform is None:
            pass
        elif not callable(self.x_transform):
            raise TypeError(f"x_transform must be a function with 1 input!")
        elif len(inspect.signature(self.x_transform).parameters) != 1:
            raise TypeError(f"x_transform must be a function with 1 input!")

        if self.y_transform is None:
            pass
        elif not callable(self.y_transform):
            raise TypeError(f"y_transform must be a function with 1 input!")
        elif len(inspect.signature(self.y_transform).parameters) != 1:
            raise TypeError(f"y_transform must be a function with 1 input!")

    def plot(self):
        return NotImplemented

    def save(
        self,
        fpath:str,
        tight_layout:bool=True,
        ):
        fig = self.ax.get_figure()
        if tight_layout:
            fig.tight_layout()
        fig.savefig(f"{fpath}.png")
        fig.savefig(f"{fpath}.pdf")
        fig.savefig(f"{fpath}.svg")
        print(f"Saved file at {fpath}.{{png,pdf,svg}}")



class Scan1D(Scan):
    def __init__(
        self,
        x_transform:Callable=None,
        y_transform:Callable=None,
        axis=None,
    ):
        super().__init__(axis, x_transform, y_transform)

    def addScan(
        self,
        files:Union[str, list],
        label:str,
        x:str, y:str="deltaNLL",
        branch_name:str="limit",
        kill_index:Union[int, list]=None,
        kill_points:bool=False,
        color:str=None,
        line_style:str="solid",
        line_width:float=2,
        marker_style:str="",
        zorder:int=None,
    ):
        if isinstance(line_style, str):
            if line_style not in self.linestyles.keys():
                print(
                    f"possible choices for line styles are: {' '.join(list(self.linestyles.keys()))}"
                )
                raise KeyError(f"line_style {line_style} not found!")
            line_style = self.linestyles[line_style]

        if y == "deltaNLL":
            self.likelihood_plot = True

        data = {}
        if isinstance(files, str):
            files = (files, )
            #turn into tuple to make life easier

        for file in files:
            data_temp = uproot.open(file)[branch_name].arrays(
                [x, y], library='np'
            )
            if x in data.keys():
                data[x] = np.concatenate( (data[x], data_temp[x]) )
                data[y] = np.concatenate( (data[y], data_temp[y]) )
            else:
                data[x] = data_temp[x]
                data[y] = data_temp[y]
        del data_temp

        indices = np.argsort(data[x])
        if self.x_transform is not None:
            x_data = np.array(
                [self.x_transform(i) for i in data[x][indices]]
            )
        else:
            x_data = data[x][indices]

        if self.y_transform is not None:
            y_data = np.array(
                [self.y_transform(i) for i in data[y][indices]]
            )
        elif y == 'deltaNLL': #this is a fun special case
            y_data = 2*data[y][indices]
        else:
            y_data = data[y][indices]

        minimized_value = np.argmin(y_data)
        convergence_point = x_data[minimized_value]

        if kill_index is not None:
            if isinstance(kill_index, int):
                kill_index = [kill_index]
            kill_index = np.array(kill_index, dtype=int)
            x_data = np.delete(x_data, kill_index)
            y_data = np.delete(y_data, kill_index)

        if kill_points:
            i = 1
            while i < len(x_data) - 1:
                if (
                    (y_data[i - 1] < y_data[i] and y_data[i + 1] < y_data[i])
                    and
                    (i != minimized_value)
                ):
                    y_data = np.delete(y_data, i)
                    x_data = np.delete(x_data, i)
                    minimized_value = np.argmin(y_data)
                    convergence_point = x_data[minimized_value]
                    i = 1
                    continue
                i += 1

        data[x] = x_data
        data[y] = y_data


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

        if zorder is None:
            zorder = max([child.zorder for child in ax.get_children()]) + 1
        if color is None:
            color = self.prop_cycle[self.n_lines]
        self.ax.plot(
            x_data,
            y_data,
            lw=line_width,
            label=label,
            color=color,
            ls=line_style,
            zorder=zorder,
            marker=marker_style
        )

        self.n_lines += 1
        self.scans[label] = (
            (
                convergence_point,
                np.abs(convergence_point - uncertainty1),
                np.abs(convergence_point + uncertainty2),
                np.abs(convergence_point - conf1),
                np.abs(convergence_point + conf2)
            ),
            data
        )

    def plot(
        self,
        x_axis_title:str="",
        y_axis_title:str="",
        unit:str="",
        axis_label_fontsize:float=40,
        min_yval:float=None, max_yval:float=None,
        min_xval:float=None, max_xval:float=None,
        margin_mult_x:float=0.95, margin_add_y:float=0.3,
        margin_add_y_65:float=None, margin_add_y_95:float=None,
        legend_loc:str="best", legend_fontsize:float=12,
        labelspacing:float=2, legend_bbox_to_anchor:tuple=(0,0,1,0.95),
        cmstext:str="Preliminary", lumitext:str=r"138 $fb^{-1}$ (13 TeV)",
        cmstext_size:float=None, lumitext_size:float=None,
        tick_size:float=20, tick_pad:float=10
    ):
        if margin_add_y_65 is None:
            margin_add_y_65 = margin_add_y
        if margin_add_y_95 is None:
            margin_add_y_95 = margin_add_y

        self.ax.margins(0, 0)
        if max_xval is None:
            max_xval = max([max(line.get_xdata()) for line in self.ax.lines if not np.isnan(line.get_xdata()).all()])
        if min_xval is None:
            min_xval = min([min(line.get_xdata()) for line in self.ax.lines if not np.isnan(line.get_xdata()).all()])
        self.ax.set_xlim(min_xval, max_xval)

        if max_yval is None:
            max_yval = max([max(line.get_ydata()) for line in self.ax.lines if not np.isnan(line.get_ydata()).all()])
        if min_yval is None:
            min_yval = min([min(line.get_ydata()) for line in self.ax.lines if not np.isnan(line.get_ydata()).all()])
        self.ax.set_ylim(min_yval, max_yval)

        if cmstext_size is None:
            hep.cms.text(cmstext, ax=self.ax)
        else:
            hep.cms.text(cmstext, ax=self.ax, fontsize=cmstext_size)

        if lumitext_size is None:
            hep.cms.lumitext(lumitext, ax=self.ax)
        else:
            hep.cms.lumitext(lumitext, ax=self.ax, fontsize=lumitext_size)

        if self.likelihood_plot:
            self.ax.set_ylabel(r"$-2$ $\Delta\ln L$", loc='center', fontsize=axis_label_fontsize)
        else:
            ylabel = r'$' + y_axis_title.replace('$', '') + r"$"
            self.ax.set_ylabel(ylabel, fontsize=axis_label_fontsize, loc='center')

        xlabel = r'$' + x_axis_title.replace('$', '')
        xlabel += r"$"
        if unit != "":
            xlabel +="  (" + unit + ")"
        self.ax.set_xlabel(xlabel, fontsize=axis_label_fontsize, loc='center')

        if 1 < max_yval and self.likelihood_plot: #1 sigma
            self.ax.axhline(1, ls="dashed", color='black', lw=1, dashes=(16, 10))
            self.ax.text(max_xval*margin_mult_x, 1+margin_add_y_65, "68% CL", horizontalalignment="right")
            if 3.84 < max_yval: #2 sigma
                self.ax.axhline(3.84, ls="dashed", color='black', lw=1, dashes=(16, 10))
                self.ax.text(max_xval*margin_mult_x, 3.84+margin_add_y_95, "95% CL", horizontalalignment="right")

        self.ax.legend(loc=legend_loc, labelspacing=labelspacing, bbox_to_anchor=legend_bbox_to_anchor, fontsize=legend_fontsize)

        # plt.style.use(hep.style.CMS)
        self.ax.tick_params(axis='both', which='both', labelsize=tick_size, pad=tick_pad, reset=True)

    def GetBounds(self, variable_name, as_tex=False, decimals:int=3):
        if as_tex:
            returnable = []
            for name, ((central, lower, upper, lower_conf, upper_conf), _) in self.scans.items():
                tex_str = f"{central}^{{+{np.abs(upper)}}}_{{-{np.abs(lower)}}}"
                tex_str += f"[{lower_conf} < {variable_name} < {upper_conf}]"
                returnable.append(tex_str)
            returnable = "\n".join(returnable)
        else:
            returnable = {}
            for name, ((central, lower, upper, lower_conf, upper_conf), _) in self.scans.items():
                returnable[name] = {
                    "central":central,
                    "lower_bound":lower,
                    "upper_bound":upper,
                    "lower_confidence":lower_conf,
                    "upper_confidence":upper_conf
                }

        return returnable

class Scan2D(Scan):

    def __init__(
        self,
        files:Union[str, list],
        x:str, y:str, z:str="deltaNLL",
        branch_name:str="limit",
        x_transform: Callable = None,
        y_transform: Callable = None,
        z_transform: Callable = None,
        kill_index:Union[int, list]=None,
        axis=None
    ):
        super().__init__(x_transform, y_transform, axis)

        self.z_transform = z_transform

        if self.z_transform is None:
            pass
        elif not callable(self.z_transform):
            raise TypeError(f"y_transform must be a function with 1 input!")
        elif len(inspect.signature(self.z_transform).parameters) != 1:
            raise TypeError(f"y_transform must be a function with 1 input!")

        if z == "deltaNLL":
            self.likelihood_plot = True

        data = {}
        if isinstance(files, str):
            files = (files, )
            #turn into tuple to make life easier

        for file in files:
            data_temp = uproot.open(file)[branch_name].arrays(
                [x, y, z], library='np'
            )
            if x in data.keys():
                data[x] = np.concatenate( (data[x], data_temp[x]) )
                data[y] = np.concatenate( (data[y], data_temp[y]) )
                data[z] = np.concatenate( (data[z], data_temp[z]) )
            else:
                data[x] = data_temp[x]
                data[y] = data_temp[y]
                data[z] = data_temp[z]
        del data_temp

        if self.x_transform is not None:
            x_data = np.array(
                [self.x_transform(i) for i in data[x]]
            )
        else:
            x_data = data[x]

        if self.y_transform is not None:
            y_data = np.array(
                [self.y_transform(i) for i in data[y]]
            )
        else:
            y_data = data[y]

        if self.z_transform is not None:
            z_data = np.array(
                [self.z_transform(i) for i in data[z]]
            )
        elif z == 'deltaNLL': #this is a fun special case
            z_data = 2*data[z]
            warnings.warn("Multiplying deltaNLL by 2 by default")
        else:
            z_data = data[z]

        minimized_value = np.argmin(z_data)
        convergence_point = (x_data[minimized_value], y_data[minimized_value])

        if kill_index is not None:
            if isinstance(kill_index, int):
                kill_index = [kill_index]
            kill_index = np.array(kill_index, dtype=int)
            x_data = np.delete(x_data, kill_index)
            y_data = np.delete(y_data, kill_index)
            z_data = np.delete(z_data, kill_index)

        data[x] = x_data
        data[y] = y_data
        data[z] = z_data

        self.x = x
        self.y = y
        self.z = z

        self.scans = (
            convergence_point,
            data
        )


    def add_contour(
        self,
        level,
        line_style,
        label,
        line_color:str="k",
        line_width:float=3,
    ):

        if isinstance(line_style, str):
            if line_style not in self.linestyles.keys():
                print(
                    f"possible choices for line styles are: {' '.join(list(self.linestyles.keys()))}"
                )
                raise KeyError(f"line_style {line_style} not found!")
            line_style = self.linestyles[line_style]

        self.ax.tricontour(
            self.scans[1][self.x], self.scans[1][self.y],
            self.scans[1][self.z],
            levels=[level],
            linewidths=[line_width],
            colors=[line_color],
            linestyles=[line_style]
        )
        #for the legend
        plt.plot([], linestyle=line_style, color=line_color, label=label)


    def add_point(
        self,
        x_value,
        y_value,
        name,
        marker,
        color,
        size:float=200
    ):
        self.ax.scatter(
            x_value, y_value,
            marker=marker,
            color=color,
            label=name,
            s=size
        )

    def add_best_fit(
        self,
        marker:str="P",
        color:str="k",
        size:float=200,
        name:str="Best Fit"
    ):
        self.add_point(
            *self.scans[0],
            name,
            marker,
            color,
            size
            )

    def plot(
        self,
        cmap:mpl.colors.Colormap=None,
        cmap_min:float=None,
        cmap_max:float=None,
        shading:str="gouraud",
        norm=None,
        colorbar_pad:float=0.025,
        colorbar_labelPad:float=10,
        colorbar_integer:bool=True,

        x_axis_title:str=None,
        y_axis_title:str=None,
        z_axis_title:str=None,
        axis_label_fontsize:float=40,
        min_yval:float=None, max_yval:float=None,
        min_xval:float=None, max_xval:float=None,
        legend_loc:str="best", legend_fontsize:float=28,
        labelspacing:float=2, legend_bbox_to_anchor:tuple=(0,0,1,0.95),
        cmstext:str="Preliminary", lumitext:str=r"138 $fb^{-1}$ (13 TeV)",
        cmstext_size:float=None, lumitext_size:float=None,
        tick_size:float=20, tick_pad:float=10
    ):
        if cmap is None:
            lvTmp = np.linspace(0.25,1.0,1000)
            cmTmp = mpl.cm.viridis(lvTmp)
            cmap = mpl.colors.ListedColormap(cmTmp)

        if cmap_min is None:
            cmap_min = np.min(self.scans[1][self.z])
        if cmap_max is None:
            cmap_max = np.max(self.scans[1][self.z])

        if x_axis_title is None:
            x_axis_title = self.x
        if y_axis_title is None:
            y_axis_title = self.y
        if z_axis_title is None:
            z_axis_title = self.z

        tpc = self.ax.tripcolor(
            self.scans[1][self.x], self.scans[1][self.y],
            self.scans[1][self.z],
            shading=shading,
            cmap=cmap,
            vmin=cmap_min,
            vmax=cmap_max,
            norm=norm,
            zorder=-np.inf
        )

        cbar = plt.colorbar(tpc, pad=colorbar_pad, extendrect=True)
        cbar.ax.get_yaxis().labelpad = colorbar_labelPad

        if self.likelihood_plot:
            cbar.ax.set_ylabel(r'$-2$ $\Delta\ln L$', rotation=90, loc="center", fontsize=axis_label_fontsize)
        else:
            cbar.ax.set_ylabel(z_axis_title, rotation=90, loc="center", fontsize=axis_label_fontsize)

        cbar.locator = MaxNLocator(integer=colorbar_integer)

        self.ax.margins(0, 0)
        if max_xval is None:
            max_xval = np.max(self.scans[1][self.x])
        if min_xval is None:
            min_xval = np.min(self.scans[1][self.x])
        self.ax.set_xlim(min_xval, max_xval)

        if max_yval is None:
            max_yval = np.max(self.scans[1][self.y])
        if min_yval is None:
            min_yval = np.min(self.scans[1][self.y])
        self.ax.set_ylim(min_yval, max_yval)

        if cmstext_size is None:
            hep.cms.text(cmstext, ax=self.ax)
        else:
            hep.cms.text(cmstext, ax=self.ax, fontsize=cmstext_size)

        if lumitext_size is None:
            hep.cms.lumitext(lumitext, ax=self.ax)
        else:
            hep.cms.lumitext(lumitext, ax=self.ax, fontsize=lumitext_size)

        self.ax.set_ylabel(y_axis_title, fontsize=axis_label_fontsize, loc='center')

        self.ax.set_xlabel(x_axis_title, fontsize=axis_label_fontsize, loc='center')

        self.ax.legend(loc=legend_loc, labelspacing=labelspacing, bbox_to_anchor=legend_bbox_to_anchor, fontsize=legend_fontsize)

        # plt.style.use(hep.style.CMS)
        self.ax.tick_params(axis='both', which='both', labelsize=tick_size, pad=tick_pad, reset=True)
