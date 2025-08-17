from textual.app import App, ComposeResult
from fluxtual.widgets.base import StatefulWidget

class _FluxtualApp(App):
    def __init__(self, widget: StatefulWidget):
        super().__init__()
        self.widget = widget

    def compose(self) -> ComposeResult:
        yield self.widget

def run(widget: StatefulWidget) -> None:
    _FluxtualApp(widget).run()