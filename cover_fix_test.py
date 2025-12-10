#DEVELOPMENT PRODUCT
from sine.site import Site
from sine.logger import SineLogger

logger = SineLogger()
meta = Site("https://www.youtube.com/watch?v=LdTIl4FS-58", logger=logger).obtain_metadata()
meta.cover.save_cover("./cover.png")