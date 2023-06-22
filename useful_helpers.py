import os

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