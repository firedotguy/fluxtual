# from textual.widgets import Static
# from textual.containers import Horizontal, Vertical, ScrollableContainer

from fluxtual.enums import TextAlign, FontWeight, TextDecoration
from fluxtual.widgets.text import Text, TextStyle
from fluxtual.widgets.flex import Flexible, Expanded
from fluxtual.widgets.align import Align, Alignment
from fluxtual.color import Colors
from fluxtual.app import MaterialApp
from fluxtual.widgets.base import StatefulWidget, State
from fluxtual.theme import ThemeData, TextTheme
from fluxtual import run


class FluxtualDemo(StatefulWidget):
    def create_state(self) -> State:
        return FluxtualDemoState()

class FluxtualDemoState(State):
    DEFAULT_CSS = '''Align {background: red;}''' #highlight align

    def build(self, context) -> MaterialApp:
        return MaterialApp(
            theme=ThemeData(
                text_theme=TextTheme(
                    body=TextStyle(color=Colors.white)
                )
            ),
            home=Align(Text('this text used for test', text_align=TextAlign.justify), alignment=Alignment.center)
        )

if __name__ == "__main__":
    run(FluxtualDemo())
