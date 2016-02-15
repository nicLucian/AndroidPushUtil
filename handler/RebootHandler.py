from handler.Handler import Handler


class RebootHandler(Handler):
    def __init__(self, frame):
        devices = frame.get_selected_devices()
        print devices
        self.commands = []

    def handle_result(self, result, frame):
        frame.set_status(result)

