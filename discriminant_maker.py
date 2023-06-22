import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from collections.abc import Iterable
import MELAcalc
import glob
import contextlib
import uproot
import pandas as pd
import useful_helpers as help

class Discriminant_base(object):
    def __init__(self,
                weights,
                cross_sections,
                gen_weight,
                fname
                ) -> None:
        
        if not isinstance(weights, dict):
            raise TypeError("weights must be a dictionary of arrays!")
        
        self.weights = weights
        self.labels = weights.keys()
        
        if weights.keys() != cross_sections.keys():
            print(weights.keys())
            print(cross_sections.keys())
            raise ValueError("Weights should be the same!")
        
        self.cross_sections = cross_sections
        
        self.c = {}
        for label1 in cross_sections:
            for label2 in cross_sections:
                self.c[(label1, label2)] = cross_sections[label1]/cross_sections[label2]
                
        self.gen = gen_weight
        self.disc_distro = {}
        
        self.fname = fname
    
    def discriminant(self, label1, label2):
            values = self.weights[label1]
            values /= self.weights[label1] + self.weights[label2]*self.c[(label1,label2)]
            
            self.disc_distro[(label1, label2)] = values
            
            return values
    
    def calc_all_discriminants(self):
        for label in self.weights:
            self.discriminant(label)

    def plot(self, labels=[], clear=True, suffix=""):
        if clear:
            plt.cla() #use this if you want to keep previous plots
        
        things_to_iterate_over = labels if labels else self.disc_distro.keys()
        
        for label in things_to_iterate_over:
            counts, bins = np.histogram(self.disc_distro[label], 100, range=[0,1])
            counts = counts.astype(float)
            counts /= np.sum(counts)
            hep.histplot(counts, bins, lw=2, label=str(label[0]))
            
        plt.xlim([0,1])
        plt.legend()
        plt.savefig(self.fname + suffix + ".png")

def get_filename(filepath):
    return filepath.split('/')[-1].replace('ghz1_', '').replace('ghz4_', '').replace('ghz2_', '')


def main(files, MAIN_COUPLING, NATIVE_WEIGHT, output, MELA=True, slice_range = [], suffix=""):
    
    plt.figure()
    plt.cla()
    
    branches = []
    with open("MELAbranches.txt") as f:
        for line in f:
            branches.append(line.strip())
    
    if MELA:
        try:
            for file in files:
                MELAcalc.main(["-i", file, 
                            "-b", "MELAbranches.txt", 
                            "-c", "MELAcouplings.txt", 
                            "-z", "zPrime-3.096900-0.00009_Higgs-6.927",
                            "-o", "/eos/home-m/msrivast/CMSSW_12_2_0_/src/HexUtils/Tetraquark_Analysis",
                            "-ow"])
        except:
            print("yo ho ho")
    
    newfiles = glob.glob("/eos/home-m/msrivast/CMSSW_12_2_0_/src/HexUtils/Tetraquark_Analysis/"+MAIN_COUPLING+"*.*")
    
    crossSections = {
        'ghz1':2.4750465e12,
        'ghz4':8.4858038e06,
        'ghz2':1.7378214e07
    }
    
    # for coupling in ['ghz1', 'ghz2', 'ghz4']:
        
    #     cs_csv = pd.read_csv("/eos/home-m/msrivast/www/data/mass_corrected_fullsim/"+coupling+"/CrossSections.csv")
    #     cs_csv["Filename"] = list(map(get_filename, cs_csv["Filename"]))
    #     cs_csv = cs_csv.set_index("Filename")
    #     cs_csv.columns = list(map(str.strip, cs_csv.columns))
    #     crossSections[coupling] = cs_csv
        
    
    print(crossSections)
    print("{:.2e}".format(crossSections['ghz1']/crossSections['ghz4']))
    with contextlib.ExitStack() as stack:
        files = [
            stack.enter_context(uproot.open(fname)) for fname in newfiles
        ]
        weight_dicts = [file["eventTree"].arrays(branches + ["M4L"], library='pd') for file in files]
        
        filenames = list(map(get_filename, newfiles))
        
        discriminants = {}
        
        for filepath, filename, weight_dict in zip(newfiles, filenames, weight_dicts):
            
            if slice_range:
                weight_dict = weight_dict.query("(M4L > " + str(slice_range[0]) + ") & (M4L < " + str(slice_range[1]) + ")")
        
            weight_dict = weight_dict.drop(columns=["M4L"]).to_dict("list")
            for thing in weight_dict:
                weight_dict[thing] = np.array(weight_dict[thing], dtype=float)
            
            other_cs = {}
            for name in branches:
                coupling = ""
                if 'ghzpzp2' in name:
                    coupling = "ghz2"
                elif 'ghzpzp4' in name:
                    coupling = "ghz4"
                elif "ghzpzp1" in name:
                    coupling = "ghz1"
                    
                other_cs[name] = crossSections[coupling]
            
            # print('\n', "{:.2e}".format(ref_cs), '\n')
            discr_generator = Discriminant_base(
                weight_dict,
                other_cs,
                weight_dict[NATIVE_WEIGHT],
                filename
            )
            
            # discr_generator.discriminant(branches[0], branches[2])
            discr_generator.discriminant(branches[1], branches[0])
            discr_generator.discriminant(branches[2], branches[0])
            # discr_generator.discriminant(branches[1])
            # discr_generator.discriminant(branches[2])
            # discr_generator.plot(clear=True)
            discriminants[filename] = discr_generator
        
        
        NBINS=50
        _, bins = np.histogram([], NBINS, range=[0,1])
        for k in [(branches[1], branches[0]), (branches[2], branches[0])]:
            discr_set = np.empty((len(filenames), NBINS), dtype=float)
            for n, filename in enumerate(discriminants.keys()):
                discr_obj = discriminants[filename].disc_distro[k]
                counts, _ = np.histogram(discr_obj, bins)
                
                discr_set[n] = counts/np.sum(counts)
            plt.cla()
            hep.histplot(np.max(discr_set, axis=0), bins, label="max", histtype="fill", color="red")
            hep.histplot(np.mean(discr_set, axis=0), bins, label="avg", histtype="fill", color="cyan", edgecolor="black", lw=2)
            plt.errorbar((bins[1:] + bins[:-1])/2, np.mean(discr_set, axis=0), fmt='.', yerr=np.std(discr_set, axis=0), color="black")
            hep.histplot(np.min(discr_set, axis=0), bins, label="min", histtype="fill", color="white", edgecolor="cyan")
            plt.legend()
            plt.tight_layout()
            plt.savefig(MAIN_COUPLING+str(k)+suffix+".png")
        
        plt.cla()
        fig, axs = plt.subplots(3,2, figsize=(12,18))
        
        for n, k in enumerate([(branches[1], branches[0]), (branches[2], branches[0])]):
            for filename in discriminants.keys():
                discr_obj = discriminants[filename].disc_distro[k]
                
                plot_ax = []
                if "BW3" in filename or "BW2" in filename:
                    plot_ax.append(2)
                if "BW1" in filename or "BW2" in filename:
                    plot_ax.append(1)
                if "BW1" in filename or "BW3" in filename:
                    plot_ax.append(0)

                counts, _ = np.histogram(discr_obj, bins)
                counts = counts/np.sum(counts)
                # print(filename, "[", plot_ax, ",", n, "]")
                for num in plot_ax:
                    hep.histplot(counts, bins, label=filename, lw=2, ax=axs[num][n])
        
        for row in axs:
            for ax in row:
                ax.legend()
        
        axs[0][0].set_title(r'$D_{0h+}$', fontsize=20)
        axs[0][1].set_title(r'$D_{0-}$', fontsize=20)
        fig.tight_layout()
        fig.savefig(MAIN_COUPLING+"super_test"+suffix+".png")

        return branches, discriminants
    
    
if __name__ == "__main__":
    
    files = glob.glob("/eos/home-m/msrivast/www/data/mass_corrected_fullsim/"+MAIN_COUPLING+"/*.root")
    
    branches, zero_plus = main('ghz1',
    "p_GG_SIG_ghg2_1_ghzpzp1_1_JHUGen_v2",
    False)
    _, zero_minus = main('ghz4',
    "p_GG_SIG_ghg2_1_ghzpzp4_1_JHUGen_v2",
    False)
    
    _, sliced = main('ghz1',
    "p_GG_SIG_ghg2_1_ghzpzp1_1_JHUGen_v2",
    False, [6.638, 6.847], "sliced"
    )
    
    
    plt.figure()
    NBINS=50
    _, bins = np.histogram([], NBINS, range=[0,1])
    for n, k in enumerate([(branches[1], branches[0]), (branches[2], branches[0])]):
        for filename in zero_plus.keys():
            discr_obj_0p = zero_plus[filename].disc_distro[k]
            discr_obj_0m = zero_minus[filename].disc_distro[k]
            
            counts_zero_plus, _ = np.histogram(discr_obj_0p, bins)
            counts_zero_plus = counts_zero_plus.astype(float)
            counts_zero_plus /= np.sum(counts_zero_plus)
            
            counts_zero_minus, _ = np.histogram(discr_obj_0m, bins)
            counts_zero_minus = counts_zero_minus.astype(float)
            counts_zero_minus /= np.sum(counts_zero_minus)
            
            hep.histplot(counts_zero_plus, bins, label="ghz1", lw=2)
            hep.histplot(counts_zero_minus, bins, label="ghz4", lw=2)
            plt.legend()
            plt.title(filename)
            plt.tight_layout()
            if n == 0:
                plt.savefig(filename+"comparison_Dh+.png")
            else:
                plt.savefig(filename+"comparison_D0-.png")
            plt.cla()