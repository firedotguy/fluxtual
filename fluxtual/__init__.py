from textual.app import App, ComposeResult
from textual.widget import Widget
from fluxtual.widgets.base import StatefulWidget, StatelessWidget, BuildContext

__author__ = 'firedotguy'
__version__ = '0.1.0'
__license__ = 'MIT'

class _ConstMeta(type):
    """Metaclass that forbids reassigning declared constants."""
    _frozen_fields: set[str] = set()

    def __setattr__(cls, name, value):
        if name in cls._frozen_fields:
            raise AttributeError(f"Cannot reassign constant '{name}' of {cls.__name__}")
        super().__setattr__(name, value)

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
    """Copy of `run_app`. Deprected - use `run_app` instead."""
    run_app(widget, CSS)