#coding=utf8

from handler.Handler import Handler


class RebootHandler(Handler):
    def __init__(self, frame):
        self.devices = frame.get_selected_devices()
        self.commands = []
        for device in self.devices:
            command = "adb -s " + device + " reboot"
            self.commands.append(command)


