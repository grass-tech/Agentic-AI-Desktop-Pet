from .customize import function, constants

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget

from qfluentwidgets import SettingCardGroup, SwitchSettingCard, OptionsSettingCard, \
    OptionsConfigItem, BoolValidator, QConfig, qconfig, OptionsValidator, ExpandLayout, \
    FluentIcon, ScrollArea, InfoBar, InfoBarPosition


class Config(QConfig):
    compatible = OptionsConfigItem("General", "compatible", False, BoolValidator())
    adult = OptionsConfigItem("General", "adult", False, BoolValidator())
    recognition = OptionsConfigItem("General", "recognition", False, BoolValidator())
    speaker = OptionsConfigItem("General", "speaker", False, BoolValidator())
    search = OptionsConfigItem("General", "search", False, BoolValidator())
    translate = OptionsConfigItem("General", "translate", False, BoolValidator())

    penetration = OptionsConfigItem(
        "Advanced", "penetration", "shut",
        OptionsValidator(["shut", "next", "left-bottom", "left-top", "right-bottom", "right-top"]), restart=True)
    taskbar_lock = OptionsConfigItem("Advanced", "locktsk", True, BoolValidator())
    media_understanding = OptionsConfigItem("Advanced", "media", False, BoolValidator())

    live2d_blink = OptionsConfigItem("Live2D", "AutoBlink", True, BoolValidator())
    live2d_breath = OptionsConfigItem("Live2D", "AutoBreath", True, BoolValidator())
    live2d_drag = OptionsConfigItem("Live2D", "AutoDrag", True, BoolValidator())


class Switches(ScrollArea):
    def __init__(self, languages, cache_config, configure):
        super().__init__()
        self.cache_config = cache_config
        self.languages = languages
        self.configure = configure

        self.scroll_widgets = QWidget()
        self.expand_layout = ExpandLayout(self.scroll_widgets)
        qconfig.load("./interface/setting/switch.json", Config)
        # 常规设置
        self.general_group = SettingCardGroup(self.languages[11], self.scroll_widgets)
        self.card_compatible_capture = SwitchSettingCard(
            icon=FluentIcon.FIT_PAGE,
            title=self.languages[12],
            content=self.languages[125],
            parent=self.general_group,
            configItem=Config.compatible,
        )
        self.card_compatible_capture.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.compatibility",
                value, "General.compatible"
            ))
        self.general_group.addSettingCard(self.card_compatible_capture)
        self.card_adult = SwitchSettingCard(
            configItem=Config.adult,
            icon=FluentIcon.HEART,
            title=self.languages[5],
            content=self.languages[127],
            parent=self.general_group
        )
        self.card_adult.checkedChanged.connect(
            lambda value: self.pop_success(
                self.languages[128], self.languages[129],
                function.change_configure, 1 if value else 0, "adult_level", self.configure))
        self.general_group.addSettingCard(self.card_adult)
        self.card_recognition = SwitchSettingCard(
            configItem=Config.recognition,
            icon=FluentIcon.MICROPHONE,
            title=self.languages[13],
            content=self.languages[130],
            parent=self.general_group
        )
        self.card_recognition.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.enable.rec",
                value, "General.recognition"
            ))
        self.general_group.addSettingCard(self.card_recognition)
        self.card_speaker = SwitchSettingCard(
            configItem=Config.speaker,
            icon=FluentIcon.SPEAKERS,
            title=self.languages[14],
            content=self.languages[131],
            parent=self.general_group
        )
        self.card_speaker.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.enable.tts",
                value, "General.speaker"
            ))
        self.general_group.addSettingCard(self.card_speaker)
        self.card_search = SwitchSettingCard(
            configItem=Config.search,
            icon=FluentIcon.SEARCH,
            title=self.languages[15],
            content=self.languages[132],
            parent=self.general_group
        )
        self.card_search.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.enable.online",
                value, "General.search"
            ))
        self.general_group.addSettingCard(self.card_search)
        self.card_translate = SwitchSettingCard(
            configItem=Config.translate,
            icon=FluentIcon.LANGUAGE,
            title=self.languages[16],
            content=self.languages[133],
            parent=self.general_group
        )
        self.card_translate.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.enable.trans",
                value, "General.translate"
            ))
        self.general_group.addSettingCard(self.card_translate)

        # 高级设置
        self.advanced_group = SettingCardGroup(self.languages[17], self.scroll_widgets)
        self.media_understanding = SwitchSettingCard(
            configItem=Config.media_understanding,
            icon=FluentIcon.PHOTO,
            title=self.languages[18],
            content=self.languages[126],
            parent=self.advanced_group
        )
        self.media_understanding.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.enable.media",
                value, "Advanced.media"
            ))
        self.advanced_group.addSettingCard(self.media_understanding)
        self.card_mouse_penetration = OptionsSettingCard(
            Config.penetration,
            icon=FluentIcon.TRANSPARENT,
            title=self.languages[19],
            content=self.languages[84],
            texts=[self.languages[20], self.languages[21], self.languages[22],
                   self.languages[23], self.languages[24], self.languages[25]],
            parent=self.advanced_group
        )
        self.card_mouse_penetration.optionChanged.connect(
            lambda value: function.change_configure(
                value.value, "Advanced.penetration", cache_config, constants.CACHE_CONFIGURE_PATH))
        self.advanced_group.addSettingCard(self.card_mouse_penetration)

        self.card_taskbar_lock = SwitchSettingCard(
            configItem=Config.taskbar_lock,
            icon=FluentIcon.PIN,
            title=self.languages[26],
            content=self.languages[85],
            parent=self.advanced_group
        )
        self.card_taskbar_lock.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.enable.locktsk",
                value, "Advanced.locktsk"
            ))
        self.advanced_group.addSettingCard(self.card_taskbar_lock)

        # Live2D 设置
        self.live2d_group = SettingCardGroup(f"Live2D {self.languages[10]}", self.scroll_widgets)
        self.card_auto_blink = SwitchSettingCard(
            configItem=Config.live2d_blink,
            icon=FluentIcon.VIEW,
            title=self.languages[74],
            content=self.languages[74],
            parent=self.live2d_group
        )
        self.card_auto_blink.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.live2d.enable.AutoBlink",
                value, "Live2D.AutoBlink"
            ))
        self.live2d_group.addSettingCard(self.card_auto_blink)
        self.card_auto_breath = SwitchSettingCard(
            configItem=Config.live2d_breath,
            icon=FluentIcon.SYNC,
            title=self.languages[75],
            content=self.languages[75],
            parent=self.live2d_group
        )
        self.card_auto_breath.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.live2d.enable.AutoBreath",
                value, "Live2D.AutoBreath"
            ))
        self.live2d_group.addSettingCard(self.card_auto_breath)
        self.card_auto_drag = SwitchSettingCard(
            configItem=Config.live2d_drag,
            icon=FluentIcon.MOVE,
            title=self.languages[76],
            content=self.languages[76],
            parent=self.live2d_group
        )
        self.card_auto_drag.checkedChanged.connect(
            lambda value: self.change_configure(
                value, "settings.live2d.enable.AutoDrag",
                value, "Live2D.AutoDrag"
            ))
        self.live2d_group.addSettingCard(self.card_auto_drag)

        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.addWidget(self.general_group)
        self.expand_layout.addWidget(self.advanced_group)
        self.expand_layout.addWidget(self.live2d_group)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.scroll_widgets)
        self.scroll_widgets.setObjectName('ScrollWidget')
        self.setObjectName("Switches")

    def change_configure(self, value, relative, cache_value, cache_relative):
        function.change_configure(cache_value, cache_relative, self.cache_config, constants.CACHE_CONFIGURE_PATH)
        function.change_configure(value, relative, self.configure)

    def pop_success(self, title, content, func, *args):
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1200,
            parent=self
        )
        func(*args)


Config = Config()
