from sine.constants import sickass_placeholder_url, global_sine_version
from sine.downloader import Downloader
from sine.link import Link
from sine.site import Site
from sine.logger import SineLogger
from sine.encoder import SineEncoder
from sine.tagger import Tagger
from sine.path import SinePath
from logging import Logger
from loguru._logger import Logger as LoguruLogger
from time import time


# noinspection PyUnresolvedReferences
class Sine:
    """the sine handler.

    simply call via running sine.run("url", directory)

    silent = kills logging completely
    logger = custom logger/loguru/sinelogger class. will be provided if none"""
    def __init__(self, silent:bool=False, logger:Logger|LoguruLogger|SineLogger=None):
        self.logger:SineLogger|LoguruLogger|Logger|None = None
        if logger:
            self.logger=logger
        elif not silent:
            self.logger=SineLogger()

    def run(self, url:str=sickass_placeholder_url,  output_directory:str="./"):
        """runs sine with given url and directory

        url = any youtube https url. must be youtube.com for it to function properly. if url is empty it will default to one of my favorite songs from FEM&M.
        output_directory = directory where output will be stored. this outputs a temporary m4a file and then converts to a tagged mp3 file. if empty will default to the current relative path of sine"""
        t = time()
        if self.logger:
            self.logger.info("sine started!")

        try:
            meta = Site(logger=self.logger, url=url).obtain_metadata()
            m4a_sp = SinePath(output_directory, logger=self.logger)
            mp3_sp = SinePath(output_directory, logger=self.logger)
            m4a_sp.apply_name(meta.title)
            mp3_sp.apply_name(meta.title, ext="mp3")
            down = Downloader(logger=self.logger)
            link = Link(url, logger=self.logger)
            down.download(link.strip(), m4a_out=m4a_sp)
            enc = SineEncoder(m4a_sp, logger=self.logger)
            enc.encode(mp3_sp)
            enc.clean()
            Tagger(logger=self.logger).tag(mp3_sp, meta)
            et = time()
            if self.logger:
                self.logger.info(f"output saved at "+str(mp3_sp))
                self.logger.success(f"completed in {str(round(et-t, 2))} seconds! :D")
        except Exception as e:
            et = time()
            if self.logger:
                self.logger.log("FAILURE", f"failed in {str(round(et-t, 2))} seconds due to unhandled exception '{str(e)}'")
            return -1