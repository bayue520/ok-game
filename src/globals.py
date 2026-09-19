from ok import Logger

logger = Logger.get_logger(__name__)


class Globals:

    def __init__(self, exit_event):
        self.exit_event = exit_event