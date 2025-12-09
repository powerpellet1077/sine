from typing import LiteralString, Literal
from requests import get
from sine.loggable import Loggable
from PIL import Image
from io import BytesIO

class Cover(Loggable):
    """cover helper class, apply cover url as argument and it will fetch and fix"""
    def __init__(self, url:str|LiteralString, mime:Literal["image/jpeg", "image/png"], name="cover", icon:bool=False, data:bytes=None, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.name: str = name
        self.bin: bytes|None = None
        self.mime: Literal["image/jpeg", "image/png"] = mime
        self.icon:bool=icon
        if not data:
            self.fetch()
        else:
            self.bin = data
        self.fix()
        self.recode(mime)
        if icon:
            self.iconify()

    def fetch(self):
        self.info("fetching cover from url " + self.url)
        resp = get(self.url)
        if resp.status_code == 200:
            self.bin = resp.content
        else:
            self.err("unable to fetch cover, status code " + str(resp.status_code))

    def fix(self):
        self.info(f"fixing {self.name} cover sizing..")
        im = Image.open(BytesIO(self.bin))
        h = im.height
        cent = im.width/2
        left = cent-h/2
        right = cent+h/2
        im = im.crop((left, 0, right, h))
        r = BytesIO()
        im.save(r, format="jpeg")
        self.mime="image/jpeg"
        self.bin = r.getvalue()
        self.info("fixed :D")

    def recode(self, mime:Literal["image/jpeg", "image/png"]):
        if mime=="image/jpeg":
            self.info(f"recoding {self.name} to jpeg...")
            im = Image.open(BytesIO(self.bin))
            b = BytesIO()
            im.save(b, format="jpeg")
            self.bin = b.getvalue()
            self.mime = mime
            self.info("recoded :D")
        elif mime=="image/png":
            self.info(f"recoding {self.name} to png...")
            im = Image.open(BytesIO(self.bin))
            b = BytesIO()
            im.save(b, format="png")
            self.bin = b.getvalue()
            self.mime=mime
            self.info("recoded :D")

    def iconify(self):
        self.info(f"iconifying {self.name}")
        im = Image.open(BytesIO(self.bin))
        im.resize((32, 32))
        b = BytesIO()
        if self.mime=="image/png":
            im.save(b, format="png")
        else:
            im.save(b, format="jpeg")
        self.bin = b.getvalue()
        self.info("done :D")

    def get(self):
        """returns binary data of image"""
        return self.bin

    def clone(self, name=None):
        if name:
            return Cover(self.url, self.mime, data=self.bin, icon=self.icon, name=name)
        else:
            return Cover(self.url, self.mime, data=self.bin, icon=self.icon, name=self.name)