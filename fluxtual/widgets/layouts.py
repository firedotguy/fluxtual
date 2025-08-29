from textual.app import ComposeResult
from textual import log
from textual.geometry import Size
from textual.widget import Widget
from textual.containers import Container #TODO: replace to our SizedBox (on ready)
from fluxtual.enums import Axis, MainAxisAlignment, MainAxisSize, CrossAxisAlignment, VerticalDirection
from fluxtual.utils import flip_axis
from asyncio import sleep

def _create_spacing_box(direction: Axis, spacing: int = 0, cross_spacing: int = 0) -> Container:
    spacing_box = Container(classes='fluxtual-spacing-box')
    if direction == Axis.horizontal:
        spacing_box.styles.width = spacing
        spacing_box.styles.height = cross_spacing
    else:
        spacing_box.styles.height = spacing
        spacing_box.styles.width = cross_spacing
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
    ) -> None:
        """Creates a flex layout. Supports 7/10 flutter arguments.

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
            children (list[Widget], optional): The widgets below this widget in the tree. Defaults to [].
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

        self.styles.layout = "horizontal" if self.direction == Axis.horizontal else "vertical"
        self.styles.width = 'auto'
        self.styles.height = 'auto'

        self._width = None
        self._height = None

        self._laid_out = False

    def _apply_between_space(self, spacing: int) -> None:
        children = []
        for i, child in enumerate(self._children):
            if child.classes == 'fluxtual-spacing-box':
                continue
            children.append(child)
            if i != len(self._children) - 1:
                children.append(_create_spacing_box(self.direction, spacing))
        self._children = children

    # def _apply_leading_space(self, spacing: int) -> None:
    #     if len(self._children) > 0:
    #         if self._children[0].classes == 'fluxtual-spacing-box':
    #             self._children.pop(0)
    #     self._children.insert(0, _create_spacing_box(self.direction, spacing, 0))

    def _apply_spacing(self) -> None:
        # apply main spacing
        if self.direction == Axis.horizontal:
            children_width = sum(child.get_content_width(self.size, self.app.size) for child in self._children)\
                + self.spacing * (len(self._children) - 1)
            children_height = max(
                child.get_content_height(
                    self.size,
                    self.app.size,
                    child.get_content_width(self.size, self.app.size))
                for child in self._children)
        else:
            children_width = max(child.get_content_width(self.size, self.app.size) for child in self._children)
            children_height = sum(
                child.get_content_height(
                    self.size,
                    self.app.size,
                    child.get_content_width(self.size, self.app.size))
                for child in self._children) + self.spacing * (len(self._children) - 1)

        if self.direction == Axis.horizontal:
            assert self._width is not None
            free_space = self._width - children_width
        else:
            assert self._height is not None
            free_space = self._height - children_height

        leading_space, between_space = self.main_axis_alignment._distribute_space(
            free_space,
            len(self._children),
            self.vertical_direction == VerticalDirection.up,
            self.spacing
        )
        if between_space > 0:
            self._apply_between_space(between_space)
        # replaced to padding
        # if leading_space > 0:
        #     self._apply_leading_space(leading_space)

        # apply cross spacing
        if self.direction == Axis.horizontal:
            assert self._height is not None
            free_space = self._height - children_height
        else:
            assert self._width is not None
            free_space = self._width - children_width
        cross_leading_space = self.cross_axis_alignment._get_child_cross_axis_offest(
            free_space,
            self.vertical_direction == VerticalDirection.up
        )
        if self.direction == Axis.horizontal:
            self.styles.padding = (cross_leading_space, 0, 0, leading_space)
        else:
            self.styles.padding = (leading_space, 0, 0, cross_leading_space)
        self.refresh(recompose=True)
        self._laid_out = True


    def get_content_width(self, container: Size, viewport: Size) -> int:
        if self._laid_out == True:
            assert self._width != None
            return self._width
        if self.direction == Axis.horizontal:
            if self.main_axis_size == MainAxisSize.max:
                return container.width
            return sum(c.get_content_width(container, viewport) for c in self._children)
        else:
            if self.cross_axis_alignment != CrossAxisAlignment.start:
                return container.width
            return max((c.get_content_width(container, viewport) for c in self._children), default=0)

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        if self._laid_out == True:
            assert self._height != None
            return self._height
        self._width = width
        if self.direction == Axis.vertical:
            if self.main_axis_size == MainAxisSize.max:
                self._height = container.height
            else:
                self._height = sum(
                    c.get_content_height(container, viewport, c.get_content_width(container, viewport))
                    for c in self._children
                )
        else:
            if self.cross_axis_alignment != CrossAxisAlignment.start:
                self._height = container.height
            else:
                self._height = max(
                    (c.get_content_height(container, viewport, c.get_content_width(container, viewport))
                    for c in self._children),
                    default=0
                )
        self._apply_spacing()
        return self._height

    def compose(self) -> ComposeResult:
        yield from self._children