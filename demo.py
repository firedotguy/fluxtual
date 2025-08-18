# from textual.widgets import Static
# from textual.containers import Horizontal, Vertical, ScrollableContainer

from fluxtual.enums import TextAlign
from fluxtual.widgets.text import Text, TextStyle
from fluxtual.widgets.flex import Flexible, Expanded
from fluxtual.color import Colors
from fluxtual.app import MaterialApp
from fluxtual.widgets.base import StatefulWidget, State
from fluxtual.theme import ThemeData, TextTheme
from fluxtual import run


class FluxtualDemo(StatefulWidget):
    def create_state(self) -> State:
        return FluxtualDemoState()

class FluxtualDemoState(State):
    #remove css when fluxtual widgets is enough
    #"""
    # Vertical.table {
    #     width: 100%;
    # }
    # Horizontal {
    #     height: auto;
    # }
    # Vertical {
    #     height: auto;
    # }
    # .row {
    #     width: 100%;
    #     height: auto;
    # }

    # .cell {
    #     padding-bottom: 1;
    #     padding-right: 1;
    #     height: 3;
    # }

    # .mode { width: 18;}
    # .col  { width: 30;}

    # .header {
    #     text-style: bold;
    #     background: #2D2F3A;
    #     height: 2;
    # }
    # .title {
    #     text-style: bold;
    #     padding: 0 1;
    #     height: 1;
    #     width: 100%;
    # }
    # .label-chip {
    #     background: #3a3d50;
    #     color: #d7d7ff;
    #     height: 1;
    #     padding: 0 1;
    #     text-style: bold;
    # }
    # .flex-box {
    #     background: #1F2230;
    #     max-height: 10;
    # }

    # """

    def build(self, context):
        # textual build
        # example = "This is long example text for overflow testing."

        # return ScrollableContainer(
        #     Static('Text: Example with TextStyle', classes='title'),
        #     Horizontal(
        #         Text('This text ', style=TextStyle(color=Colors.amber)),
        #         Text('styled using ', style=TextStyle(color=Colors.cyan, background_color=Colors.brown)),
        #         Text('TextStyle.', style=TextStyle(color=Colors.blue, decoration=TextDecoration.underline, font_style=FontStyle.italic))
        #     ),
        #     Static('Text: difference between overflowing variants', classes='title'),
        #     Vertical(
        #         Horizontal(
        #             Static("Mode", classes="cell header mode"),
        #             Static("clip", classes="cell header col"),
        #             Static("fade", classes="cell header col"),
        #             Static("ellipsis", classes="cell header col"),
        #             classes='row'
        #         ),
        #         Horizontal(
        #             Static("with soft wrap", classes='cell mode'),
        #             Text(example, soft_wrap=True, overflow=TextOverflow.clip, classes='cell col'),
        #             Text(example, soft_wrap=True, overflow=TextOverflow.fade, classes='cell col'),
        #             Text(example, soft_wrap=True, overflow=TextOverflow.ellipsis, classes='cell col'),
        #             classes='row'
        #         ),
        #         Horizontal(
        #             Static("without soft wrap", classes='cell mode'),
        #             Text(example, soft_wrap=False, overflow=TextOverflow.clip, classes='cell col'),
        #             Text(example, soft_wrap=False, overflow=TextOverflow.fade, classes='cell col'),
        #             Text(example, soft_wrap=False, overflow=TextOverflow.ellipsis, classes='cell col'),
        #             classes='row'
        #         ),
        #         classes="table"
        #     ),
        #     Static('Expanded / Flexible', classes='title'),
        #     Flexible(
        #         Vertical(
        #             Static("Flexible(loose, 1fr)", classes="label-chip"),
        #             Text("Short text (loose) — grows only if there is room.", soft_wrap=True)
        #         ),
        #         classes='flex-box'
        #     ),
        #     Expanded(
        #         Vertical(
        #             Static("Expanded(tight, 1fr)", classes="label-chip"),
        #             Text("Expanded fills exactly its fr share.", soft_wrap=True)
        #         ),
        #         classes='flex-box'
        #     ),
        # )
        return MaterialApp(
            theme=ThemeData(
                text_theme=TextTheme(
                    body=TextStyle(color=Colors.amber, background_color=Colors.indigo)
                )
            ),
            home=Align(Text('Hello ember?', text_align=TextAlign.justify))
        )

if __name__ == "__main__":
    run(FluxtualDemo())
