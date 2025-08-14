from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Container, Horizontal, Vertical

from fluxtual.enums import TextOverflow, TextDecoration, FontStyle
from fluxtual.widgets.text import Text, TextStyle
from fluxtual.color import Colors

class Row(Horizontal):
    def __init__(self, *cells):
        super().__init__(*cells, classes="row")

class HeaderCell(Static):
    def __init__(self, label: str, extra_classes: str = ""):
        super().__init__(label, classes=f"cell header {extra_classes}".strip())

class ModeCell(Static):
    def __init__(self, label: str):
        super().__init__(label, classes="cell mode")

class Cell(Container):
    def __init__(self, child):
        super().__init__(child, classes="cell col")

class FluxtualDemoApp(App):
    CSS = """
    Vertical.table {
        width: 100%;
        height: auto;
    }
    .row {
        width: 100%;
        height: auto;
    }

    .cell {
        padding-bottom: 1;
        padding-right: 1;
        height: 3;
    }

    .mode { width: 18;}
    .col  { width: 30;}

    .header {
        text-style: bold;
        background: #2D2F3A;
        color: #E6E6E6;
        height: 2;
    }

    """

    def compose(self) -> ComposeResult:
        example = "This is long example text for overflow testing."

        tbl = Vertical(
            Row(
                HeaderCell("Mode", extra_classes="mode"),
                HeaderCell("clip", extra_classes="col"),
                HeaderCell("fade", extra_classes="col"),
                HeaderCell("ellipsis", extra_classes="col"),
            ),
            Row(
                ModeCell("with soft wrap"),
                Cell(Text(example, soft_wrap=True, overflow=TextOverflow.clip)),
                Cell(Text(example, soft_wrap=True, overflow=TextOverflow.fade)),
                Cell(Text(example, soft_wrap=True, overflow=TextOverflow.ellipsis)),
            ),
            Row(
                ModeCell("without soft wrap"),
                Cell(Text(example, soft_wrap=False, overflow=TextOverflow.clip)),
                Cell(Text(example, soft_wrap=False, overflow=TextOverflow.fade)),
                Cell(Text(example, soft_wrap=False, overflow=TextOverflow.ellipsis)),
            ),
            classes="table"
        )
        yield tbl

        yield Horizontal(
            Text('This text ', style=TextStyle(color=Colors.amber)),
            Text('styled using ', style=TextStyle(color=Colors.cyan, background_color=Colors.brown)),
            Text('TextStyle.', style=TextStyle(color=Colors.blue, decoration=TextDecoration.underline, font_style=FontStyle.italic))
        )

if __name__ == "__main__":
    FluxtualDemoApp().run()
