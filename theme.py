from fluxtual.enums import Brightness, TextAlign
from fluxtual.widgets.text import TextStyle

class TextTheme:
    """Text theme"""
    def __init__(
        self,
        body_normal: TextStyle | None = None,
        body_bold: TextStyle | None = None
    ):
        self.normal = body_normal
        self.bold = body_bold

class ThemeData:
    """Defines the configuration of the overall visual Theme for a widget subtree within the app."""
    def __init__(
        self,
        brightness: Brightness = Brightness.dark,
        primary_color: str | None = None,
        text_theme: TextTheme = TextTheme()
    ):
        pass