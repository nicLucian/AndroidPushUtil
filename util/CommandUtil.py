import os


class CommandUtil:
    def __init__(self):
        pass

    def devices(self):
        command = "adb devices"
        result = os.popen(command)
        return result.readlines()
