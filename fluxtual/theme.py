from textual.widget import Widget
from fluxtual.enums import Brightness
from fluxtual.color import Color, Colors
from fluxtual.widgets.text import TextStyle
from fluxtual.widgets.base import StatelessWidget
from fluxtual.context import BuildContext
from fluxtual.inherited import InheritedTheme, InheritedWidget

class TextTheme:
    """Material design text theme."""
    def __init__(
        self,
        body: TextStyle | None = None,
        title: TextStyle | None = None
    ):
        """Creates a text theme that uses the given values. Supports 2/15 flutter arguments."""
        self.body = body
        self.title = title


class ColorScheme:
    """A set of 8 (in flutter 45) colors based on the Material spec that can be used to configure the color properties of most components."""
    def __init__(
        self,
        brightness: Brightness,
        primary: Color,
        on_primary: Color,
        secondary: Color,
        on_secondary: Color,
        surface: Color,
        on_surface: Color,
        tertiary: Color | None = None,
        on_tertiary: Color | None = None
    ):
        """Create a ColorScheme instance from the given colors. Supports 9/49 flutter arguments.

        Args:
            brightness (Brightness): The overall brightness of this color scheme.
            primary (Color): The color displayed most frequently across your app’s screens and
                components.
            on_primary (Color): A color that's clearly legible when drawn on `primary`.
            secondary (Color): An accent color used for less prominent components in the UI, such
                as filter chips, while expanding the opportunity for color expression.
            on_secondary (Color): A color that's clearly legible when drawn on `secondary`.
            surface (Color): The background color for widgets like `Scaffold`.
            on_surface (Color): A color that's clearly legible when drawn on `surface`.
            tertiary (Color, optional): A color used as a contrasting accent that can balance
                `primary` and `secondary` colors or bring heightened attention to an element,
                such as an input field. Defaults to `secondary`.
            on_tertiary (Color, optional): A color that's clearly legible when drawn on
                `tertiary`. Defaults to `onSecondary`.
        """
        self.brightness = brightness
        self.primary = primary
        self.on_primary = on_primary
        self.secondary = secondary
        self.on_secondary = on_secondary
        self.tertiary = tertiary or secondary
        self.on_tertiary = on_tertiary or on_secondary
        self.surface = surface
        self.on_surface = on_surface

    @classmethod
    def light(
        cls,
        primary: Color = Color(0xff6200ee),
        on_primary: Color = Colors.white,
        secondary: Color = Color(0xff03dac6),
        on_secondary: Color = Colors.black,
        surface: Color = Colors.white,
        on_surface: Color = Colors.black,
        tertiary: Color | None = None,
        on_tertiary: Color | None = None
    ):
        """Create a light ColorScheme based on a purple primary color. Supports 9/49 flutter arguments.

        Args:
            primary (Color, optional): The color displayed most frequently across your app’s
                screens and components. Defaults to `Color(0xff6200ee)`.
            on_primary (Color, optional): A color that's clearly legible when drawn on `primary`.
                Defaults to `Colors.white`.
            secondary (Color, optional): An accent color used for less prominent components in the
                UI, such as filter chips, while expanding the opportunity for color expression.
                Defaults to `Color(0xff03dac6)`.
            on_secondary (Color, optional): A color that's clearly legible when drawn on
                `secondary`. Defaults to `Colors.black`
            surface (Color, optional): The background color for widgets like `Scaffold`.
                Defaults to `Colors.white`
            on_surface (Color): A color that's clearly legible when drawn on `surface`.
                Defaults to `Colors.black`
            tertiary (Color, optional): A color used as a contrasting accent that can balance
                `primary` and `secondary` colors or bring heightened attention to an element,
                such as an input field. Defaults to `secondary`.
            on_tertiary (Color, optional): A color that's clearly legible when drawn on
                `tertiary`. Defaults to `onSecondary`.
        """
        return cls(
            brightness=Brightness.light,
            primary=primary,
            on_primary=on_primary,
            secondary=secondary,
            on_secondary=on_secondary,
            surface=surface,
            on_surface=on_surface,
            tertiary=tertiary,
            on_tertiary=on_tertiary
        )

    @classmethod
    def dark(
        cls,
        primary: Color = Color(0xffbb86fc),
        on_primary: Color = Colors.black,
        secondary: Color = Color(0xff03dac6),
        on_secondary: Color = Colors.black,
        surface: Color = Color(0xff121212),
        on_surface: Color = Colors.white,
        tertiary: Color | None = None,
        on_tertiary: Color | None = None
    ):
        """Create the dark color scheme. Supports 9/49 flutter arguments.

        Args:
            primary (Color, optional): The color displayed most frequently across your app’s
                screens and components. Defaults to `Color(0xffbb86fc)`.
            on_primary (Color, optional): A color that's clearly legible when drawn on `primary`.
                Defaults to `Colors.black`.
            secondary (Color, optional): An accent color used for less prominent components in the
                UI, such as filter chips, while expanding the opportunity for color expression.
                Defaults to `Color(0xff03dac6)`.
            on_secondary (Color, optional): A color that's clearly legible when drawn on
                `secondary`. Defaults to `Colors.black`
            surface (Color, optional): The background color for widgets like `Scaffold`.
                Defaults to `Color(0xff121212)`
            on_surface (Color): A color that's clearly legible when drawn on `surface`.
                Defaults to `Colors.white`
            tertiary (Color, optional): A color used as a contrasting accent that can balance
                `primary` and `secondary` colors or bring heightened attention to an element,
                such as an input field. Defaults to `secondary`.
            on_tertiary (Color, optional): A color that's clearly legible when drawn on
                `tertiary`. Defaults to `onSecondary`.
        """
        return cls(
            brightness=Brightness.dark,
            primary=primary,
            on_primary=on_primary,
            secondary=secondary,
            on_secondary=on_secondary,
            surface=surface,
            on_surface=on_surface,
            tertiary=tertiary,
            on_tertiary=on_tertiary
        )


class _InheritedTheme(InheritedTheme):
    def __init__(self, theme: 'Theme', child: Widget):
        super().__init__(child)
        self.theme = theme

    def wrap(self, context: BuildContext, child: Widget) -> Widget:
        return Theme(data=self.theme.data, child=child)

    def update_should_notify(self, old_widget: '_InheritedTheme') -> bool:
        return self.theme.data != old_widget.theme.data

class Theme(StatelessWidget):
    """Applies a theme to descendant widgets."""
    def __init__(
        self,
        data: 'ThemeData',
        child: Widget
    ) -> None:
        """Applies the given theme `data` to `child`. Supports 2/2 flutter arguments.

        Args:
            data (ThemeData): Specifies the color and typography values for descendant widgets.
            child (Widget): The widget below this widget in the tree.
        """
        self.data = data
        self.child = child

    @staticmethod
    def of(context: BuildContext) -> 'ThemeData':
        """The data from the closest `Theme` instance that encloses the given context."""
        inherited_theme = context.depend_on_inherited_widget_of_exact_type(_InheritedTheme)
        theme = (inherited_theme.theme.data if inherited_theme else None) or ThemeData()
        return theme

    def build(self, context: BuildContext) -> Widget:
        return _InheritedTheme(
            theme=self,
            child=self.child
        )
class ThemeData:
    """Defines the configuration of the overall visual Theme for a widget subtree within the app."""
    def __init__(
        self,
        brightness: Brightness = Brightness.dark,
        color_scheme: ColorScheme | None = None,
        text_theme: TextTheme = TextTheme()
    ):
        self.brightness = brightness
        self.color_scheme = color_scheme
        self.text_theme = text_theme

    @classmethod
    def light(cls) -> 'ThemeData':
        """A default light theme."""
        return cls(brightness=Brightness.light)

    @classmethod
    def dark(cls) -> 'ThemeData':
        """A default dark theme."""
        return cls(brightness=Brightness.dark)

    @classmethod
    def fallback(cls) -> "ThemeData":
        """The default color theme. Same as `ThemeData.light`."""
        return cls.light()