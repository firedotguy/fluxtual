# from textual.widgets import Static
# from textual.containers import Horizontal, Vertical, ScrollableContainer

from fluxtual.enums import TextAlign, FontWeight, TextDecoration
from fluxtual.widgets.text import Text, TextStyle
from fluxtual.widgets.flex import Flexible, Expanded
from fluxtual.widgets.align import Align, Alignment, Center
from fluxtual.color import Colors
from fluxtual.app import MaterialApp
from fluxtual.widgets.base import StatefulWidget, State
from fluxtual.theme import ThemeData, TextTheme
from fluxtual import run
from textual_englyph import EnGlyphText
from textual.containers import Vertical

class FluxtualDemo(StatefulWidget):
    def create_state(self) -> State:
        return FluxtualDemoState()

class FluxtualDemoState(State):
    DEFAULT_CSS = '''Align {background: red;}''' #highlight align

    def build(self, context):
        return Vertical(
            EnGlyphText('one', text_size='x-small', font_name=r'D:\projects\fluxtual\venv\Lib\site-packages\textual_englyph\assets\AtariSmall.ttf'),
            EnGlyphText('two', text_size='small', font_name=r'D:\projects\fluxtual\venv\Lib\site-packages\textual_englyph\assets\AtariSmall.ttf'),
            EnGlyphText('three', text_size='medium', font_name=r'D:\projects\fluxtual\venv\Lib\site-packages\textual_englyph\assets\AtariSmall.ttf'),
            EnGlyphText('four', text_size='large', font_name=r'D:\projects\fluxtual\venv\Lib\site-packages\textual_englyph\assets\AtariSmall.ttf'),
            EnGlyphText('five', text_size='x-large', font_name=r'D:\projects\fluxtual\venv\Lib\site-packages\textual_englyph\assets\AtariSmall.ttf'),
            EnGlyphText('six', text_size='xx-large', font_name=r'D:\projects\fluxtual\venv\Lib\site-packages\textual_englyph\assets\AtariSmall.ttf'),
            EnGlyphText('seven', text_size='xxx-large', font_name=r'D:\projects\fluxtual\venv\Lib\site-packages\textual_englyph\assets\AtariSmall.ttf', ),
            
        )

if __name__ == "__main__":
    run(FluxtualDemo(), CSS = """
Vertical {
    background: darkblue;
}
""")