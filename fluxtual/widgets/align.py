from typing import ClassVar
from textual.geometry import Size
from textual.widget import Widget
from textual import log
from fluxtual.enums import TextAlign
from fluxtual import _ConstMeta

class AlignmentGeometry:
    """Base class for `Alignment` that allows for text-direction aware resolution."""
    _x: float
    _y: float
    _start: float

    def __init__(self):
        """Abstract const constructor. This constructor enables subclasses to provide const
            constructors so that they can be used in const expressions."""
        pass

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def start(self):
        return self._start

    @classmethod
    def xy(cls, x: float, y: float) -> 'Alignment':
        return Alignment(x, y)

    def resolve(self) -> 'Alignment':
        """Convert this instance into an `Alignment`, which uses literal coordinates (the `x`
            coordinate being explicitly a distance from the left). Supports 0/1 flutter
            arguments."""
        ...

    def __neg__(self) -> 'AlignmentGeometry':
        """Returns the negation of the given `AlignmentGeometry` object."""
        ...
    def __mul__(self, other: float) -> 'AlignmentGeometry':
        """Scales the `AlignmentGeometry` object in each dimension by the given factor."""
        ...

    def __truediv__(self, other: float) -> 'AlignmentGeometry':
        """Divides the `AlignmentGeometry` object in each dimension by the given factor."""
        ...

    def __floordiv__(self, other: float) -> 'AlignmentGeometry':
        """Integer divides the `AlignmentGeometry` object in each dimension by the given factor."""
        ...

    def __mod__(self, other: float) -> 'AlignmentGeometry':
        """Computes the remainder in each dimension by the given factor."""
        ...

    def __eq__(self, other: object) -> bool:
        return other is AlignmentGeometry and other._x == self._x and other._start == self._start and other._y == self._y

class Alignment(AlignmentGeometry, metaclass=_ConstMeta):
    """A point within a rectangle."""
    def __init__(self, x: float, y: float):
        """Creates an alignment. Supports 2/2 flutter arguments.

        Args:
            x (float): The distance fraction in the horizontal direction.
            y (float): The distance fraction in the vertical direction.
        """
        self._x = x
        self._y = y

    @property
    def start(self) -> float:
        return 0.0

    def resolve(self) -> 'Alignment':
        """Convert this instance into an `Alignment`, which uses literal coordinates (the `x`
            coordinate being explicitly a distance from the left). Supports 0/1 flutter
            arguments."""
        return self

    def __sub__(self, other: 'Alignment') -> 'Alignment':
        """Returns the difference between two `Alignment`s."""
        ...

    def __add__(self, other: 'Alignment') -> 'Alignment':
        """Returns the sum of two `Alignment`s."""
        ...

    def __neg__(self) -> 'Alignment':
        """Returns the negation of the given `Alignment`."""
        return Alignment(-self.x, -self.y)

    def __mul__(self, other: float) -> 'Alignment':
        """Scales the `Alignment` object in each dimension by the given factor."""
        return Alignment(self.x * other, self.y * other)

    def __truediv__(self, other: float) -> 'Alignment':
        """Divides the `Alignment` object in each dimension by the given factor."""
        return Alignment(self.x / other, self.y / other)

    def __floordiv__(self, other: float) -> 'Alignment':
        """Integer divides the `Alignment` object in each dimension by the given factor."""
        return Alignment(float(self.x // other), float(self.y // other))

    def __mod__(self, other: float) -> 'Alignment':
        """Computes the remainder in each dimension by the given factor."""
        return Alignment(self.x % other, self.y % other)

    @staticmethod
    def _stringify(x: float, y: float) -> str:
        match (x, y):
            case (-1.0, -1.0):
                return "Alignment.topLeft"
            case (0.0, -1.0):
                return "Alignment.topCenter"
            case (1.0, -1.0):
                return "Alignment.topRight"
            case (-1.0, 0.0):
                return "Alignment.centerLeft"
            case (0.0, 0.0):
                return "Alignment.center"
            case (1.0, 0.0):
                return "Alignment.centerRight"
            case (-1.0, 1.0):
                return "Alignment.bottomLeft"
            case (0.0, 1.0):
                return "Alignment.bottomCenter"
            case (1.0, 1.0):
                return "Alignment.bottomRight"
            case _:
                return f"Alignment({x:.1f}, {y:.1f})"

    def __str__(self) -> str:
        return self._stringify(self.x, self.y)

    def __repr__(self) -> str:
        return str(self)

    top_left: ClassVar["Alignment"]
    top_center: ClassVar["Alignment"]
    top_right: ClassVar["Alignment"]
    center_left: ClassVar["Alignment"]
    center: ClassVar["Alignment"]
    center_right: ClassVar["Alignment"]
    bottom_left: ClassVar["Alignment"]
    bottom_center: ClassVar["Alignment"]
    bottom_right: ClassVar["Alignment"]

Alignment.top_left = Alignment(-1.0, -1.0)
Alignment.top_center = Alignment(0.0, -1.0)
Alignment.top_right = Alignment(1.0, -1.0)
Alignment.center_left = Alignment(-1.0, 0.0)
Alignment.center = Alignment(0.0, 0.0)
Alignment.center_right = Alignment(1.0, 0.0)
Alignment.bottom_left = Alignment(-1.0, 1.0)
Alignment.bottom_center = Alignment(0.0, 1.0)
Alignment.bottom_right = Alignment(1.0, 1.0)


class Align(Widget): #in flutter SingleChildRenderObjectWidget -> RenderObjectWidget -> Widget, here is simplified
    """A widget that aligns its child within itself and optionally sizes itself based on the
        child's size."""
    def __init__(
        self,
        child: Widget,
        alignment: Alignment = Alignment.center,
        width_factor: float | None = None,
        height_factor: float | None = None,
        id: str | None = None,
        classes: str = ''
    ) -> None:
        """Creates an alignment widget. Supports 4/4 flutter arguments.

        Args:
            child (Widget): The widget below this widget in the tree.
            alignment (Alignment, optional): How to align the child. Defaults to Alignment.center.
            width_factor (float, optional): If non-null, sets its width to the child's width
                multiplied by this factor. Defaults to None.
            height_factor (float, optional): If non-null, sets its height to the child's height
                multiplied by this factor. Defaults to None.
            id (str, optional): Textual CSS id. Defaults to None.
            classes (str, optional): Textual CSS classes. Defaults to ''.
        """
        super().__init__(child, id=id, classes=classes)
        assert width_factor == None or width_factor >= 0
        assert height_factor == None or height_factor >= 0
        self.child = child
        self.alignment = alignment
        self.width_factor = width_factor
        self.height_factor = height_factor

        self.styles.width = 'auto'
        self.styles.height = 'auto'

    def _reflow(self, container_size, viewport):
        #use variables instead of textual size because we need to changes it (textual don't allows it idk why)
        child_width = self.child.get_content_width(container_size, viewport)
        child_height = self.child.get_content_height(container_size, viewport, child_width)
        container_width = container_size.width
        container_height = container_size.height

        #set chils size * factor instead of maximum size
        if self.height_factor is not None:
            container_height = child_height * self.height_factor
        if self.width_factor is not None:
            container_width = child_width * self.width_factor

        free_width = max(0, container_width - child_width)
        free_height = max(0, container_height - child_height)
        left_margin = round(free_width * (self.alignment.x + 1) * 0.5)
        top_margin = round(free_height * (self.alignment.y + 1) * 0.5)

        self.child.styles.margin = (top_margin, 0, 0, left_margin)

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        self._reflow(container, viewport)
        if self.height_factor is None:
            return container.height
        return round(
            self.child.get_content_height(
                container,
                viewport,
                self._child_width or self.child.get_content_width(container, viewport))
            * self.height_factor
        )

    def get_content_width(self, container: Size, viewport: Size) -> int:
        if self.width_factor is None:
            return container.width
        self._child_width = self.child.get_content_width(container, viewport) #for use in get_content_height
        return round(self._child_width * self.width_factor)

    def compose(self):
        yield self.child

class Center(Align):
    """A widget that centers its child within itself."""
    def __init__(
            self,
            child: Widget,
            id: str | None = None,
            classes: str = ''
        ) -> None:
        """Creates a widget that centers its child.

        Args:
            child (Widget): The widget below this widget in the tree.
            id (str, optional): textual CSS id. Defaults to None.
            classes (str, optional): textual CSS classes. Defaults to ''.
        """
        super().__init__(child, Alignment.center, None, None, id, classes)

def _text_align_to_alignment(text_align: TextAlign) -> Alignment | None: #flutter hasn't this one, it uses only in fluxtual _TextAlign
        if text_align == TextAlign.center:
            return Alignment.top_center
        elif text_align == TextAlign.left:
            return Alignment.top_left
        elif text_align == TextAlign.right:
            return Alignment.top_right
        # if its TextAlign.justify, return None

class _TextAlign(Align): #flutter hasn't this one, it uses for align text
    """Custom wrapper to align text"""
    def __init__(self, child: Widget, text_align: TextAlign = TextAlign.left):
        super().__init__(child, _text_align_to_alignment(text_align) or Alignment.top_left)
        self.is_justify = _text_align_to_alignment(text_align) is None

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        self._reflow(container, viewport)
        return self.child.get_content_height(container, viewport, width)

    def get_content_width(self, container: Size, viewport: Size) -> int:
        if self.alignment != Alignment.top_left or self.is_justify:
            return container.width
        return self.child.get_content_width(container, viewport)