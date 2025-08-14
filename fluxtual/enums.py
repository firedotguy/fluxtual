from enum import Enum

class Brightness(Enum):
    """Describes the contrast of a theme or color palette. Supports 2/2 variants."""
    dark = 'dark'
    light = 'light'


class TextAlign(Enum):
    """Whether and how to align text horizontally. Supports 4/6 vartiants."""
    center = 'center'
    left = 'left'
    right = 'right'
    justify = 'justify'

class FontWeight(Enum):
    """The thickness of the glyphs used to draw the text. Supports 4/11 variants."""
    normal = 'w400'
    bold = 'w700'
    w400 = 'w400'
    w700 = 'w700'

class FontStyle(Enum):
    """Whether to use the italic type variation of glyphs in the font. Supports 2/2 variants."""
    normal = 'normal'
    italic = 'italic'

class TextDecoration(Enum):
    """A linear decoration to draw near the text. Supports 3/5 variants. `combine` method does not supprots - use `combined` variant instead."""
    none = ''
    underline = 'underline'
    line_through = 'strike'
    combined = 'combined'

class TextOverflow(Enum):
    """How overflowing text should be handled. Supports 4/4 variants."""
    clip = 'hidden'
    fade = 'fade'
    ellipsis = 'ellipsis'
    visible = 'visible'