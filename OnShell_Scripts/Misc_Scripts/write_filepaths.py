import os 
import sys
from glob import glob
PATH = sys.argv[1]
OUTFILE = sys.argv[2]
result = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.root'))]

with open(OUTFILE, 'w') as f:
    for filename in result:
        path = os.getcwd()+"/"+filename
        f.write("%s\n" % path)
