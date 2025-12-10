from loguru._logger import Logger, Core
from sine.gui.android.constants import *


class SineGuiLogger(Logger):
    """modified SineLogger to interface directly through the kivy application instead of through the console"""
    def __init__(self, log):
        super().__init__(
            Core(),
            exception=None,
            depth=0,
            record=False,
            lazy=False,
            colors=False,
            raw=False,
            capture=True,
            patchers=[],
            extra={}
        )
        self.add(self.__sine_sink__)
        self.level("WARNING")
        self.level("ERROR")
        self.level("INFO")
        self.level("CRITICAL")
        self.level("FAILURE", no=50)
        self.level("SUCCESS")
        self.log = log

    def _color_with_level(self, text, level):
        mu = {"WARNING": kv_yellow,
              "ERROR": kv_red,
              "INFO": kv_blue,
              "SUCCESS": kv_green,
              "CRITICAL": kv_magenta,
              "FAILURE": kv_maroon,
              "DEBUG": kv_blue}[level]
        return mu+text+kv_close

    def __sine_sink__(self, message):
        self.log(((self._color_with_level("<"+message.record["level"].name+">" ,message.record["level"].name)+
            kv_yellow+
            "<*func*>"+
            kv_close+
            " "+
            self._color_with_level(message.record["message"], message.record["level"].name))
            .replace("*func*", str(message.record["module"] + "." + message.record["function"]).lower()))
            .replace("__init__", "sine"))

    def say(self, message):
        self.info(message)
