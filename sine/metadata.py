from sine.cover import Cover


class Metadata:
    """YouTube metadata helper class"""
    def __init__(self):
        self.artist:str|None=None #artist name
        self.album:str|None=None #album name, if left blank should return artist's name
        self.year_created:int|None=None #year created (2025 for ex)
        self.cover:Cover|None=None #the front cover in png format
        self.icon:Cover|None=None #the icon in jpeg format
        self.artist_cover:Cover|None=None #artist's icon or image in png format
        self.title:str|None=None #title of song

    def __str__(self):
        return f"{self.__string_format__(self.title)} by {self.__string_format__(self.artist)}"

    def __string_format__(self, string:str):
        if string:
            return string
        else:
            return "[null]"

    def display(self, lf):
        lf(f"metadata get! {self.__str__()}")
    def __len__(self):
        ln = 0
        for o in [self.artist, self.album, self.year_created, self.cover, self.title, self.artist_cover, self.icon]:
            if o:
                ln+=1
        return ln