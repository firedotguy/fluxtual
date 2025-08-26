from fluxtual.enums import *
from fluxtual.widgets.text import Text, TextStyle
from fluxtual.widgets.layouts import Flex
from fluxtual.color import Colors
from fluxtual.app import MaterialApp
from fluxtual.widgets.base import StatefulWidget, State
from fluxtual.theme import ThemeData, TextTheme
from fluxtual import run_app


class FluxtualDemo(StatefulWidget):
    def create_state(self) -> State:
        return FluxtualDemoState()

class FluxtualDemoState(State):
    def build(self, context) -> MaterialApp:
        return MaterialApp(
            theme=ThemeData(
                text_theme=TextTheme(
                    body=TextStyle(color=Colors.white)
                )
            ),
            home=Flex(
                direction=Axis.horizontal,
                main_axis_alignment=MainAxisAlignment.space_between,
                children=[
                    Text('this text used for test'),
                    Text('Text number two'),
                    Text('Text number three')
                ]
            )
        )


if __name__ == "__main__":
    run_app(FluxtualDemo(), CSS = """
Flex {
    background: darkblue;
}
Text {
    background: red;
}
""")