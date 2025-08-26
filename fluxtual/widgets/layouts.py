from textual.app import ComposeResult
from textual import log
from textual.geometry import Size
from textual.widget import Widget
from textual.containers import Container #TODO: replace to our SizedBox (on ready)
from fluxtual.enums import Axis, MainAxisAlignment, MainAxisSize, CrossAxisAlignment, VerticalDirection
from fluxtual.utils import flip_axis

def _create_spacing_box(direction: Axis, spacing: int = 0) -> Container:
    spacing_box = Container(classes='fluxtual-spacing-box')
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
        self._host = Container()

        self._host.styles.layout = "horizontal" if self.direction == Axis.horizontal else "vertical"
        self.styles.width = 'auto'
        self.styles.height = 'auto'

        self._width = None
        self._height = None

    def _apply_between_space(self, spacing: int) -> None:
        children = []
        for i, child in enumerate(self._children):
            if child.classes == 'fluxtual-spacing-box':
                continue
            children.append(child)
            if i != len(self._children) - 1 and i != 0:
                children.append(_create_spacing_box(self.direction, spacing))
        self._children = children
        log('between', spacing)

    def _apply_leading_space(self, spacing: int, direction: Axis = Axis.horizontal) -> None:
        if len(self._children) > 0:
            if self._children[0].classes == 'fluxtual-spacing-box':
                self._children.pop(0)
        self._children.insert(0, _create_spacing_box(direction, spacing))
        log('leading', spacing)

    def _apply_spacing(self) -> None:
        # apply main spacing
        if self.direction == Axis.horizontal:
            assert self.size.width is not None
            free_space = self.size.width
        else:
            assert self.size.height is not None
            free_space = self.size.height

        leading_space, between_space = self.main_axis_alignment._distribute_space(
            free_space,
            len(self._children),
            self.vertical_direction == VerticalDirection.up,
            self.spacing
        )
        if between_space > 0:
            self._apply_between_space(between_space)
        if leading_space > 0:
            self._apply_leading_space(leading_space, self.direction)

        # apply cross spacing
        if self.direction == Axis.horizontal:
            assert self.size.height is not None
            free_space = self.size.height
        else:
            assert self.size.width is not None
            free_space = self.size.width

        leading_space = self.cross_axis_alignment._get_child_cross_axis_offest(
            free_space,
            self.vertical_direction == VerticalDirection.up
        )
        self._apply_leading_space(leading_space, flip_axis(self.direction))


    def get_content_width(self, container: Size, viewport: Size) -> int:
        if self.direction == Axis.horizontal:
            if self.main_axis_size == MainAxisSize.max:
                return container.width
            return sum(c.get_content_width(container, viewport) for c in self._children)
        else:
            if self.cross_axis_alignment != CrossAxisAlignment.start:
                return container.width
            return max((c.get_content_width(container, viewport) for c in self._children), default=0)

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        if self.direction == Axis.vertical:
            if self.main_axis_size == MainAxisSize.max:
                return container.height
            return sum(
                c.get_content_height(container, viewport, c.get_content_width(container, viewport))
                for c in self._children
            )
        else:
            if self.cross_axis_alignment == CrossAxisAlignment.stretch:
                return container.height
            return max(
                (c.get_content_height(container, viewport, c.get_content_width(container, viewport))
                for c in self._children),
                default=0
            )

    async def _rebuild_host(self) -> None:
        self._apply_spacing()
        self._host.remove_children()
        await self._host.mount(*self._children)
        self.refresh(layout=True)

    def compose(self) -> ComposeResult:
        yield self._host

    async def on_mount(self) -> None:
        await self._host.mount(*self._children) # firstly paint without spacing
        self.call_after_refresh(self._rebuild_host)

    async def watch_size(self, size: Size) -> None:
        await self._rebuild_host()