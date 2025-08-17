from fluxtual.widgets.base import StatelessWidget
from fluxtual.context import BuildContext

class Builder(StatelessWidget):
    """A stateless utility widget whose `build` method uses its `builder` callback to create
        the widget's child."""
    def __init__(self, builder):
        """Creates a widget that delegates its build to a callback.

        Args:
            builder (Callable[[BuildContext], Widget]): Called to obtain the child widget.
        """
        self.builder = builder

    def build(self, context: BuildContext):
        return self.builder(context)