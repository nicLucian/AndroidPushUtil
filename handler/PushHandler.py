from handler.Handler import Handler


class PushHandler(Handler):

    def __init__(self, frame):
        self.build_in_apk_names = ['InCallUI', 'Telecomm', 'TeleService']
        self.commands = []
        devices = frame.get_selected_devices()
        files = frame.get_selected_filepaths()
        if len(devices) <= 0:
            frame.show_dialog("you have not chosen any device yet", "Error")
        elif len(files) <= 0:
            frame.show_dialog("you have not chosen any file yet", "Error")
        else:
            self._exec_commands(devices, files)

    def _exec_commands(self, devices, files):
        for device in devices:
            for file_name in files:
                self.exist = False
                self.push_apk(device, file_name)
                self.install_apk(device, file_name)

    def push_apk(self, device, file_name):
        command = "adb -s " + device + " push " + file_name + " system/app/"
        for buildin_filename in self.build_in_apk_names:
            if buildin_filename in file_name:
                self.exist = True
                command += file_name
                self.commands.append(command)

    def install_apk(self, device, file_name):
        if not self.exist:
            command = "adb -s " + device + " install -r " + file_name
            self.commands.append(command)


