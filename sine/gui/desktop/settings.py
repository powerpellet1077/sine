from ttkbootstrap import Toplevel, Label


class SettingsWindow(Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("settings")
        self.geometry("200x400")

        self.nothing_here_label = Label(self, text="nothing here yet :P")
        self.nothing_here_label.pack()