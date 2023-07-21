class shell:

    def __init__(self, argv, options, docker, workdir):
        self.argv = argv
        self.options = options
        self.docker = docker
        self.workdir = workdir

    @abstractmethod
    def commandline(self):
        pass

class local_run(shell):

    def __init__(self, argv, options, workdir):
        super().__init__(argv, options, None, workdir)

    def commandline(self):


class docker_run(shell):

    def __init__(self, argv, options, docker, workdir):
        super().__init__(argv, options, None, workdir)

    def commandline(self):