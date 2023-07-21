class shell:

    def __init__(self, argv, options, workdir):
        self.argv = argv
        self.options = options
        self.workdir = workdir

    @abstractmethod
    def commandline(self, func):
        """Generates the commandline for run the target R# lambda function
        """
        pass

    def call_lambda(self, func, run_debug = False):
        shell = 0
        shell_command = self.commandline(func, run_debug)
        
        print("")
        print("Run shell commandline:")
        print(shell_command)
        print("")

        if not run_debug:
            shell = os.system(shell_command)
        else:
            print("skip of run shell command!")

        print("run R# lambda pipeline job done!")
        print("exit={0}".format(shell))
        print("")

        return shell

class local_shell(shell):

    def __init__(self, argv, options, workdir):
        super().__init__(argv, options, workdir)

    def commandline(self, func):
        # run rscript command
        RSCRIPT_HOST   = "/usr/local/bin/Rscript.dll"    
        RSCRIPT_LAMBDA = "--lambda {} --SetDllDirectory /usr/local/bin/".format(func)

        shell = []
        shell.append("dotnet")
        shell.append(RSCRIPT_HOST)
        shell.append(RSCRIPT_LAMBDA)

        return " ".join(shell)

class docker_run(shell):

    def __init__(self, argv, options, docker, workdir):
        self.docker = docker
        super().__init__(argv, options, workdir)

    def commandline(self, func):