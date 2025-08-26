from enum import Enum

# === base ===
class Brightness(Enum):
    """Describes the contrast of a theme or color palette. Supports 2/2 flutter variants."""
    dark = 'dark'
    light = 'light'

# === Text ===
class TextAlign(Enum):
    """Whether and how to align text horizontally. Supports 4/6 flutter vartiants."""
    center = 'center'
    left = 'left'
    right = 'right'
    justify = 'justify'


class FontWeight(Enum):
    """The thickness of the glyphs used to draw the text. Supports 4/11 flutter variants."""
    normal = 'w400'
    bold = 'w700'
    w400 = 'w400'
    w700 = 'w700'

class FontStyle(Enum):
    """Whether to use the italic type variation of glyphs in the font. Supports 2/2 flutter variants."""
    normal = 'normal'
    italic = 'italic'

class TextDecoration(Enum):
    """A linear decoration to draw near the text. Supports 3/5 flutter variants. `combine` method does not supprots - use `combined` variant instead."""
    none = ''
    underline = 'underline'
    line_through = 'strike'
    combined = 'combined'

class TextOverflow(Enum):
    """How overflowing text should be handled. Supports 3/4 flutter variants."""
    clip = 'hidden'
    fade = 'fade'
    ellipsis = 'ellipsis'

# === Flex ===
class FlexFit(Enum):
    """How the child is inscribed into the available space. Supports 2/2 flutter variants."""
    loose = 'loose'
    tight = 'tight'

# === Layouts ===
class MainAxisAlignment(Enum):
    """How the children should be placed along the main axis in a flex layout. Supports 6/6 flutter variants."""
    start = 'start'
    center = 'center'
    end = 'end'
    space_between = 'space_between'
    space_evenly = 'space_evenly'
    space_around = 'space_around'

    def _distribute_space(self, free_space: int, item_count: int, flipped: bool = False, spacing: int = 0) -> tuple[int, int]:
        """Distribute space between children.  
        **difference from flutter:** `/` replaced to `//` because textual avoid float values (only int dimensions)
        """
        if (
            self == MainAxisAlignment.start or
            (item_count < 2 and self == MainAxisAlignment.space_between) or
            (item_count == 0 and self == MainAxisAlignment.space_around)
        ):
            return (free_space, spacing) if flipped else (0, spacing)

        elif self == MainAxisAlignment.center:
            return (free_space // 2, spacing)

        elif self == MainAxisAlignment.space_between:
            return (0, free_space // (item_count - 1) + spacing)

        elif self == MainAxisAlignment.space_around:
            return (free_space // item_count // 2, free_space // item_count + spacing)

        elif self == MainAxisAlignment.space_evenly:
            return (free_space // (item_count + 1), free_space // (item_count + 1) + spacing)

        elif self == MainAxisAlignment.end:
            return (0, spacing) if flipped else (free_space, spacing)

        else:
            raise ValueError(f'Unknown MainAxisAlignment value: {self.value}')

class CrossAxisAlignment(Enum):
    """How the children should be placed along the cross axis in a flex layout. Supports 4/5 flutter variants."""
    start = 'start'
    center = 'center'
    end = 'end'
    stretch = 'stretch'

    def _get_child_cross_axis_offest(self, free_space: int, flipped: bool = False) -> int:
        """Get cross axis offset before children.  
        **difference from flutter:** `/` replaced to `//` because textual avoid float values (only int dimensions)
        """
        if self == CrossAxisAlignment.stretch:
            return 0
        elif self == CrossAxisAlignment.start:
            return free_space if flipped else 0
        elif self == CrossAxisAlignment.center:
            return free_space // 2
        elif self == CrossAxisAlignment.end:
            return 0 if flipped else free_space
        else:
            raise ValueError(f'Unknown CrossAxisAlignment value: {self.value}')

class MainAxisSize(Enum):
    """How much space should be occupied in the main axis."""
    min = 'min'
    max = 'max'

class Axis(Enum):
    """The two cardinal directions in two dimensions."""
    horizontal = 'horizontal'
    vertical = 'vertical'

class VerticalDirection(Enum):
    """A direction in which boxes flow vertically."""
    up = 'up'
    down = 'down'