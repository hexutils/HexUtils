import os
import re
import argparse

exceptions = {
    '__pycache__',
    'Pdfdata'
}

def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title.
    Ripped from https://stackoverflow.com/questions/39969064/how-to-print-a-message-box-in-python
    Arguments:
        msg -- The message to use

    Keyword Arguments:
        indent -- indent size (default: {1})
        width -- box width (default: {None})
        title -- box title (default: {None})
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
    print(box)

lhe_2_root_options = [
    'vbf',
    'vbf_withdecay',
    'zh',
    'zh_withdecay',
    'zh_lep',
    'zh_lep_hawk',
    'wh_withdecay',
    'wh_lep',
    'wh',
    'ggH4l',
    'ggH4lMG',
    'use-flavor',
    'merge_photon',
    'calc_prodprob',
    'calc_decayprob',
    'CJLST',
    'MELAcalc',
    'reweight-to'
]

parser = argparse.ArgumentParser()
parser.add_argument('argument', type=str,
                    choices=lhe_2_root_options,
                    help="The argument to be passed to LHE2ROOT.py")
parser.add_argument('-c',"--clean", action='store_true',
                    help="remove all produced ROOT files and re-create them")
parser.add_argument('-e','--exceptions', nargs='*',
                    help="Any folder exceptions you want to make to conversion. Useful if you have different argument types for LHE files",
                    default=[])
args = parser.parse_args()

if __name__ == '__main__':

    possible_directories = os.listdir()

    for exception in args.exceptions:
        exceptions.add(exception)
    
    for candidate in possible_directories:
        candidate = os.fsdecode(candidate)
        if (not os.path.isdir(candidate)) or (candidate in exceptions):
            continue
        cross_sections = open(candidate + '/' + "CrossSections.txt", 'w+')
        cross_sections.write('Sample, Cross Section, Uncertainty\n')
        for lhefile in os.listdir(candidate):
            lhefile = os.fsdecode(lhefile)
            
            filename, *extension = lhefile.split('.')
            
            if not ''.join(extension).endswith('lhe'):
                continue
            
            if args.clean:
                if os.path.isfile(candidate + "/" + filename + ".root"):
                    print_msg_box("Removing " + filename + '.root', title="Cleaning directory " + candidate)
                    os.system("rm " + candidate + "/" + filename + ".root")
                
                continue
            
            # print(candidate + '/' + lhefile)

            running_str = "python lhe2root.py --" + args.argument + " " + (candidate + '/LHE_' + filename) + '.root ' + (candidate + '/' + lhefile) + ' > /dev/null'
            titlestr = "Generating ROOT file for " + (candidate + '/' + lhefile)
            
            with open(candidate + '/' + lhefile) as getting_cross_section:
                head = getting_cross_section.read()
                cross_finder = re.compile(r'<init>\n.+\n.+(\d+\.\d+E(\+|-)\d{2})\s+(\d+\.\d+E(\+|-)\d{2})\s+(\d+\.\d+E(\+|-)\d{2})(\d|\s)+</init>')
                cross_section_match = re.search(cross_finder,head)
                cross_sections.write('LHE_'+filename + '.root' + ', ' + cross_section_match.group(1) + ',' + cross_section_match.group(3) + '\n')
            
                print_msg_box("Output name: " + 'LHE_' + filename + '.root' + 
                            "\nArgument: " + args.argument + 
                            "\n\u03C3: " + cross_section_match.group(1) + " \u00b1 " + cross_section_match.group(3),
                            title=titlestr, width=len(titlestr))
            
            os.system(running_str)
        
        cross_sections.close()