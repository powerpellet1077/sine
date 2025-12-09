from typing import LiteralString

from eyed3 import load
from eyed3.id3.frames import ImageFrame
from eyed3.id3 import ID3_V2_3
from eyed3.core import AudioFile
from scripts.regsetup import description

from sine.loggable import Loggable
from sine.metadata import Metadata
from sine.path import SinePath


class Tagger(Loggable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def tag(self, path:str|LiteralString|SinePath, meta:Metadata):
        self.info("initializing tagger...")
        f = load(str(path))
        if not f.tag:
            f.initTag(version=ID3_V2_3)
        if meta.artist:
            f.tag.artist=meta.artist
            f.tag.album_artist=meta.artist
        if meta.album:
            f.tag.album=meta.album
        if meta.year_created:
            f.tag.release_date=meta.year_created
        if meta.title:
            f.tag.title=meta.title
        if meta.cover:
            self.info("applying front cover...")
            f.tag.images.set(
                ImageFrame.FRONT_COVER,
                meta.cover.get(),
                meta.cover.mime,
                description="cover"
            )
        if meta.icon:
            self.info("applying icon cover...")
            f.tag.images.set(
                ImageFrame.ICON,
                meta.icon.get(),
                meta.icon.mime,
                description="icon"
            )
        if meta.artist_cover:
            self.info("applying artist cover...")
            f.tag.images.set(
                ImageFrame.ARTIST,
                meta.artist_cover.get(),
                meta.artist_cover.mime,
                description="artist"
            )
        self.info("writing tags...")
        f.tag.save()