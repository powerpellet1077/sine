from sine.logger import SineLogger
from ttkbootstrap import Window
class SineDesktopLogger(SineLogger):
    """sine logger modified to function properly with desktop application"""
    def __init__(self, parent: Window, log_call, backlog_call,  **kwargs):
        super().__init__(**kwargs)
        self.log_call = log_call
        self.backlog_call = backlog_call
        self.parent = parent
    def __sine_sink__(self, message):
        m = (message.replace("*func*", str(message.record["module"]+"."+message.record["function"]).lower()))
        m = m.replace("__init__", "sine")
        if m.find("*back*")!=-1:
            m=m.replace("*back*","")
            self.parent.after(
                0,
                self.backlog_call,
                None
            )
        self.parent.after(
            0,
            self.log_call,
            m
        )