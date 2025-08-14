from textual.widget import Widget

class Expanded(Widget):
    def __init__(self, flex: int = 1):
        self.flex = flex
        self.styles.height = f'{flex}fr'
        self.styles.width = f'{flex}fr'