from typing import Generic, TypeVar, cast

from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Container

from fluxtual.context import BuildContext
from fluxtual.exceptions import FlutterError

W = TypeVar("W", bound="StatefulWidget")
S = TypeVar("S", bound="State")

class StatelessWidget(Widget):
    """A widget that does not require mutable state."""
    def build(self, context: BuildContext) -> Widget:
        """Describes the part of the user interface represented by this widget."""
        raise NotImplementedError

    def compose(self) -> ComposeResult:
        """Connection to Textual API"""
        yield self.build(BuildContext(self))


class State(Generic[W]):
    """The logic and internal state for a `StatefulWidget`."""
    _widget: W | None = None
    mounted: bool

    def _bind(self, widget: W) -> None:
        self._widget = widget

    @property
    def widget(self) -> W:
        assert self._widget is not None, "State.widget is not bound yet"
        return self._widget

    def build(self, context: BuildContext) -> Widget:
        raise NotImplementedError

    def init_state(self) -> None:
        pass

    def set_state(self, mutate) -> None:
        mutate()
        self.widget.call_later(self.widget._rebuild)

class StatefulWidget(Widget, Generic[S]):
    """A widget that has mutable state."""
    _state: S | None = None
    _host: Container | None = None
    def __init__(self, id: str | None = None, classes: str = ''):
        super().__init__(id=id, classes=classes)

    def create_state(self) -> S:
        """Creates the mutable state for this widget at a given location in the tree."""
        raise NotImplementedError

    def compose(self) -> ComposeResult:
        """Create widgets in Textual."""
        self._host = Container()
        yield self._host

    async def on_mount(self) -> None:
        self._state = self.create_state()
        self._state._bind(self)
        await self._rebuild(initial=True)

    async def _rebuild(self, *, initial: bool = False) -> None:
        """Rebuild current widget tree."""
        assert self._host is not None
        assert self._state is not None

        try:
            tree = self._state.build(BuildContext(self))
        except TypeError:
            raise TypeError('Build method must have "context" argument')
        self._host.remove_children()
        await self._host.mount(tree)

        if initial:
            self._state.init_state()

    @property
    def state(self) -> S:
        assert self._state is not None, "State is not initialized yet"
        return cast(S, self._state)


class _NullWidget(StatelessWidget):
    def build(self, context: BuildContext) -> Widget:
        raise FlutterError(
            'A DefaultTextStyle constructed with DefaultTextStyle.fallback cannot be incorporated into the widget tree, '
            'it is meant only to provide a fallback value returned by DefaultTextStyle.of() '
            'when no enclosing default text style is present in a BuildContext.',
        )