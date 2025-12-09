from kivy import Config
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButtonIcon, MDButton, MDButtonText, MDFabButton
from kivymd.uix.card import MDCard
from kivymd.uix.divider import MDDivider
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.filemanager.filemanager import MDFileManagerItem
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.list import MDListItemLeadingIcon
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon, MDTextFieldHintText, MDTextFieldHelperText
from os.path import expanduser
from sine import Sine
from sine.gui.android.label import LoggableLabel
from sine.gui.android.logger import SineGuiLogger
from concurrent.futures import ThreadPoolExecutor

class SineApp(MDApp):
    def __init__(self, root:str, **kwargs):
        super().__init__(**kwargs)
        #element placeholders
        self.appearance_menu = None
        self.clear_button = None
        self.download_button = None
        self.configuration_menu = None
        self.scrollview = None
        self.log_frame = None
        self.title_sep = None
        self.title_text = None
        self.settings_button = None
        self.screen = None
        self.input_entry = None
        self.main_menu = None
        self.fm = None
        #actual shit
        self.processor = ThreadPoolExecutor(max_workers=20)
        self.logger = None
        self.rt = root
        self.last_position = None

    def build(self):
        self.theme_cls.primaryColor = [1, 1, 1, 1]
        self.theme_cls.backgroundColor = [0, 0, 0, 1]
        self.theme_cls.secondaryColor = [0, 0, 0, 1]
        self.theme_cls.tertiaryColor = [0, 0, 0, 1]
        self.theme_cls.inversePrimaryColor = [0, 0, 0, 1]
        self.theme_cls.surfaceColor = [0, 0, 0, 1]
        self.theme_cls.primary_palette = "Blue"
        #seperated elements for retrival
        self.input_entry = MDTextField(  # url input
            MDTextFieldLeadingIcon(  # icon
                icon="link-variant",
                text_color=self.theme_cls.primaryColor,
                theme_icon_color="Custom",
                icon_color_focus=self.theme_cls.primaryColor,
                icon_color_normal=self.theme_cls.primaryColor
            ),
            MDTextFieldHintText(  # hint
                text="input url",
                text_color_normal=self.theme_cls.primaryColor,
                text_color_focus=self.theme_cls.primaryColor
            ),
            # MDTextFieldHelperText(  # helper
            #     text="ex: youtube.com/watch?v=dQw4w9WgXcQ",
            #     text_color_focus=self.theme_cls.primaryColor,
            #     text_color_normal=self.theme_cls.primaryColor
            # ),
            mode="filled",
            theme_text_color="Custom",
            text_color_normal=self.theme_cls.primaryColor,
            text_color_focus=self.theme_cls.primaryColor,
            theme_line_color="Custom",
            line_color_focus=self.theme_cls.primaryColor,
            line_color_normal=self.theme_cls.primaryColor,
            theme_bg_color="Custom",
            fill_color_normal=self.theme_cls.backgroundColor,
            fill_color_focus=self.theme_cls.backgroundColor,
            size_hint_x=None,
            width=dp(200)
            # minimum_height=0,
            # size_hint_x=0.5
        )
        # self.input_entry.minimum_height=0
        self.settings_button = MDIconButton(  # settings
            icon="dots-horizontal",
            size_hint=(0.15, 0.15),
            pos_hint={"right": 1, "top": 1},
            font_size=sp(48),
            theme_text_color="Custom",
            text_color=self.theme_cls.primaryColor,
            on_release=lambda x: self.open_sm()
        )
        self.title_text = MDLabel( #title
            text="sine",
            font_style="Display",
            size_hint=(0.45, 0.15),
            pos_hint={"x": 0.02, "y": 0.05},
            text_color=self.theme_cls.primaryColor
        )
        self.title_sep = MDDivider( #seperator
            color=self.theme_cls.primaryColor,
            height=dp(1),
            pos_hint={"y": 0, "center_x": 0.5},
            spacing=dp(3)
        )
        self.log_frame = MDBoxLayout(
            orientation="vertical",
            size_hint_x=1,
            size_hint_y=None
        )
        self.log_frame.ignore_bgcolor=True
        self.download_button = MDButton(
            style="filled",
            theme_bg_color="Custom",
            radius=[3, 3, 3, 3],
            size_hint=(None, None),
            height=dp(56),
            width=dp(56),
            md_bg_color=self.theme_cls.primaryColor,
            on_release=lambda x: self.open_selector(),
        )
        # self.download_button.ignore_bgcolor=True
        self.clear_button = MDButton(
            style="filled",
            theme_bg_color="Custom",
            radius=[3, 3, 3, 3],
            size_hint=(None, None),
            height=dp(56),
            width=dp(88),
            md_bg_color=self.theme_cls.primaryColor,
            on_release=lambda x: self.clear_entry(),
        )
        # self.clear_button.ignore_bgcolor=True
        Clock.schedule_once(
            lambda x: self.download_button.add_widget(MDButtonIcon(
            icon="download",
            theme_icon_color="Custom",
            icon_color=self.theme_cls.backgroundColor,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )))
        Clock.schedule_once(
            lambda x: self.clear_button.add_widget(MDButtonIcon(
                icon="trash-can",
                theme_icon_color="Custom",
                icon_color=self.theme_cls.backgroundColor,
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )))
        #trash-can

        #the screen
        self.screen = MDScreen(
            MDBoxLayout( #main layout
                MDFloatLayout( #top layout
                    self.title_text,
                    self.settings_button,
                    self.title_sep,
                    size_hint_y=None,
                    height=dp(80),
                ),
                MDBoxLayout( #input layout
                    self.input_entry, #url input
                    self.clear_button,
                    self.download_button,
                    size_hint_y=None,
                    size_hint_x=1,
                    height=dp(56),
                    orientation="horizontal",
                    spacing=dp(0),
                    padding=dp(0),
                    md_bg_color=[1,0,0,1]
                ),
                MDDivider(
                    orientation="horizontal",
                    color=self.theme_cls.primaryColor
                ),
                MDFloatLayout( #log layout
                    MDCard(
                        MDFloatLayout(
                            MDScrollView(
                                self.log_frame,
                                do_scroll_x=False,
                                do_scroll_y=True,
                                size_hint=(1, 1),
                                pos_hint={"top": 1, "center_x":0.5}
                            ),
                            size_hint=(1, 1)
                        ),
                        size_hint_x=1,
                        size_hint_y=1,
                        style="outlined",
                        radius=[0, 0, 0, 0],
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    ),
                    size_hint_x=1,
                    size_hint_y=1,
                ),
                orientation="vertical",
                padding=dp(8),
                spacing=dp(4),
                size_hint_x=1,
                size_hint_y=1
            )
        )
        self.screen.md_bg_color = self.theme_cls.backgroundColor
        self.logger = SineGuiLogger(self.log)
        self.log_frame.bind(minimum_height=self.log_frame.setter('height'))
        self.redef_gui()
        self.load_sine_config()
        return self.screen

    def clear_entry(self):
        self.input_entry.text = ""

    def set_theme(self, theme:str):
        theme_valid = True
        m=False
        if theme=="Dark":
            self.theme_cls.theme_style = "Dark"
        elif theme=="Light":
            self.theme_cls.theme_style = "Light"
        elif theme=="Midnight":
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primaryColor = [1, 1, 1, 1]
            self.theme_cls.backgroundColor = [0, 0, 0, 1]
            self.theme_cls.secondaryColor = [0, 0, 0, 1]
            m = True
        else:
            theme_valid = False

        if theme_valid:
            if m:
                self.config.set("sine", "lighting", "Midnight")
            else:
                self.config.set("sine", "lighting", self.theme_cls.theme_style)
            self.config.write()
        else:
            print("dfdsfsduf")
        self.screen.md_bg_color = self.theme_cls.backgroundColor
        if self.appearance_menu:
            self.appearance_menu.dismiss()
        if self.main_menu:
            self.main_menu.dismiss()
        self.redef_gui()

    def build_config(self, config):
        config.setdefaults(
            "sine", {
                "lighting": "Dark",
                "last_directory": ""
            }
        )

    def load_sine_config(self):
        lighting = self.config.get("sine", "lighting")
        self.set_theme(lighting)
        directory = self.config.get("sine", "last_directory")
        if directory.strip()!="":
            self.last_position=directory



    def open_am(self):
        self.appearance_menu = MDDropdownMenu(
            caller=self.main_menu,
            md_bg_color=self.theme_cls.backgroundColor,
            items=[
                {
                    "text": "Midnight",
                    "leading_icon": "lightbulb-night",
                    "on_release": lambda: self.set_theme("Midnight"),
                    "theme_text_color": "Custom",
                    "text_color": self.theme_cls.primaryColor,
                    "leading_icon_color": self.theme_cls.primaryColor,
                    "md_bg_color": self.theme_cls.backgroundColor
                },
                {
                    "text": "Dark",
                    "leading_icon": "weather-night",
                    "on_release": lambda: self.set_theme("Dark"),
                    "theme_text_color": "Custom",
                    "text_color": self.theme_cls.primaryColor,
                    "leading_icon_color": self.theme_cls.primaryColor,
                    "md_bg_color": self.theme_cls.backgroundColor
                },
                {
                    "text": "Light",
                    "leading_icon": "weather-sunny",
                    "on_release": lambda: self.set_theme("Light"),
                    "theme_text_color": "Custom",
                    "text_color": self.theme_cls.primaryColor,
                    "leading_icon_color": self.theme_cls.primaryColor,
                    "md_bg_color": self.theme_cls.backgroundColor
                }
            ]
        )
        self.appearance_menu.open()

    def open_sm(self):
        self.main_menu = MDDropdownMenu(
            caller=self.settings_button,
            md_bg_color=self.theme_cls.backgroundColor,
            items=[
                {
                    "text": "Appearance",
                    "leading_icon": "theme-light-dark",
                    "on_release": self.open_am,
                    "theme_text_color": "Custom",
                    "text_color": self.theme_cls.primaryColor,
                    "leading_icon_color": self.theme_cls.primaryColor,
                    "md_bg_color": self.theme_cls.backgroundColor
                },
                {
                    "text": "Configuration",
                    "leading_icon": "wrench",
                    "theme_text_color": "Custom",
                    "on_release": self.open_cf,
                    "text_color": self.theme_cls.primaryColor,
                    "leading_icon_color": self.theme_cls.primaryColor,
                    "md_bg_color": self.theme_cls.backgroundColor

                }
            ],
        )
        self.main_menu.open()

    def open_cf(self):
        self.configuration_menu = MDDropdownMenu(
            caller=self.main_menu,
            md_bg_color=self.theme_cls.backgroundColor,
            items=[
                {
                    "text": "nothing here yet :P",
                    "leading_icon": "baguette",
                    "theme_text_color": "Custom",
                    "text_color": self.theme_cls.primaryColor,
                    "leading_icon_color": self.theme_cls.primaryColor,
                    "md_bg_color": self.theme_cls.backgroundColor
                }
            ]
        )
        self.configuration_menu.open()

    def format_wid(self, wid):
        for dec in (
            ("text_color", self.theme_cls.primaryColor, None, MDButtonIcon),
            ("color", self.theme_cls.primaryColor, None, MDButtonIcon),
            ("md_bg_color", self.theme_cls.backgroundColor, None, (MDLabel, MDButton)),
            ("md_bg_color", self.theme_cls.primaryColor, MDButton),
            ("text_color_normal", self.theme_cls.primaryColor),
            ("text_color_focus", self.theme_cls.primaryColor),
            ("theme_text_color", "Custom"),
            ("theme_line_color", "Custom"),
            ("line_color", self.theme_cls.primaryColor, MDCard),
            ("line_color_focus", self.theme_cls.primaryColor),
            ("line_color_normal", self.theme_cls.primaryColor),
            ("theme_bg_color", "Custom"),
            ("fill_color_normal", self.theme_cls.backgroundColor),
            ("fill_color_focus", self.theme_cls.backgroundColor),
            ("leading_icon_color", self.theme_cls.primaryColor),
            ("theme_icon_color", "Custom"),
            ("icon_color_focus", self.theme_cls.primaryColor),
            ("icon_color_normal", self.theme_cls.primaryColor),
            ("title_color", self.theme_cls.primaryColor),
            ("specific_text_color", self.theme_cls.primaryColor),
            ("background_color_toolbar", self.theme_cls.backgroundColor),
            ("background_color_selection_button", self.theme_cls.backgroundColor, None, MDFileManager),
            ("icon_color", self.theme_cls.primaryColor, None, MDButtonIcon),
            ("icon_color", self.theme_cls.backgroundColor, MDButtonIcon),
            ("divider_color", self.theme_cls.primaryColor),
            ("md_bg_color_disabled", self.theme_cls.backgroundColor),
            ("font_name", self.rt+"/sine/gui/assets/jbm.ttf", LoggableLabel)
        ):
            if not ((hasattr(wid, "ignore_decolor") and dec[0] == "text_color") or (hasattr(wid, "ignore_bgcolor") and dec[0]=="md_bg_color")):
                if len(dec) == 4:
                    if hasattr(wid, dec[0]) and not isinstance(wid, dec[3]):
                        setattr(wid, dec[0], dec[1])
                        print(f"changed {wid} {dec[0]} to {dec[1]}")
                elif len(dec) == 3:
                    if hasattr(wid, dec[0]) and isinstance(wid, dec[2]):
                        setattr(wid, dec[0], dec[1])
                        print(f"changed {wid} {dec[0]} to {dec[1]}")
                else:
                    if hasattr(wid, dec[0]):
                        setattr(wid, dec[0], dec[1])
                        print(f"changed {wid} {dec[0]} to {dec[1]}")
        return wid


    def redef_gui(self):
        for wid in self.retrive_widgets():
            self.format_wid(wid)

    def retrive_widgets(self, w=None):
        if not w:
            w = self.screen
        widgets = [w]
        for c in w.children:
            widgets.extend(self.retrive_widgets(c))
        return widgets

    def open_selector(self):
        url = self.input_entry.text
        if url.strip() == "":
            self.logger.say("you must enter a link")
            return
        self.fm = (MDFileManager(
            selector="folder",
            select_path=lambda x:self.run_sine(url, x),
            exit_manager=lambda x:self.close_fm(),
            icon_selection_button="download",
            background_color_selection_button=self.theme_cls.backgroundColor,
        ))
        if self.last_position:
            self.fm.show(self.last_position)
        else:
            self.fm.show(expanduser("~"))
        Clock.schedule_once(lambda x: self.tree_format(self.fm))

    def set_attr(self, obj, ref, val):
        if hasattr(obj, ref):
            setattr(obj, ref, val)


    def tree_format(self, wid):
        for o in self.retrive_widgets(wid):
            self.format_wid(o)


    def close_fm(self):
        if self.fm:
            self.fm.close()

    def log(self, msg):
        Clock.schedule_once(
            lambda x: self.log_frame.add_widget(
                self.format_wid(LoggableLabel(
                    text=msg,
                    size_hint_x=1,
                    size_hint_y=None,
                    markup=True,
                    font_size=dp(4)
                ))
            )
        )


    def run_sine(self, url, path):
        if self.fm:
            self.fm.close()
        self.last_position=path
        self.config.set("sine", "last_directory", path)
        self.config.write()
        self.processor.submit(lambda: Sine(logger=self.logger).run(url, path))
