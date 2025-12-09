from sine.loggable import Loggable
from os.path import abspath
from string import ascii_lowercase, punctuation
from random import choice

class SinePath(Loggable):
    """incredibly small object and it's only purpose is to make songs have names and directories

    if no name for file is defined, it will automatically become random ascii characters.

    https://files.catbox.moe/rxeuv8.mp4"""
    def __init__(self, target_directory:str, **kwargs):
        super().__init__(**kwargs)
        self.raw_path = target_directory
        self.path:str
        self.raw_path = self.format_raw_path(self.raw_path)
        self.apply_name(self.gen_temp_name())

    def apply_name(self, name:str, do_not_adjust:bool=False, ext:str="m4a"):
        if do_not_adjust:
            self.path=self.format_raw_path(abspath(self.raw_path))+"/"+name+"."+ext.lower()
        else:
            self.path=self.format_raw_path(abspath(self.raw_path))+"/"+self.format_text(name)+"."+ext.lower()
        self.info("saved path adjusted to "+self.path)

    def format_text(self, text:str):
        t = text
        for punc in punctuation:
            t = t.replace(punc, "")
        if t == "":
            t = "_"
        t = t.replace(" ", "_")
        return t.lower()

    def gen_temp_name(self):
        out = ""
        for i in range(8):
            out+=choice(ascii_lowercase)
        return out+".m4a"

    def format_raw_path(self, path:str):
        return path.replace("\\", "/").replace("//", "/")

    def __str__(self):
        return self.path

    def __len__(self):
        return len(self.path)