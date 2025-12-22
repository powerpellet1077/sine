from concurrent.futures import ThreadPoolExecutor
from tkinter import END
from re import compile
import ttkbootstrap as ttk
from tkinter import NORMAL, DISABLED
from tkinter.filedialog import askdirectory
from ttkbootstrap.widgets.scrolled import ScrolledText
from sine.gui.desktop.config import Config
from sine.gui.desktop.constants import *
from sine.gui.desktop.logger import SineDesktopLogger
from sine import Sine
from sine.gui.desktop.settings import SettingsWindow

class SineApp(ttk.Window):
    """The interface to the sine wrapper through ttkbootstrap. intended for desktop use only, not elegant but semi usable."""
    def __init__(self):
        # core
        self.config = Config()
        t = self.config.get("theme")
        if t:
            super().__init__(themename=t)
        else:
            super().__init__(themename=default_theme)
        self.geometry("600x500")
        self.title("sine")
        self.logger = SineDesktopLogger(self, self.log, self.backlog)
        self.processor = ThreadPoolExecutor(max_workers=1)
        #elements
        self.title_elm = ttk.Label(self, text="sine", font=("Roboto", 45))
        self.title_elm.pack()

        self.title_sep = ttk.Separator(self, bootstyle="light")
        self.title_sep.pack(fill="x")

        self.input_frame = ttk.Labelframe(self, text="input")

        self.input_entry_frame = ttk.Frame(self.input_frame)

        self.input_entry_text_frame = ttk.Frame(self.input_entry_frame)

        self.input_entry_title = ttk.Label(self.input_entry_text_frame, text="link", bootstyle="light")
        self.input_entry_title.pack(side="left", anchor="s")

        self.input_entry_hint = ttk.Label(self.input_entry_text_frame, text="ex: https://www.youtube.com/watch?v=dQw4w9WgXcQ", font=("Roboto", 7), bootstyle="light")
        self.input_entry_hint.pack(side="right", anchor="s")

        self.input_entry_text_frame.pack(fill="x")

        self.input_entry = ttk.Entry(self.input_entry_frame)
        self.input_entry.pack(fill="x")

        self.input_entry_frame.pack(fill="x", padx=5, pady=5)

        self.input_control_frame = ttk.Frame(self.input_frame)

        self.input_control_download = ttk.Button(self.input_control_frame, text="download", bootstyle="success", command=self.download)
        self.input_control_download.pack(side="left", padx=5, pady=5)

        self.input_control_settings = ttk.Button(self.input_control_frame, text="settings", bootstyle="info", command=self.settings)
        self.input_control_settings.pack(side="left", padx=5, pady=5)

        self.input_control_frame.pack(padx=5, pady=5)
        self.input_frame.pack(fill="x", pady=15, padx=15)

        self.log_frame = ttk.Labelframe(self, text="log")

        self.log_inner_frame = ScrolledText(self.log_frame, autohide=True)
        self._logger_disable()
        self.log_inner_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.log_frame.pack(fill="x", padx=15, pady=15)

        self.assign_markup(self.log_inner_frame)

    @staticmethod
    def _sine_run(logger, path, inp):
        sine = Sine(logger=logger)
        sine.run(path, inp)

    def download(self):
        path = askdirectory()
        if not path:
            return
        inp = self.input_entry.get()
        self.processor.submit(
            self._sine_run,
            self.logger,
            inp,
            path
        )

    def settings(self):
        sw = SettingsWindow()
        sw.mainloop()

    def assign_markup(self, tbox:ScrolledText):
        for sym in (sym_blue, sym_magenta, sym_red, sym_green, sym_white, sym_maroon, sym_yellow):
            tbox.text.tag_configure(self.sym_strip(sym), foreground=self.sym_strip(sym))

    @staticmethod
    def sym_strip(sym):
        return (sym.replace("[", "") #most elegant solution indeed
                .replace("]", "")
                .strip())

    def _logger_enable(self):
        self.log_inner_frame.text.config(state=NORMAL)

    def _logger_disable(self):
        self.log_inner_frame.text.config(state=DISABLED)

    def _append_logger(self, text, tag):
        self._logger_enable()
        self.log_inner_frame.text.insert(END, text, tag)
        self._logger_disable()

    # noinspection PyTypeChecker
    def log(self, text):
        m = compile(r"\x1b\[([0-9;]+)m")
        codes = { # manual labor at it's finest
            (0, 0, 0): sym_white,
            (255, 255, 0): sym_yellow,
            (0, 255, 0): sym_green,
            (255, 0, 255): sym_magenta,
            (0, 0, 255): sym_blue,
            (85, 0, 0): sym_maroon
        }
        cursor = 0
        pen = self.sym_strip(sym_white)
        for match in m.finditer(text):
            self._append_logger(text[cursor:match.start()], pen)
            parts = tuple(match.group(1).split(";")[2:])
            code = tuple(int(x) for x in parts)
            if code not in codes:
                print(code) #fixing debug
            pen = self.sym_strip(codes.get(code, sym_white))
            cursor=match.end()
        if cursor < len(text):
            self._append_logger(text[cursor:], pen)

    def backlog(self):
        self._logger_enable()
        self.log_inner_frame.text.delete("end-2l", "end-1l")
        self._logger_disable()