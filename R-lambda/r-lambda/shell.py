import docker
import os

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

    def call_lambda(self, func, run_debug = False):
        pwd = os.getcwd()
        os.chdir(self.workdir)
        exitcode = super().call_lambda(func, run_debug = run_debug)
        os.chdir(pwd)

        return exitcode

class docker_run(shell):

    def __init__(self, argv, options, docker, workdir):
        self.docker = docker
        self.local = local_shell(argv, options, workdir)

        super().__init__(argv, options, workdir)

    def commandline(self, func):
        image_id = self.docker.image

        run_pipeline = []
        run_pipeline.append("docker run -it --rm -e WINEDEBUG=-all")

        if not self.docker.name is None:
            run_pipeline.append("--name \"{}\"".format(self.docker.name))

        run_pipeline = docker.mount_volumn(
            docker_run = run_pipeline, 
            argv = self.argv, 
            workdir = self.workdir, 
            docker = self.docker
        )
        run_pipeline.append(image_id)
        run_pipeline.append(self.local.commandline(func))

        return " ".join(run_pipeline)
