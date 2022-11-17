import os
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

parser = argparse.ArgumentParser()
parser.add_argument('-c',"--clean", action='store_true')
args = parser.parse_args()

if __name__ == '__main__':

    possible_directories = os.listdir()

    for candidate in possible_directories:
        candidate = os.fsdecode(candidate)
        if (not os.path.isdir(candidate)) or (candidate in exceptions):
            continue
        
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

            running_str = "python lhe2root.py --ggH4l " + (candidate + '/LHE_' + filename) + '.root ' + (candidate + '/' + lhefile) + ' > /dev/null'
            # print(running_str)
            print_msg_box("Generating ROOT file for " + (candidate + '/' + lhefile) + "\nWith name " + 'LHE_' + filename + '.root')
            os.system(running_str)