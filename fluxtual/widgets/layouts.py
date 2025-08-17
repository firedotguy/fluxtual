from textual.widget import Widget
from textual.containers import Container #TODO: replace to our SizedBox (on ready)
from fluxtual.enums import Axis, MainAxisAlignment, MainAxisSize, CrossAxisAlignment, VerticalDirection


def _create_spacing_box(direction: Axis, spacing: int = 0) -> Container:
    spacing_box = Container()
    if direction == Axis.horizontal:
        spacing_box.styles.width = spacing
    else:
        spacing_box.styles.height = spacing
    return spacing_box

class Flex(Widget):
    """A widget that displays its children in a one-dimensional array."""
    def __init__(
        self,
        direction: Axis,
        main_axis_alignment: MainAxisAlignment = MainAxisAlignment.start,
        main_axis_size: MainAxisSize = MainAxisSize.max,
        cross_axis_alignment: CrossAxisAlignment = CrossAxisAlignment.center,
        vertical_direction: VerticalDirection = VerticalDirection.down,
        spacing: int = 0,
        children: list[Widget] = [],
        id: str | None = None,
        classes: str = ''
    ):
        """Creates a flex layout.

        Args:
            direction (Axis): The direction to use as the main axis.
            main_axis_alignment (MainAxisAlignment, optional): How the children should be placed
                along the main axis. Defaults to MainAxisAlignment.start.
            main_axis_size (MainAxisSize, optional): How much space should be occupied in the main
                axis. Defaults to MainAxisSize.max.
            cross_axis_alignment (CrossAxisAlignment, optional): How the children should be placed
                along the cross axis. Defaults to CrossAxisAlignment.center.
            vertical_direction (VerticalDirection, optional): Determines the order to lay children
                out vertically and how to interpret `start` and `end` in the vertical direction.
                Defaults to VerticalDirection.down.
            spacing (int, optional): How much space to place between children in the main axis. Defaults to 0.
            children (list[Widget], optional): The widgets below this widget in the tree. Defaults to []
            id (str, optional): Textual CSS id. Defaults to None.
            classes (str, optional): Textual CSS classes. Defaults to ''.
        """
        super().__init__(id=id, classes=classes)
        self.direction = direction
        self.main_axis_alignment = main_axis_alignment
        self.main_axis_size = main_axis_size
        self.cross_axis_alignment = cross_axis_alignment
        self.vertical_direction = vertical_direction
        self.spacing = spacing
        self._children = children

        if self.main_axis_size == MainAxisSize.min:
            self.styles.width = 'auto'
            self.styles.height = 'auto'
        else:
            if self.direction == Axis.horizontal:
                self.styles.width = '1fr'
            else:
                self.styles.height = '1fr'

        self._width = None
        self._height = None

    def _apply_between_space(self, spacing):
        spacing_box = _create_spacing_box(self.direction, spacing)

        children = []
        for i, child in enumerate(self._children):
            children.append(child)
            if i != len(self._children) - 1:
                children.append(spacing_box)
        self._children = children

    def on_mount(self):
        if self.direction == Axis.horizontal:
            assert self._width != None
            free_space = self._width
        else:
            assert self._height != None
            free_space = self._height
        leading_space, between_space = self.main_axis_alignment._distribute_space(
            free_space,
            len(self._children),
            self.vertical_direction == VerticalDirection.up,
            self.spacing
        )
        self._apply_between_space(between_space)
        