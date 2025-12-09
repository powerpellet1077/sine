import os.path

from audioread import audio_open
from lameenc import Encoder
from sine.loggable import Loggable
from sine.path import SinePath
class SineEncoder(Loggable):
    def __init__(self, input_path:str|SinePath, **kwargs):
        super().__init__(**kwargs)
        self.f = str(input_path)

    def encode(self, outpath:str|SinePath):
        self.info("beginning encode...")
        e = Encoder()
        with audio_open(self.f) as f:
            e.set_channels(f.channels)
            e.set_in_sample_rate(f.samplerate)
            e.set_quality(2)
            e.set_bit_rate(128)
            dat = b""
            i = 0
            l = 0
            buffers = []
            self.info(f"indexing buffers...")
            for buf in f:
                l+=1
                buffers.append(buf)

            for buffer in buffers:
                i += 1
                if i%100==0 or i==l:
                    self.info(f"encoding buffer {str(i)}/{str(l)}")
                dat+=e.encode(buffer)

            dat+=e.flush()
        self.info(f"writing to {outpath}")
        with open(str(outpath), "wb") as f:
            f.write(dat)

    def clean(self):
        self.info("attempting to clean up..")
        try:
            if os.path.exists(self.f) and os.path.isfile(self.f):
                os.remove(self.f)
                self.info("cleaned :D")
            else:
                self.info("could not find temp file to clean. the problem solved itself ¯\\_(ツ)_/¯")
        except PermissionError:
            self.warn(f"was unable to clean up due to lack of permissions at point {self.f}")
        except Exception as e:
            self.warn(f"was unable to clean up due to unhandled exception '{str(e)}'")

