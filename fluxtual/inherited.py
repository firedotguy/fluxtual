from textual.containers import Container
from textual.widget import Widget
from fluxtual.widgets.base import StatelessWidget
from fluxtual.context import BuildContext

class InheritedWidget(Container):
    """Base class for widgets that efficiently propagate information down the tree."""
    def __init__(self, child: Widget):
        """Abstract const constructor. This constructor enables subclasses to provide const
            constructors so that they can be used in const expressions. Supports 1/1
            flutter arguments.

        Args:
            child (Widget): The widget below this widget in the tree.
        """
        super().__init__(child)
        self.child = child

    def update_should_notify(self, old_widget: 'InheritedWidget') -> bool:
        """Whether the framework should notify widgets that inherit from this widget. Supports
            1/1 flutter arguments."""
        return True


class _CaptureAll(StatelessWidget):
    def __init__(self, themes: list['InheritedTheme'], child: Widget):
        super().__init__()
        self.themes = themes
        self.child = child

    def build(self, context: BuildContext) -> Widget:
        wrapped_child = self.child
        for theme in self.themes:
            wrapped_child = theme.wrap(context, wrapped_child)
        return wrapped_child

class CapturedThemes:
    """Stores a list of captured `InheritedTheme`s that can be wrapped around a child `Widget`."""
    def __init__(self, themes: list['InheritedTheme']) -> None:
        """Supprots 1/1 flutter aguments."""
        self._themes = themes

    def wrap(self, child: Widget) -> Widget:
        """Wraps a `child` `Widget` in the `InheritedTheme`s captured in this object. Supports
            1/1 flutter arguments."""
        return _CaptureAll(self._themes, child)

class InheritedTheme(InheritedWidget):
    """An `InheritedWidget` that defines visual properties like colors and text styles, which
        the `child`'s subtree depends on."""
    def wrap(self, context: BuildContext, child: Widget) -> Widget:
        """Return a copy of this inherited theme with the specified `child`. Supports 2/2 flutter
            arguments."""
        return child

    @staticmethod
    def capture(_from: BuildContext, to: BuildContext | None = None) -> CapturedThemes:
        """Returns a `CapturedThemes` object that includes all the `InheritedTheme`s between the
            given `from` and `to` `BuildContext`s. Supports 2/2 flutter arguments."""
        if _from == to:
            return CapturedThemes([])

        themes = []
        theme_types = []
        def visitor(ancestor):
            if to is not None and ancestor is to.widget:
                return False
            if isinstance(ancestor, InheritedTheme):
                theme_type = type(ancestor)
                if theme_type not in theme_types:
                    theme_types.append(theme_type)
                    themes.append(ancestor)
            return True
        _from.visit_ancestor_element(visitor)
        return CapturedThemes(themes)

    @staticmethod
    def capture_all(context: BuildContext, child: Widget, to: BuildContext | None = None):
        """Returns a widget that will `wrap` `child` in all of the inherited themes which are
            present between `context` and the specified `to` `BuildContext`. Supports 3/3
            flutter arguments."""
        return InheritedTheme.capture(_from=context, to=to).wrap(child)
