import numpy as np
import subprocess
import sys
import os

lhe_2_root_options = [ #these are all the possible mutually exclusive options for lhe2root
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
]
lhe_2_root_args = [ #these are all the other options for lhe2root
    'use-flavor',
    'merge_photon',
    'calc_prodprob',
    'calc_decayprob',
    'CJLST',
    'MELAcalc',
    'reweight-to',
    'verbose'
]

beautified_title = { # a dictionary to beautify your feeble and puny existence. Add or remove depending on what you want.
    'costhetastard':r'$\cos(\theta*)$',
    'Phi1d':r'$\phi_1$',
    'costheta1d':r'$\cos\theta_1$',
    'costheta2d':r'$\cos\theta_2$',
    'Phid':r'$\phi$',
    'MZ1':r'$m_1$' + ' (GeV)',
    'MZ2':r'$m_2$' + ' (GeV)',
    'M4L':r'$m_{4\mu}$' + ' (GeV)'
}

ranges = { #a dictionary of ranges to make your life easier! Add or remove depending on what you want.
    'Phid':[-np.pi, np.pi],
    'Phi1d':[-np.pi, np.pi],
    'costheta1d':[-1,1],
    'costheta2d':[-1,1],
    'costhetastard':[-1,1],
    'M4L':[6,9],
    'MZ1':[3,3.2],
    'MZ2':[3,3.2]
}

def print_msg_box(msg, indent=1, width=0, title=""):
    """Print message-box with optional title.
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
    print(box)
    
def safely_run_process(running_str, env={}):
    """Safely runs a process in the terminal with proper exception handling

    Parameters
    ----------
    running_str : str
        This is the command you are passing to the terminal
    env : dict
            This contains the lhe2root environment variables by doing dict(os.environ) in a main method, by default {}
    """
    try:
        retcode = subprocess.check_call(running_str, shell=True, env=env)
        if retcode < 0:
            print("Child terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print("Command failed:", e, file=sys.stderr)
        
def check_for_MELA(env):
    """A function that checks whether or not you have the environment variables for MELA set up within your terminal

    Parameters
    ----------
    env : dict
        A dictionary of environment variables gotten by doing dict(os.environ) in the main process

    Returns
    -------
    bool
        A boolean as to whether or not MELA is properly set up
    """
    # if "LD_LIBRARY_PATH" not in os.environ: #this library path is set up by the MELA setup script
    #     print("MELA environment variables have not been set up correctly")
    #     if 'HexUtils' in os.getcwd():
    #         print("Run './install.sh' in the directory above HexUtils to set these up!")
    #     else:
    #         print("Run './setup.sh' in the MELA directory to set these up!")
            
    #     return False
    
    # return True

    try:
        env["LD_LIBRARY_PATH"]
        return True
    except:
        if 'HexUtils' in os.getcwd():
            print("Run './install.sh' in the directory above HexUtils to set these up!")
        else:
            print("Run './setup.sh' in the MELA directory to set these up!")
        return False