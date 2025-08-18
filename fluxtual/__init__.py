from textual.app import App, ComposeResult
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
    def __init__(self, widget: StatefulWidget | StatelessWidget):
        super().__init__()
        self.widget = widget

    def compose(self) -> ComposeResult:
        yield self.widget

def run(widget: StatefulWidget | StatelessWidget) -> None:
    _FluxtualApp(widget).run()