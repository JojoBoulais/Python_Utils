import logging


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;20m"
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    COLOR_MAPPING = {
        logging.DEBUG: grey,
        logging.INFO: grey,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red
    }

    fmt = "[%(asctime)s] | %(levelname)8s | '%(message)s' (%(filename)s:%(lineno)s)"
    time_format = '%H:%M:%S'

    def __init__(self):
        super().__init__()

    def format(self, record):
        color = self.COLOR_MAPPING.get(record.levelno)
        log_fmt = color + self.fmt + self.reset
        formatter = logging.Formatter(log_fmt, datefmt=self.time_format)
        return formatter.format(record)


class MyLogger(logging.Logger):
    def __init__(self,
                 name=__name__,
                 level=logging.NOTSET):
        super().__init__(name, level)

        self.extra_info = None
        self.custom_formatter = CustomFormatter()

        handler = logging.StreamHandler()

        handler.setFormatter(self.custom_formatter)
        self.addHandler(handler)

    def info(self, msg, *args, xtra=None, **kwargs):
        extra_info = xtra if xtra is not None else self.extra_info
        super().info(msg, *args, extra=extra_info, **kwargs)


myLogger = MyLogger()

myLogger.info("yippppi")
myLogger.warning("yippppi")
