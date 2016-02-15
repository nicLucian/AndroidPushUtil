import os


class Handler:
    def __init__(self):
        self.commands = []
        pass

    def exec_command(self, frame):
        if len(self.commands) <= 0:
            self.handle_result("you have not chosen any device\n", frame)

        for command in self.commands:
            result = os.popen(command).readlines()
            self.handle_result(result, frame, command=command)

    def handle_result(self, result_lines, frame, command=""):
        result = command + ":\n"
        for line in result_lines:
            result = result + line
        frame.set_status(result)
