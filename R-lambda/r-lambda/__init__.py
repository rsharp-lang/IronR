
#!/usr/bin/python3

import json 
import os
import sys

from pathlib import Path

def docker_image(id, volumn = [], name = None):
    """A helper function for create the docker argument

    Keyword arguments:
    id -- required, the docker image id to run the application 
    volumn -- optional, the volumn names to mapping from the physical file system to 
        the docker internal file system
    name -- optional, the name that specific to the running container, 
        default value none means no name was specific.
    """

    return {
        "image": id,
        "volumn": volumn,
        "name": name
    }

def call_lambda(func, 
                argv = None, 
                options = None,
                workdir = "./",
                image = None, 
                run_debug = False):
    """A helper function for run a R# function from the commandline
    
    Keyword arguments:
    func -- required, the target R# function name to run, should be in format 
        like: pkg_name::function_name
    argv -- optional, the function parameters of the target R# function, default none 
        means target function not required of parameters.
    options -- optional, the R# runtime environment options, this parameter value will
        take effects of the ``getOption`` function in the R# environment.
    workdir -- optional, the workdir for invoke the target R# function, default work dir
        for the function invocation is at current directory
    image -- optional, the docker image argument for this function invoke, default 
        value none means run on locally, not running in a docker container. The value 
        of this parameter should be generated via the ``docker_image`` helper function. 
    run_debug -- optional, a boolean value for flag the function call running in 
        debug mode or not? set this parameter value to ``True`` means echo more verbose
        information about the function call and skip of the commandline invoke.
    """

    # default has no arguments
    if argv is None: argv = {}
    if options is None: options = {}

    # run rscript command
    RSCRIPT_HOST   = "/usr/local/bin/Rscript.dll"    
    RSCRIPT_LAMBDA = "--lambda {} --SetDllDirectory /usr/local/bin/".format(func)

    save_configs(argv, options, workdir)

    


def save_configs(argv, options, workdir):
    """Save the R# runtime configuration to the workdir

    Keyword arguments:
    workdir -- required, the working directory of the R# function invocation
    argv -- required, the parameter list of the target R# function for invoke
    options -- required, the R# runtime environment configs
    """

    print("*************** setup the R-dotnet runtime environment variables *****************")
    print("")
    print("view of your input parameters:")
    print(argv)

    # Serializing json and setup Rscript envrionment variables 
    # at current workspace
    argv_str = json.dumps(argv, indent = 2)
    pwd = os.path.abspath(workdir)
    r_env = os.path.join(pwd, ".r_env")

    if not os.path.exists(r_env): 
        os.makedirs(r_env)

    jsonfile = open("{}/.r_env/run.json".format(pwd), 'w')
    jsonfile.write(argv_str)
    jsonfile.close()

    argv_str = json.dumps(options, indent = 2)
    
    jsonfile = open("{}/.r_env/options.json".format(pwd), 'w')
    jsonfile.write(argv_str)
    jsonfile.close()

    return argv