from kivymd.uix.label import MDLabel


class LoggableLabel(MDLabel):
    """label modified to fix height in boxlayouts bcuz kivy is ass and does not do this for you"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(texture_size=self._update_height)
        self.ignore_decolor=True

    def _update_height(self, instance, value):
        self.height = value[1]