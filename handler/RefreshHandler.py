from handler.Handler import Handler


class RefreshHandler(Handler):
    def __init__(self):
        self.commands = ["adb devices"]

    def handle_result(self, result_lines, frame, command):
        self._set_status(result_lines, frame, command)
        self._set_devices(result_lines, frame)

    def _set_devices(self, result_lines, frame):
        for line in result_lines:
            if line.endswith("device\n"):
                device_name = line.split('\t')[0]
                frame.add_device(device_name)


    def _set_status(self, result_lines, frame, command):
        result = command + ":\n"
        for line in result_lines:
            result = result + line + str()
        frame.set_status(result)



