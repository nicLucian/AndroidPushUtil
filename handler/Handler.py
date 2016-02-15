import os


class Handler:
    def __init__(self):
        self.commands = ['']
        pass

    def exec_command(self, frame):
        for command in self.commands:
            result = os.popen(command).readlines()
            self.handle_result(result, frame, command)

    def handle_result(self, result, frame, command):

        pass
