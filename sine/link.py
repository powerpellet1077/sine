from typing import LiteralString
from sine.loggable import Loggable


class Link(Loggable):
    """youtube link helper class. only used to prevent people from inputting weird ass links"""
    def __init__(self, link:LiteralString|str, **kwargs):
        super().__init__(**kwargs)
        self.link = link

    def strip(self):
        BASE = "youtube.com/watch?v="
        i = self.link.find(BASE)
        if i!=-1:
            ref = self.link[i+len(BASE):] #refined
            pol = ref.split("&")[0] #polished
            self.info(f"isolated id [{pol}]")
            return "https://"+BASE+pol
        else:
            self.failure(f"unable to strip url. no base '{BASE}' was found inside the url")


    def __str__(self):
        return self.link
