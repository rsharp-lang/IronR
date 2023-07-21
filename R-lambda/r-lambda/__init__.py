
#!/usr/bin/python3

import json 
import os
import sys

from pathlib import Path

def call_lambda(func, 
                argv = None, 
                image = None, 
                run_debug = False):

    # default has no arguments
    if argv is None: argv = {}

    RSCRIPT_HOST   = "/usr/local/bin/Rscript.dll"    
    RSCRIPT_LAMBDA = "--lambda %s --SetDllDirectory /usr/local/bin/"