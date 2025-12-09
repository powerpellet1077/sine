from yt_dlp import YoutubeDL
from sine.link import Link
from sine.loggable import Loggable
from sine.path import SinePath


class Downloader(Loggable):
    """very very very basic ytdlp downloader"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def download(self, url:Link, m4a_out:str|SinePath="sine.m4a"):
        """uses yt-dlp to download via youtubedl. outputs compressed m4a to m4a_out"""
        with YoutubeDL({
                "logger": self._logger,
                "format": "bestaudio[ext=m4a]",
                "outtmpl": str(m4a_out)}
        ) as ydl:
            info = ydl.extract_info(str(url), download=True)
            fp = ydl.prepare_filename(info)
            self.info("downloaded successfully :D")
            return fp