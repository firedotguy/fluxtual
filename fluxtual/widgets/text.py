from rich.text import Text as RichText
from textual.geometry import Size
from textual.widget import Widget
from textual.reactive import reactive
from fluxtual.color import Color, Colors
from fluxtual.enums import FontStyle, FontWeight, TextAlign, TextDecoration, TextOverflow
from textual import log

def _wrap_line(line: str, width: int) -> list[str]:
    """Wrap line"""
    lines = []
    tail = line
    i = 0
    while True:
        if i > 10000:
            raise ValueError('Too long text for wrapping. Set soft_wrap to False.')
        if len(tail) > width:
            lines.append(tail[:width])
            tail = tail[width:]
            i += 1
        else:
            lines.append(tail)
            break
    return lines

def wrap_text(text: str, width: int, height: int, soft_wrap: bool = True, overflow: TextOverflow = TextOverflow.clip, fade_overflow_length: int = 1) -> RichText:
    """Custom wrapping functions with overflowing and multiline/singleline support"""
    if width <= 0 or height <= 0:
        return RichText('')

    # standart overflowing
    if not soft_wrap:
        if len(text) > width:
            text = text[:width]
            if overflow == TextOverflow.ellipsis:
                return RichText(text[:-1] + '…')
            elif overflow == TextOverflow.fade:
                rich_text = RichText(text[:-fade_overflow_length])
                fade_text = RichText(text[-fade_overflow_length])
                fade_text.stylize('dim')
                rich_text.append(fade_text)
                return rich_text
        return RichText(text)

    # custom overflowing with multiline support
    lines = []
    for line in text.splitlines(True):
        if line.endswith("\n"):
            chunks = _wrap_line(line[:-1], width) or [""]
            lines.extend(chunks)
        else:
            chunks = _wrap_line(line, width) or [""]
            lines.extend(chunks)

    last = lines[-1]
    if len(last) >= width:
        if overflow == TextOverflow.ellipsis:
            rich_text = RichText(last[:-1] + '…')
        elif overflow == TextOverflow.fade:
            rich_text = RichText(last[:-1])
            fade_text = RichText(last[-1])
            fade_text.stylize('dim')
            rich_text.append(fade_text)
        else:
            rich_text = RichText(last)
        lines[-1] = rich_text

    # convert to RichText
    rich_text = RichText()
    for i, line in enumerate(lines):
        if i != len(lines) - 1:
            rich_text.append(RichText(line + '\n'))
        else:
            rich_text.append(line)
    return rich_text


class TextStyle:
    def __init__(
        self,
        inherit: bool = True,
        color: Color | None = None,
        background_color: Color | None = None,
        font_style: FontStyle | None = None,
        font_weight: FontWeight | None = None,
        letter_spacing: int | None = None,
        word_spacing: int | None = None,
        decoration: TextDecoration | None = None,
    ):
        """Init Text stylizations

        Args:
            inherit (bool, optional): Whether null values in this TextStyle can be replaced with their value in another TextStyle using merge. Defaults to True.
            color (Color, optional): The color to use when painting the text. Defaults to Colors.white.
            background_color (Color, optional): The color to use as the background for the text. Defaults to Colors.black.
            font_style (FontStyle, optional): The typeface variant to use when drawing the letters. Defaults to FontStyle.normal.
            font_weight (FontWeight, optional): The typeface thickness to use when painting the text. Defaults to FontWeight.normal.
            letter_spacing (int, optional): The amount of spaces to add between each letter. Defaults to 0.
            word_spacing (int, optional): The amount of spaces to add at each sequence of white-space (i.e. between each word). Defaults to 1.
            decoration (TextDecoration, optional): The decorations to paint near the text (e.g., an underline). Defaults to TextDecoration.none
        """
        self.inherit = inherit
        self.color = color
        self.bg_color = background_color
        self.font_style = font_style
        self.font_weight = font_weight
        self.letter_spacing = letter_spacing
        self.word_spacing = word_spacing
        self.decoration = decoration

    def merge(self, other: 'TextStyle') -> 'TextStyle':
        """Flutter-like style merging (merge only if inherit=True, otherwise keep values)"""
        if not other:
            return self
        if self.inherit:
            return TextStyle(
                color=self.color or other.color or Colors.white,
                background_color=self.bg_color or other.bg_color or Colors.black,
                font_style=self.font_style or other.font_style or FontStyle.normal,
                font_weight=self.font_weight or other.font_weight or FontWeight.normal,
                letter_spacing=self.letter_spacing or other.letter_spacing or 0,
                word_spacing=self.word_spacing or other.word_spacing or 1,
                decoration=self.decoration or other.decoration or TextDecoration.none
            )
        else:
            return self

    def _get_css_text_style(self):
        text_style = []
        if self.decoration:
            if self.decoration == TextDecoration.line_through or self.decoration == TextDecoration.combined:
                text_style.append('strike')
            if self.decoration == TextDecoration.underline or self.decoration == TextDecoration.combined:
                text_style.append('underline')
        if self.font_weight:
            if self.font_weight.value == 'w700':
                text_style.append('bold')
        if self.font_style:
            if self.font_style == FontStyle.italic:
                text_style.append('italic')
        return " ".join(text_style) if text_style else None

    def get_css(self) -> str:
        css = ''

        text_style = self._get_css_text_style()

        if text_style:
            css += f'text-style: {text_style};'
        if self.color:
            css += f'color: {self.color};'
        if self.bg_color:
            css += f'background-color: {self.bg_color};'
        return css

    def apply(self, widget: Widget) -> None:
        text_style = self._get_css_text_style()
        if text_style:
            widget.styles.text_style = text_style
        if self.color:
            widget.styles.color = self.color.to_hex()
        if self.bg_color:
            widget.styles.background = self.bg_color.to_hex()

class Text(Widget):
    content = reactive("", layout=True)

    def __init__(
        self,
        data: str,
        style: TextStyle | None = None,
        text_align: TextAlign | None = None,
        soft_wrap: bool = False,
        overflow: TextOverflow = TextOverflow.clip,
        max_lines: int | None = None,
        textual_id: str | None = None,
        textual_classes: str = ''
    ) -> None:
        """Creates a text widget. Supports 6/17 flutter arguments.

        Args:
            data (str): The text to display.
            style (TextStyle, optional): If non-null, the style to use for this text. Defaults to TextStyle().
            text_align (TextAlign, optional): How the text should be aligned horizontally. Defaults to TextAlign.left.
            soft_wrap (bool): Whether the text should break at soft line breaks. Defaults to False.
            overflow (TextOverflow, optional): How visual overflow should be handled. Defaults to TextOverflow.clip.
            max_lines (int, optional): An optional maximum number of lines for the text to span, wrapping if necessary. Defaults to None.
            textual_id (str, optional): Textual CSS id. Defaults to None.
            textual_classes (str, optional): Textual CSS classes. Defaults to ''.
        """
        super().__init__(id=textual_id, classes=(textual_classes + ' fluxtual-text').strip())
        self.content = data
        self.style = style
        self.align = text_align
        self.soft_wrap = soft_wrap
        self.overflow = overflow
        self.max_lines = max_lines
        self.fade_overflow_length = 1

        self._width = None
        self._height = None
        self.styles.height = 'auto'
        self.styles.width = 'auto'
        self._given_width = 0

    def get_css(self) -> str:
        css = '.fluxtual-text {'
        if self.max_lines:
            css += f'max-height: {self.max_lines};'
        if self.align:
            css += f'text-align: {self.align.value};'
        return css + '}'

    def on_mount(self) -> None:
        if self.style:
            self.style.apply(self)

        if self.align:
            self.styles.text_align = self.align.value
        if self.max_lines:
            self.styles.max_height = self.max_lines


    def _reflow(self, width, height):
        self._wrapped = wrap_text(self.content, width, height, self.soft_wrap, self.overflow, self.fade_overflow_length)
        # set sizes to minimal
        self._width = max([len(line) for line in self._wrapped.split('\n')])
        self._height = len(self._wrapped.split('\n'))
        # self.styles.height = self._height
        # self.styles.width = self._width

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        return self._height or 1

    def get_content_width(self, container: Size, viewport: Size) -> int:
        self._reflow(container.width, container.height)
        return self._width or len(self.content)

    def render(self) -> RichText:
        return self._wrapped