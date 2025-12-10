from typing import LiteralString, Literal
from requests import get
from sine.loggable import Loggable
from PIL import Image
from io import BytesIO

class Cover(Loggable):
    """cover helper class, stores an image and automatically crops and adjusts it for best functionality"""
    def __init__(self, url:str|LiteralString, mime:Literal["image/jpeg", "image/png"], name="cover", icon:bool=False, data:bytes=None, erase_bg:int=0, **kwargs):
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
        if erase_bg==0:
            iavg = self._get_img_avg()
            print(iavg)
            if self._check_color(iavg, 60, 0):
                self.erase(25, 0)
        elif erase_bg==1:
            self.erase()
        self.crop()
        self.recode(mime)
        if icon:
            self.iconify()

    def fetch(self) -> None:
        """fetches the image from the set url. meant for internal usage"""
        self.info("fetching cover from url " + self.url)
        resp = get(self.url)
        if resp.status_code == 200:
            self.bin = resp.content
        else:
            self.err("unable to fetch cover, status code " + str(resp.status_code))

    def crop(self):
        """crops the cover in a square from the center to make icons that are nice to look at"""
        self.info(f"cropping {self.name} cover..")
        im = Image.open(BytesIO(self.bin))
        h = im.height
        cent = im.width/2
        left = cent-h/2
        right = cent+h/2
        im = im.crop((left, 0, right, h))
        self.mime=self._write(im)
        self.info("cropped :D")

    def _check_color(self, c, hi, lo):
        """checks a single color between a high and low range"""
        cmap = [True, True, True]
        for i in range(len(c)):
            color=c[i]
            if color>=hi or color<=lo:
                cmap[i]=False
        if cmap[0] and cmap[1] and cmap[2]:
            return True #valid pixel
        else:
            return False #invalid pixel


    def _get_img_avg(self, filter=15):
        """gets the average of every color in the image"""
        im = Image.open(BytesIO(self.bin))
        p = im.load()
        r = 0
        b = 0
        g = 0
        unac = 0 #unaccounted
        for x in range(im.width):
            for y in range(im.height):
                pix = p[x, y]
                if filter!=-1:
                    if not self._check_color(pix, filter, 0):
                        r+=pix[0]
                        b+=pix[1]
                        g+=pix[2]
                    else:
                        unac+=1
                else:
                    r+=pix[0]
                    b+=pix[1]
                    g+=pix[2]
        area = im.width*im.height
        avg_r = r/(area-unac)
        avg_b = b/(area-unac)
        avg_g = g/(area-unac)
        return avg_r, avg_b, avg_g


    def erase(self, hi=200, lo=0):
        """erases all of a range between two colors (such as the background)"""
        self.info(f"erasing the bg of {self.name} cover..")
        im = Image.open(BytesIO(self.bin))
        r = 0 #right
        t = im.height #top
        b = 0 #bottom
        l = im.width #left
        p = im.load()
        for x in range(im.width): #note to self. check if pillow starts from bottom-left or top-left before spending an hour debugging.
            for y in range(im.height):
                if self._check_color(p[x, y], hi, lo):
                    if x < l:
                        l=x
                    if x > r:
                        r=x
                    if y < t:
                        t=y
                    if y > b:
                        b=y
        im=im.crop((l,t,r+1,b+1))
        self.mime=self._write(im)
        self.info(f"erased :D")

    def _write(self, im:Image, fm:str="jpeg"):
        """saves image to binary"""
        b=BytesIO()
        im.save(b, format=fm)
        self.bin=b.getvalue()
        if fm=="png":
            return "image/png"
        else:
            return "image/jpeg"

    def recode(self, mime:Literal["image/jpeg", "image/png"]):
        """recodes the saved image to a new file format"""
        if mime=="image/jpeg":
            self.info(f"recoding {self.name} to jpeg...")
            im = Image.open(BytesIO(self.bin))
            self.mime=self._write(im)
            self.mime = mime
            self.info("recoded :D")
        elif mime=="image/png":
            self.info(f"recoding {self.name} to png...")
            im = Image.open(BytesIO(self.bin))
            self.mime=self._write(im, fm="png")
            self.mime=mime
            self.info("recoded :D")

    def iconify(self):
        """changes the image to be a 32x32 image. created because sometimes windows does not like icons above 32x32 dimensions. not recommended for generic usage"""
        self.info(f"iconifying {self.name}")
        im = Image.open(BytesIO(self.bin))
        im.resize((32, 32))
        if self.mime=="image/png":
            self.mime=self._write(im, fm="png")
        else:
            self.mime=self._write(im)
        self.info("done :D")

    def get(self):
        """returns binary data of image"""
        return self.bin

    def clone(self, name=None):
        """creates a copy containing the roughly same metadata within"""
        if name:
            return Cover(self.url, self.mime, data=self.bin, icon=self.icon, name=name)
        else:
            return Cover(self.url, self.mime, data=self.bin, icon=self.icon, name=self.name)

    def save_cover(self, path:str):
        """saves the modified cover as a file to a new location"""
        with open(path, "wb") as f:
            f.write(self.bin)