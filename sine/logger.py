from loguru._logger import Core, Logger
from sys import exit, stdout
from sine.constants import log_l, log_lc, log_yfgc, log_yfg, log_bfg, log_mfg, log_rfg, log_mafg, log_gfg


class SineLogger(Logger):
    """custom loguru logger wrapper for custom cool logging. same syntax as loguru.logger"""
    def __init__(self, close_on_crit=False):
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
        self.COE = close_on_crit
        self.add(self.__sine_sink__, colorize=True, format=f"{log_l}[{{level}}]{log_lc+log_yfg}[*func*]{log_yfgc} {{message}}")
        self.level("WARNING", color=log_yfg)
        self.level("ERROR", color=log_rfg)
        self.level("INFO", color=log_bfg)
        self.level("CRITICAL", color=log_mfg)
        self.level("FAILURE", color=log_mafg, no=50)
        self.level("SUCCESS", color=log_gfg)
        self.debug = self.info


    def __sine_sink__(self, message):
        m = (message.replace("*func*", str(message.record["module"]+"."+message.record["function"]).lower()))
        m = m.replace("__init__", "sine")
        if m.find("*back*")!=-1:
            m=m.replace("*back*","")
            stdout.write("\x1b[1A\x1b[2K")
            stdout.flush()
        stdout.write(m)
        if message.record["level"].name=="CRITICAL" and not self.COE:
            exit()
