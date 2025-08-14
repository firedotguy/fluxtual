# fluxtual
`fluxtual` brings a **Flutter-inspired API** to [Textual](https://github.com/Textualize/textual), aiming to provide a familiar, expressive, and scalable way to build terminal UIs.  
It includes a **theme system**, ready-to-use widgets, strongly typed enums for styling, and utilities for layout and text rendering.

> **⚠ Work in progress**  
> This package is under active development. Expect frequent updates, breaking changes, and a growing set of widgets, helpers, and theming capabilities.

## ✨ Features

- 🎨 Theme-aware colors and styles
- 🖋 Flutter-like API
- 📐 Typed enums for alignment, font weight/style, overflow, and decoration
- 🧩 Widgets with consistent styling behavior

## ❓ Why Fluxtual?
If you’ve ever built Flutter apps, you’ll feel right at home with Fluxtual.
It brings familiar patterns like `Text`, `TextStyle`, and strongly typed enums into the terminal world, making it easier to build complex, themed UIs without manually managing ANSI codes or low-level styles.

## 📦 Installation

Install directly from the GitHub repository:

```bash
pip install git+https://github.com/codeflane/fluxtual.git
```
> **soon:** PyPI package

## 🎨 Color API
We made full copy of flutter standalone `Color` class and `Colors` enum.
```python
from fluxtual.color import Color, Colors

# From hex
c1 = Color.from_hex("#FF0000")
# From ARGB
c2 = Color.from_argb(0xFF, 255, 0, 0)
# From int (Flutter-style)
c3 = Color(0xFFFF0000)
#From RGBO (soon)

# Predefined colors enum
print(Colors.red)
print(Colors.amber)
```

## 🧩 Widgets

### Text
A styled text widget with support for alignment, wrapping, overflow handling, and background colors.

```python
from fluxtual.color import Colors
from fluxtual.enums import TextAlign, TextOverflow
from fluxtual.text import Text, TextStyle

style = TextStyle(color=Colors.amber)

text_widget = Text(
    data="Hello Fluxtual!",
    style=style,
    text_align=TextAlign.center,
    soft_wrap=True,
    overflow=TextOverflow.fade,
    max_lines=1
)
```

#### TextStyle
Describes how text should be painted, merged, and applied to a widget.
Supports merging with inheritance, theme-aware defaults, and conversion to CSS for Textual styles.

```
from fluxtual.color import Colors
from fluxtual.enums import FontStyle, FontWeight, TextDecoration

style = TextStyle(
    color=Colors.red,
    background_color=Colors.black,
    font_style=FontStyle.italic,
    font_weight=FontWeight.w700,
    decoration=TextDecoration.underline
)
```

#### Related enums
| Enum               | Values                                          |
| ------------------ | ----------------------------------------------- |
| **TextAlign**      | `left`, `right`, `center`, `justify`            |
| **FontWeight**     | `w400`, `w700`, `normal`, `bold`                |
| **FontStyle**      | `normal`, `italic`                              |
| **TextDecoration** | `none`, `underline`, `line_through`, `combined` |
| **TextOverflow**   | `clip`, `ellipsis`, `fade`, `visible`           |

---
Soon more widgets! Made 1/~300 Flutter widgets

## 🛣️ Roadmap
 - [ ] Layouts (e.g `Column`, `Row`, `Stack`, etc.)
 - [ ] Animations support
 - [ ] Material 3 widgets (`Buttons`, `Switches`, `Dropdowns`, etc.)
 - [ ] Release to PyPI
 - [ ] Add documentation to readthedocs.io
 - [ ] Improve theme

## 📜 License
This project licensed under [MIT](./LICENSE) License

## 🤝 Contributing

This project is still in active development, and your help is highly appreciated!  
If you have ideas, find a bug, or want to add a new widget — feel free to:

- Open a **Pull Request** with your improvements.
- Create an **Issue** to report problems or suggest features.
- ⭐ **Star the repository** to support the project and help it grow.
