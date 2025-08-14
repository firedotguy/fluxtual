from enum import Enum
import re

BLACK = 0x000000
WHITE = 0xFFFFFF
HEX_PATTERN = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

def _validate(self, *components: int):
    for c in components:
        if not (0 <= c <= 255):
            raise ValueError(f"Color component out of range 0..255: {c}")

class Color:
    """Color with ARGB storage. String form is '#RRGGBB' for Textual."""

    def __init__(self, value: int):
        """value can be 0xRRGGBB or 0xAARRGGBB; alpha preserved if present."""
        self.a = (value >> 24) & 0xFF if value > 0xFFFFFF else 0xFF
        self.r = (value >> 16) & 0xFF
        self.g = (value >> 8) & 0xFF
        self.b = value & 0xFF
        _validate(self.a, self.r, self.g, self.b)

    @classmethod
    def from_hex(cls, hex_value: str) -> "Color":
        """
        Accepts '#RGB', '#RRGGBB', '#AARRGGBB' (leading '#' optional).
        Short '#RGB' expands to '#RRGGBB' with full alpha (FF).
        """
        m = HEX_PATTERN.match(hex_value.strip())
        if not m:
            raise ValueError(f"Invalid HEX color: {hex_value}")
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)  # RGB -> RRGGBB
        if len(h) == 6:
            a, r, g, b = 0xFF, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        else:  # len == 8 (AARRGGBB)
            a, r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16)
        return cls.from_argb(a, r, g, b)

    @classmethod
    def from_argb(cls, a: int, r: int, g: int, b: int) -> "Color":
        _validate(a, r, g, b)
        return cls((a << 24) | (r << 16) | (g << 8) | b)

    def to_int(self, argb: bool = True) -> int:
        """Return 0xAARRGGBB if argb=True, else 0xRRGGBB."""
        return (self.a << 24 | self.r << 16 | self.g << 8 | self.b) if argb else (self.r << 16 | self.g << 8 | self.b)

    def to_hex(self, with_alpha: bool = False) -> str:
        """'#RRGGBB' or '#AARRGGBB'."""
        if with_alpha:
            return f"#{self.a:02X}{self.r:02X}{self.g:02X}{self.b:02X}"
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    def __str__(self) -> str:
        """For Textual styles: return '#RRGGBB' (alpha not rendered in terminal)."""
        return self.to_hex(with_alpha=False)


class Colors(Color, Enum):
    """Standalone Flutter colors (without shade and opacity)"""
    transparent = 0x00000000
    black = 0xFF000000
    white = 0xFFFFFFFF
    red = 0xFFF44336
    red_accent = 0xFFFF5252
    pink = 0xFFE91E63
    pink_accent = 0xFFFF4081
    purple = 0xFF9C27B0
    purple_accent = 0xFFE040FB
    deep_purple = 0xFF673AB7
    deep_purple_accent = 0xFF7C4DFF
    indigo = 0xFF3F51B5
    indigo_accent = 0xFF536DFE
    blue = 0xFF2196F3
    blue_accent = 0xFF448AFF
    light_blue = 0xFF03A9F4
    light_blue_accent = 0xFF40C4FF
    cyan = 0xFF00BCD4
    cyan_accent = 0xFF18FFFF
    teal = 0xFF009688
    teal_accent = 0xFF64FFDA
    green = 0xFF4CAF50
    green_accent = 0xFF69F0AE
    light_green = 0xFF8BC34A
    light_green_accent = 0xFFB2FF59
    lime = 0xFFCDDC39
    lime_accent = 0xFFEEFF41
    yellow = 0xFFFFEB3B
    yellow_accent = 0xFFFFFF00
    amber = 0xFFFFC107
    amber_accent = 0xFFFFD740
    orange = 0xFFFF9800
    orange_accent = 0xFFFFAB40
    deep_orange = 0xFFFF5722
    deep_orange_accent = 0xFFFF6E40
    brown = 0xFF795548
    grey = 0xFF9E9E9E
    blue_grey = 0xFF607D8B

    def __new__(cls, value: int):
        obj = Color(value)
        return obj