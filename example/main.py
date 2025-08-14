from fluxtual.enums import TextOverflow
from fluxtual.widgets.text import Text
from textual.app import App, ComposeResult
from textual.containers import Container

class FluxtualApp(App):
    CSS = '''
    Container {
        width: 10;
        height: 2;
        background: #008D64
    }
    '''
    def compose(self) -> ComposeResult:
        yield Container(
            Text('Welcome to the Fluxtual', soft_wrap=True, overflow=TextOverflow.ellipsis)
        )
        yield Container(
            Text('123456789123456789123456789', soft_wrap=False)
        )

if __name__ == '__main__':
    FluxtualApp().run()