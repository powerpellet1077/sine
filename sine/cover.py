from typing import LiteralString, Literal, Tuple
from requests import get
from sine.loggable import Loggable
from PIL import Image
from io import BytesIO

class Cover(Loggable):
    """cover helper class, stores an image and automatically crops and adjusts it for best functionality
    
    name = The assigned name to the cover. used for logging.
    icon = iconify image in initialization
    data = provide raw image data. used mostly for internal use
    iconify = reduces size of image to 32x32 and applies an icon tag. I thought it would need this during development but I in fact did not.
    resize_to = if the image is resized, it will resize to width and height of this value
    the rest of the arguments are self-explanatory"""
    def __init__(self, url:str|LiteralString,
                 mime:Literal["image/jpeg", "image/png"],
                 name="cover",
                 iconify:bool=False,
                 data:bytes=None,
                 resize_to:int=360,
                 do_crop:bool=True,
                 do_autocrop:bool=True,
                 do_resize:bool=True, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.name: str = name
        self.bin: bytes|None = None
        self.mime: Literal["image/jpeg", "image/png"] = mime
        self.icon:bool=iconify
        if not data:
            self.fetch()
        else:
            self.bin = data
        if do_crop:
            if do_autocrop: #OMG ITS FIXED :DD
                v = self.vibrancy()
                if v>=45:
                    self.info("vibrancy check passed, auto cropping...")
                    self.auto_crop(vibrancy=v)
                else:
                    self.warn("vibrancy check failed, will not auto crop")
            self.crop()
        if do_resize:
            if self.get_width() < resize_to or self.get_height() < resize_to:
                self.resize(to=(resize_to, resize_to))
        self.recode(mime)
        if iconify:
            self.iconify()

    def fetch(self) -> None:
        """fetches the image from the set url. meant for internal usage"""
        self.info("fetching cover from url " + self.url)
        resp = get(self.url)
        if resp.status_code == 200:
            self.bin = resp.content
        else:
            self.err("unable to fetch cover, status code " + str(resp.status_code))

    def crop(self) -> None:
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

    def _check_color(self, c, hi, lo) -> bool:
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


    def _get_img_avg(self) -> Tuple[float|int, float|int, float|int]:
        """gets the average of every color in the image"""
        im = Image.open(BytesIO(self.bin))
        p = im.load()
        r = 0
        b = 0
        g = 0
        for x in range(im.width):
            for y in range(im.height):
                pix = p[x, y]
                r+=pix[0]
                b+=pix[1]
                g+=pix[2]
        area = im.width*im.height
        avg_r = r/area
        avg_b = b/area
        avg_g = g/area
        return avg_r, avg_b, avg_g

    def vibrancy(self) -> float|int:
        """the overall vibrancy of the image. used internally

        fyi vibrancy means the averaged color of every color in the image, with all three values averaged"""
        return sum(self._get_img_avg())/3

    def _get_color_average(self, color) -> float|int:
        return sum(color)/3

    def resize(self, to:Tuple[float, float]|None=None, by:float|int|None=None) -> None:
        """makes images sometimes look nicer by scaling them up"""
        im = Image.open(BytesIO(self.bin))
        if to:
            self.info(f"resizing cover {self.name} to {to}..")
            im = im.resize(to)
        elif by:
            self.info(f"resizing cover {self.name} by {by}x..")
            im = im.resize(im.width*by, im.height*by)
        else:
            self.failure("did not declare to or by when calling resize, halted")
        self.mime=self._write(im)
        self.info("resized :D")

    def auto_crop(self, vibrancy:float|int) -> None:
        """attempts to automatically crop out pixels within a range of color"""
        self.info(f"auto cropping {self.name} cover..")
        im = Image.open(BytesIO(self.bin))
        r = 0 #right
        t = im.height #top
        b = 0 #bottom
        l = im.width #left
        p = im.load()
        for x in range(im.width): #note to self. check if pillow starts from bottom-left or top-left before spending an hour debugging.
            for y in range(im.height):
                if self._get_color_average(p[x, y]) > vibrancy*1.3:
                    if x < l:
                        l=x
                    if x > r:
                        r=x
                    if y < t:
                        t=y
                    if y > b:
                        b=y
        im=im.crop((l,t,r,b))
        self.mime=self._write(im)
        self.info("autocropped :D")

    def _write(self, im:Image, fm:str="jpeg"):
        """saves image to binary"""
        b=BytesIO()
        im.save(b, format=fm)
        self.bin=b.getvalue()
        if fm=="png":
            return "image/png"
        else:
            return "image/jpeg"

    def get_width(self) -> int:
        """get width of image"""
        im = Image.open(BytesIO(self.bin))
        return im.width

    def get_height(self) -> int:
        """get height of image"""
        im = Image.open(BytesIO(self.bin))
        return im.height

    def get_size(self) -> Tuple[int, int]:
        """get width and height of image"""
        im =  Image.open(BytesIO(self.bin))
        return im.width, im.height

    def recode(self, mime:Literal["image/jpeg", "image/png"]):
        """recodes the saved image to a new file format"""
        im = Image.open(BytesIO(self.bin))
        if mime=="image/jpeg":
            self.info(f"recoding {self.name} to jpeg...")
            self.mime=self._write(im)
        elif mime=="image/png":
            self.info(f"recoding {self.name} to png...")
            self.mime=self._write(im, fm="png")
        else:
            return 0
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
            return Cover(self.url, self.mime, data=self.bin, iconify=self.icon, name=name)
        else:
            return Cover(self.url, self.mime, data=self.bin, iconify=self.icon, name=self.name)

    def save_cover(self, path:str):
        """saves the modified cover as a file to a new location"""
        with open(path, "wb") as f:
            f.write(self.bin)
