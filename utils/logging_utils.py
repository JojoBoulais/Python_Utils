import logging


class MyLogger(logging.Logger):
    def __init__(self,
                 name=__name__,
                 level=logging.NOTSET):
        super().__init__(name, level)
        self.extra_info = None

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def info(self, msg, *args, xtra=None, **kwargs):
        extra_info = xtra if xtra is not None else self.extra_info
        super().info(msg, *args, extra=extra_info, **kwargs)



myLogger = MyLogger()

myLogger.info("yippppi")