import uproot
import pandas
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import argparse


beautified_title = { # a dictionary to beautify your feeble existence
    'costhetastard':r'$\cos(\theta*)$',
    'Phi1d':r'$\phi_1$',
    'costheta1d':r'$\cos\theta_1$',
    'costheta2d':r'$\cos\theta_2$',
    'Phid':r'$\phi$',
    'MZ1':r'$m_1$' + ' (GeV)',
    'MZ2':r'$m_2$' + ' (GeV)',
    'M4L':r'$m_{4\mu}$' + ' (GeV)',
    
    'cos_theta_star':r'$\cos\theta*$',
    'phi1':r'$\phi_1$',
    'cos_theta1':r'$\cos\theta_1$',
    'cos_theta2':r'$\cos\theta_2$',
    'phi':r'$\phi$',
    '(cos_theta1|cos_theta2)':r'$\cos\theta_{1,2}$'
}

def ran(s):
    try:
        left, right = map(float, s.split(','))
        return (left, right)
    except:
        raise argparse.ArgumentTypeError("Ranges must be of form 'left, right'!")

mpl.rcParams['axes.labelsize'] = 40
mpl.rcParams['xaxis.labellocation'] = 'center'
plt.style.use(hep.style.ROOT)

parser = argparse.ArgumentParser()

parser.add_argument('filename',nargs='+',
                    help="The file you want to plot")

parser.add_argument('-v','--values',nargs='*',default=['M4L'],
                    help="The attributes you want to plot.")

parser.add_argument('-r','--ranges',nargs='*', default=[(6,9)], type=ran,
                    help='The ranges for your attributes. Enclose your ranges with quotes and a leading space i.e. " -3.14,3.14"')

parser.add_argument('-n', '--nbins', nargs=1, type=int, default=100,
                    help="The number of bins")

parser.add_argument('-l', '--label', nargs=1, type=str, default=None,
                    help="The overall legend label for your plots")

args = parser.parse_args()




if __name__ == "__main__":
    
    if len(args.values) != len(args.ranges):
        raise argparse.ArgumentTypeError("values and ranges must have the same number of entries!")
    
    for file in args.filename:
        if file.split('.')[-1] != 'root':
            raise argparse.ArgumentTypeError("This is not a root file!")
        
        with uproot.open(file) as f:
            keys = f.keys()
            f = f[keys[0]].arrays(library='pd')
            
            for value, range_x in zip(args.values, args.ranges):
                attribute = None
                try:
                    attribute = f[value]
                except:
                    raise argparse.ArgumentTypeError("You can only choose from these attributes:\n" + str(list(f.columns)))
                
                if args.label:
                    plt.hist(attribute, range=range_x, histtype='step', bins=args.nbins, label=args.label, lw=2)
                else:
                    plt.hist(attribute, range=range_x, histtype='step', bins=args.nbins, lw=2)
                plt.xlim(range_x)
                plt.xlabel(beautified_title[value], horizontalalignment='center', fontsize=30)
                plt.tight_layout()
                if args.label:
                    plt.legend()
                plt.show()