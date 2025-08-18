from re import match

from rich.text import Text as RichText
from textual.geometry import Size
from textual.widget import Widget
from textual.reactive import reactive
from textual import log

from fluxtual.color import Color, Colors
from fluxtual.enums import FontStyle, FontWeight, TextAlign, TextDecoration, TextOverflow
from fluxtual.inherited import InheritedTheme
from fluxtual.widgets.base import BuildContext, _NullWidget, StatelessWidget
from fluxtual.widgets.builder import Builder
from fluxtual.widgets.align import _TextAlign


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

def _justify_line(line: RichText, width: int) -> RichText:
    """Distribute extra spaces across gaps so that len(line) == width.
        Skips lines that have no gaps or already match width."""
    lines = line.split('\n')
    justified = RichText()
    for line in lines:
        spaces = len([i for i in str(line) if i == ' '])
        if spaces:
            spacing = 1 + (width - len(line)) // spaces
            extra = (width - len(line)) % spaces
            words = [str(word) for word in line.split(' ')]
            if extra:
                justified_line = ''
                for i, word in enumerate(words):
                    if i == len(words) - 1:
                        justified_line += word
                    elif i <= extra:
                        justified_line += word + ' ' * (spacing + 1)
                    else:
                        justified_line += word + ' ' * spacing
                justified.append(justified_line)
            else:
                justified.append((' ' * spacing).join(words))
        else:
            justified.append(line)
    return justified

class TextStyle:
    """An immutable style describing how to format and paint text."""
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
        overflow: TextOverflow | None = None
    ):
        """Creates a text style. Supports 9/26 flutter arguments.

        Args:
            inherit (bool, optional): Whether null values in this TextStyle can be replaced with
                their value in another TextStyle using merge. Defaults to True.
            color (Color, optional): The color to use when painting the text. Defaults to
                Colors.white.
            background_color (Color, optional): The color to use as the background for the text.
                Defaults to Colors.black.
            font_style (FontStyle, optional): The typeface variant to use when drawing the letters.
                Defaults to FontStyle.normal.
            font_weight (FontWeight, optional): The typeface thickness to use when painting the
                text. Defaults to FontWeight.normal.
            letter_spacing (int, optional): The amount of spaces to add between each letter.
                Defaults to 0.
            word_spacing (int, optional): The amount of spaces to add at each sequence of
                white-space (i.e. between each word). Defaults to 1.
            decoration (TextDecoration, optional): The decorations to paint near the text
                (e.g., an underline). Defaults to TextDecoration.none
            overflow (TextOverflow, optional): How visual text overflow should be handled.
        """
        self.inherit = inherit
        self.color = color
        self.bg_color = background_color
        self.font_style = font_style
        self.font_weight = font_weight
        self.letter_spacing = letter_spacing
        self.word_spacing = word_spacing
        self.decoration = decoration
        self.overflow = overflow

    def merge(self, other: 'TextStyle | None') -> 'TextStyle':
        """Returns a new text style that is a combination of this style and the given other style."""
        if not other:
            return self
        if not other.inherit:
            return other
        return TextStyle(
            color=other.color or self.color or Colors.white,
            background_color=other.bg_color or self.bg_color or Colors.black,
            font_style=other.font_style or self.font_style or FontStyle.normal,
            font_weight=other.font_weight or self.font_weight or FontWeight.normal,
            letter_spacing=other.letter_spacing or self.letter_spacing or 0,
            word_spacing=other.word_spacing or self.word_spacing or 1,
            decoration=other.decoration or self.decoration or TextDecoration.none
        )


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
        return " ".join(text_style) if text_style else ""

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

    def apply(self, widget: '_TextRender') -> None:
        text_style = self._get_css_text_style()
        if text_style:
            widget.styles.text_style = text_style
        if self.color:
            widget.styles.color = self.color.to_hex()
        if self.bg_color:
            widget.styles.background = self.bg_color.to_hex()
        if self.word_spacing is not None:
            widget.content = widget.content.replace(' ', ' ' * self.word_spacing)
        if self.letter_spacing is not None:
            content = ''
            for i, letter in enumerate(widget.content):
                if i != len(widget.content) - 1 and match(r'\S', letter) and match(r'\S', widget.content[i + 1]):
                    content += letter + ' ' * self.letter_spacing
                else:
                    content += letter
            widget.content = content


class DefaultTextStyle(InheritedTheme):
    """The text style to apply to descendant `Text` widgets which don't have an explicit style."""
    def __init__(
        self,
        child: Widget,
        style: TextStyle,
        text_align: TextAlign | None = None,
        soft_wrap: bool = True,
        overflow: TextOverflow | None = None,
        max_lines: int | None = None
    ) -> None:
        """Creates a default text style for the given subtree. Supports 6/8 flutter arguments.

        Args:
            child (Widget): The widget below this widget in the tree.
            style (TextStyle): The text style to apply.
            text_align (TextAlign, optional): How each line of text in the Text widget should be
                aligned horizontally. Defaults to None.
            overflow (TextOverflow, optional): How visual overflow should be handled.
                Defaults to None.
            max_lines (int, optional): An optional maximum number of lines for the text to span,
                wrapping if necessary. Defaults to None.
        """
        super().__init__(child)
        assert max_lines == None or max_lines > 0
        self.child = child
        self.style = style
        self.text_align = text_align
        self.soft_wrap = soft_wrap
        self.overflow = overflow
        self.max_lines = max_lines

    @classmethod
    def fallback(cls):
        """A const-constructable default text style that provides fallback values."""
        return cls(style=TextStyle(), text_align=None, soft_wrap=True, max_lines=None, overflow=TextOverflow.clip, child=_NullWidget())

    @staticmethod
    def merge(
        child: Widget,
        style: TextStyle | None = None,
        text_align: TextAlign | None = None,
        soft_wrap: bool | None = None,
        overflow: TextOverflow | None = None,
        max_lines: int | None = None,
    ):
        """Creates a default text style that overrides the text styles in scope at this point in
            the widget tree. Supports 6/8 flutter arguments."""
        def build(context: BuildContext):
            parent = DefaultTextStyle.of(context)
            return DefaultTextStyle(
                style=parent.style.merge(style),
                text_align=text_align or parent.text_align,
                soft_wrap=soft_wrap or parent.soft_wrap,
                overflow=overflow or parent.overflow,
                max_lines=max_lines or parent.max_lines,
                child=child
            )
        return Builder(build)

    @staticmethod
    def of(context: BuildContext) -> "DefaultTextStyle":
        """The closest instance of this class that encloses the given context. Supports 1/1
            flutter arguments"""
        return context.depend_on_inherited_widget_of_exact_type(DefaultTextStyle) or DefaultTextStyle.fallback()

    def update_should_notify(self, old_widget: 'DefaultTextStyle') -> bool:
        """Whether the framework should notify widgets that inherit from this widget. Supports
            1/1 flutter arguments."""
        return (
            self.style != old_widget.style or self.text_align != old_widget.text_align or
            self.soft_wrap != old_widget.soft_wrap or self.overflow != old_widget.overflow or
            self.max_lines != old_widget.max_lines
        )

    def wrap(self, context: BuildContext, child: Widget) -> "DefaultTextStyle":
        """Return a copy of this inherited theme with the specified `child`. Supports 2/2 flutter
            arguments."""
        return DefaultTextStyle(
            style=self.style,
            text_align=self.text_align,
            soft_wrap=self.soft_wrap,
            overflow=self.overflow,
            max_lines=self.max_lines,
            child=child
        )

class _TextRender(Widget):
    """A run of text with a single style."""
    content = reactive("", layout=True)

    def __init__(
        self,
        data: str,
        style: TextStyle,
        text_align: TextAlign | None = None,
        soft_wrap: bool = False,
        overflow: TextOverflow = TextOverflow.clip,
        max_lines: int | None = None,
        id: str | None = None,
        classes: str = ''
    ) -> None:
        """Creates a text widget. Supports 6/17 flutter arguments.

        Args:
            data (str): The text to display.
            style (TextStyle): If non-null, the style to use for this text. Defaults to TextStyle().
            text_align (TextAlign, optional): How the text should be aligned horizontally. Defaults to TextAlign.left.
            soft_wrap (bool): Whether the text should break at soft line breaks. Defaults to False.
            overflow (TextOverflow, optional): How visual overflow should be handled. Defaults to TextOverflow.clip.
            max_lines (int, optional): An optional maximum number of lines for the text to span, wrapping if necessary. Defaults to None.
            id (str, optional): Textual CSS id. Defaults to None.
            classes (str, optional): Textual CSS classes. Defaults to ''.
        """
        super().__init__(id=id, classes=classes)
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
        self._wrapped = None

    def get_css(self) -> str:
        css = '.fluxtual-text {'
        if self.max_lines:
            css += f'max-height: {self.max_lines};'
        if self.align:
            css += f'text-align: {self.align.value};'
        return css + '}'

    def on_mount(self) -> None:
        self.style.apply(self)

        self.overflow = self.overflow or self.style.overflow
        if self.align:
            self.styles.text_align = self.align.value
        if self.max_lines:
            self.styles.max_height = self.max_lines


    def _reflow(self, width, height):
        self._wrapped = wrap_text(self.content, width, height, self.soft_wrap, self.overflow, self.fade_overflow_length)
        # set sizes to minimal if not justify
        if self.align == TextAlign.justify:
            self._width = width
            self._wrapped = _justify_line(self._wrapped, width)
            log(self._wrapped)
        else:
            self._width = max([len(line) for line in self._wrapped.split('\n')])
        self._height = len(self._wrapped.split('\n'))
        # self.styles.height = self._height
        # self.styles.width = self._width

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        self._reflow(container.width, container.height)
        return self._height or 1

    def get_content_width(self, container: Size, viewport: Size) -> int:
        return self._width or len(self.content)

    def render(self) -> RichText:
        if not self._wrapped:
            self._reflow(self._width, self._height)
        assert self._wrapped != None
        return self._wrapped

class Text(StatelessWidget):
    def __init__(
        self,
        data: str,
        style: TextStyle | None = None,
        text_align: TextAlign | None = None,
        soft_wrap: bool = False,
        overflow: TextOverflow = TextOverflow.clip,
        max_lines: int | None = None,
        id: str | None = None,
        classes: str = ''
    ) -> None:
        """Creates a text widget. Supports 6/17 flutter arguments.

        Args:
            data (str): The text to display.
            style (TextStyle, optional): If non-null, the style to use for this text. Defaults to TextStyle().
            text_align (TextAlign, optional): How the text should be aligned horizontally. Defaults to TextAlign.left.
            soft_wrap (bool): Whether the text should break at soft line breaks. Defaults to False.
            overflow (TextOverflow, optional): How visual overflow should be handled. Defaults to TextOverflow.clip.
            max_lines (int, optional): An optional maximum number of lines for the text to span, wrapping if necessary. Defaults to None.
            id (str, optional): Textual CSS id. Defaults to None.
            classes (str, optional): Textual CSS classes. Defaults to ''.
        """
        super().__init__(id=id, classes=classes)
        self.content = data
        self.style = style
        self.text_align = text_align
        self.soft_wrap = soft_wrap
        self.overflow = overflow
        self.max_lines = max_lines
        self.textual_id = id
        self.textual_classes = classes
        self._rendered_text = None

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        assert self._rendered_text != None, 'Text not rendered yet'
        return self._rendered_text.get_content_height(container, viewport, width)

    def get_content_width(self, container: Size, viewport: Size) -> int:
        assert self._rendered_text != None, 'Text not rendered yet'
        return self._rendered_text.get_content_width(container, viewport)

    def build(self, context: BuildContext) -> _TextAlign:
        default_text_style = DefaultTextStyle.of(context)
        effective_text_style = self.style
        if self.style == None or self.style.inherit:
            effective_text_style = default_text_style.style.merge(self.style)

        self._rendered_text = _TextRender(
            self.content,
            effective_text_style or TextStyle(),
            self.text_align or default_text_style.text_align or TextAlign.left,
            self.soft_wrap or default_text_style.soft_wrap,
            self.overflow or (effective_text_style or default_text_style).overflow,
            self.max_lines or default_text_style.max_lines,
            self.textual_id,
            self.textual_classes
        )
        return _TextAlign(self._rendered_text, self.text_align or TextAlign.left)