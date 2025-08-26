from textual.app import App, ComposeResult
from textual.widget import Widget
from fluxtual.enums import Axis
from fluxtual.widgets.base import StatefulWidget, StatelessWidget

def flip_axis(axis: Axis) -> Axis:
    """Returns the opposite of the given `Axis`."""
    if axis == Axis.horizontal: return Axis.vertical
    else: return Axis.horizontal

class _FluxtualApp(App):
    def __init__(self, widget: Widget, css: str):
        super().__init__()
        self.widget = widget
        self.css = css

    def compose(self) -> ComposeResult:
        yield self.widget

    def on_mount(self):
        if self.css:
            self.stylesheet.add_source(self.css)
            self.refresh_css()

def run_app(widget: Widget, CSS: str = '') -> None:
    """Inflate the given widget and attach it to the view.

    Args:
        widget (Widget): Main app widget. Recommend to use `MaterialApp`.
        CSS (str, optional): Textual CSS source for things that fluxtual not support. Defaults to ''.
    """
    _FluxtualApp(widget, CSS).run()

def run(widget: StatefulWidget | StatelessWidget, CSS: str = '') -> None:
    """Copy of `run_app`. Deprecated - use `run_app` instead."""
    run_app(widget, CSS)