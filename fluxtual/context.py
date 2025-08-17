from textual.widget import Widget
from typing import Type, TypeVar

T = TypeVar("T", bound=Widget)

class BuildContext:
    """Lightweight Flutter-like context for a widget."""
    def __init__(self, widget: Widget):
        self.widget = widget

    def find_ancestor_widget_of_type(self, widget_type: Type[T]) -> T | None:
        """Walk up the widget tree to find the first ancestor of a given type."""
        p = self.widget.parent
        while p is not None:
            if isinstance(p, widget_type):
                return p
            p = p.parent
        return None

    def depend_on_inherited_widget_of_exact_type(self, widget_type: Type[T]) -> T | None:
        """Returns the nearest widget of the given `InheritedWidget` subclass `T` or null if an
            appropriate ancestor is not found."""
        p = self.widget.parent
        while p is not None:
            if type(p) is widget_type:
                return p
            p = p.parent
        return None

    def visit_ancestor_element(self, visitor) -> None:
        """Walks the ancestor chain, starting with the parent of this build context's widget,
            invoking the argument for each ancestor."""
        p = self.widget.parent
        while p is not None:
            if visitor(p) is False:
                break
            p = p.parent