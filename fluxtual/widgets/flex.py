from textual.containers import Container
from textual.widget import Widget
from fluxtual.enums import FlexFit

class Flexible(Container):
    """A widget that controls how a child of a Row, Column, or Flex flexes."""

    def __init__(
        self,
        child: Widget,
        flex: int = 1,
        fit: FlexFit = FlexFit.loose,
        id: str | None = None,
        classes: str = ''
    ) -> None:
        """Creates a widget that controls how a child of a Row, Column, or Flex flexes. Supports 2/2 flutter arguments.

        Args:
            child (Widget): The widget below this widget in the tree.
            flex (int, optional): The flex factor to use for this child. Defaults to 1.
            fit (FlexFit, optional): How a flexible child is inscribed into the available space. Defaults to FlexFit.loose.
            id (str, optional): Textual CSS id. Defaults to None.
            classes (str, optional): Textual CSS classes. Defaults to ''.
        """
        super().__init__(child, id=id, classes=classes)
        self.flex = flex
        self.fit = fit

        if fit == FlexFit.loose:
            self.styles.height = "auto"
            self.styles.max_height = f"{flex}fr"
            self.styles.width = "auto"
            self.styles.max_width = f"{flex}fr"
        else:
            self.styles.width = f"{flex}fr"
            self.styles.height = f"{flex}fr"

class Expanded(Flexible):
    """A widget that expands a child of a Row, Column, or Flex so that the child fills the available space."""

    def __init__(
        self,
        child: Widget,
        flex: int = 1,
        id: str | None = None,
        classes: str = ''
    ) -> None:
        """Creates a widget that expands a child of a Row, Column, or Flex so that the child. Supports 1/1 flutter arguments.
        fills the available space along the flex widget's main axis.

        Args:
            child (Widget): The widget below this widget in the tree.
            flex (int, optional): The flex factor to use for this child. Defaults to 1.
            fit (FlexFit, optional): How a flexible child is inscribed into the available space. Defaults to FlexFit.loose.
            id (str, optional): Textual CSS id. Defaults to None.
            classes (str, optional): Textual CSS classes. Defaults to ''.
        """
        super().__init__(child, flex=flex, fit=FlexFit.tight, id=id, classes=classes)