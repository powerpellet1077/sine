from sine.gui.android.app import SineApp
from os.path import dirname, abspath

if __name__ == "__main__":
    root = str(dirname(abspath(__file__))).replace("\\", "/")
    SineApp(root).run()
