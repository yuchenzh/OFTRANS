from pathlib import Path
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from oftrans import OFTrans
import sys

# help information
if (sys.argv[1] == '--help'):
    print("Usage: python main.py <mech_file> <version>")
    print("mech_file: the path to the mechanism file")
    print("version: the version of OpenFOAM. Default is 7, optional")
    # quit
    sys.exit()

# if the length of argument is 2, the second one is the version
version = 7
if (len(sys.argv) > 2):
    version = sys.argv[2]
    
oftrans = OFTrans(sys.argv[1])
oftrans.getSutherlandParams()
oftrans(version)