from textual.widget import Widget
from fluxtual.context import BuildContext
from fluxtual.theme import ThemeData, Theme
from fluxtual.color import Color
from fluxtual.enums import Brightness
from fluxtual.widgets.base import State, StatefulWidget
from fluxtual.widgets.text import DefaultTextStyle, TextStyle


class _MaterialAppState(State["MaterialApp"]):
    def _theme_builder(self):
        """Resolve which theme to use based on brightness. Supports 0/1 flutter arguments.
            high-contrast themes and system theme not support."""
        theme = None
        mode = self.widget.theme_mode or Brightness.light
        use_dark_theme = mode == Brightness.dark
        if use_dark_theme and self.widget.dark_theme != None:
            theme = self.widget.dark_theme
        else:
            theme = self.widget.theme or ThemeData()

        return theme

    def _material_builder(self, child):
        theme = self._theme_builder()
        child_widget = child
        # TODO: add builder
        # if self.widget.builder != None:
        #     def build_widget(context: BuildContext):
        #         self.widget.builder(context, child)
        #     return Builder(build_widget)
        # TODO: add scaffold messenger
        # child_widget = ScaffoldMessenger(
        #     child=child_widget
        # )
        child_widget = Theme(data=theme, child=child_widget)
        return child_widget

    def build(self, context: BuildContext) -> Widget:
        # very very simplified (flutter uses WidgetsApp inside MaterialApp)
        return DefaultTextStyle(
            style=(self.widget.theme.text_theme.body or TextStyle()) if self.widget.theme != None else TextStyle(),
            child=self.widget.home
        )

class MaterialApp(StatefulWidget):
    """Root container that provides ThemeData to the subtree."""
    # DEFAULT_CSS = '''Align {background: red;}''' #highlight align 
    def __init__(
            self,
            home: Widget,
            title: str = '',
            color: Color | None = None,
            theme: ThemeData | None = None,
            dark_theme: ThemeData | None = None,
            theme_mode: Brightness = Brightness.light, #flutter uses ThemeMode, but Brightness is the same
            id: str | None = None,
            classes: str = ''
        ) -> None:
        """Creates a MaterialApp.

        Args:
            home (Widget): The widget for the default route of the app.
            title (str, optional): A one-line description used by the device to identify the app
                for the user. Defaults to ''.
            color (Color, optional): The primary color to use for the application in the operating
                system interface. Defaults to None.
            theme (ThemeData, optional): Default visual properties, like colors fonts and shapes,
                for this app's material widgets. Defaults to None.
            dark_theme (ThemeData, optional): The `ThemeData` to use when a 'dark mode' is
                requested by the system. Defaults to None.
            theme_mode (Brightness, optional): Determines which theme will be used by the
                application if both `theme` and `darkTheme` are provided. Defaults to
                Brightness.light.
            id (str, optional): Textual CSS id. Defaults to None.
            classes (str, optional): Textual CSS classes. Defaults to ''.
        """
        super().__init__(id=id, classes=classes)
        self.home = home
        self.title = title
        self.color = color
        self.theme = theme
        self.dark_theme = dark_theme
        self.theme_mode = theme_mode

    @staticmethod
    def of(widget: Widget) -> "MaterialApp | None":
        p = widget.parent
        while p is not None:
            if isinstance(p, MaterialApp):
                return p
            p = p.parent
        return None

    def create_state(self) -> State:
        return _MaterialAppState()