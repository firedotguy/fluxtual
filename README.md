# fluxtual
![License](https://img.shields.io/github/license/firedotguy/fluxtual) ![GitHub last commit](https://img.shields.io/github/last-commit/firedotguy/fluxtual) ![GitHub issues](https://img.shields.io/github/issues/firedotguy/fluxtual) ![GitHub Repo stars](https://img.shields.io/github/stars/codeFlane/fluxtual?style=social) ![Platform](https://img.shields.io/badge/platform-Terminal-blue) ![Textual](https://img.shields.io/badge/powered%20by-Textual-purple)

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

### Flexible
A layout widget that controls how its child is laid out within a `Row` or `Column`.
By default, it takes up a portion of the available space determined by flex, but if `fit=FlexFit.loose`, it only expands if there's free space.
```python
from fluxtual.flex import Flexible
from fluxtual.enums import FlexFit
from textual.widgets import Static

flexible_widget = Flexible(
    Static("Short text (loose) – grows only if there is room."),
    flex=2,
    fit=FlexFit.loose
)
```
#### Related enums
| Enum               | Values           |
| ------------------ | -----------------|
| **FlexFit**        | `loose`, `tight` |
---

### Expanded
A layout widget that forces its child to occupy exactly its allocated flex share in a Row or Column, regardless of the child’s intrinsic size.
```python
from fluxtual.flex import Expanded
from textual.widgets import Static

expanded_widget = Expanded(
    Static("Expanded fills exactly its fr share."),
    flex=1
)
```
---

### Align
Positions a single child within itself using Flutter-like `Alignment`.
Optionally sizes itself to a multiple of the child via `width_factor` / `height_factor`.
```python
from fluxtual.geometry.alignment import Alignment
from fluxtual.widgets.align import Align
from fluxtual.widgets.text import Text

# Center a text
aligned = Align(
    child=Text("Centered"),
    alignment=Alignment.center,
)

# Bottom-right, container size collapses to 1.5x child width and 2x child height
compact = Align(
    child=Text("Bottom Right"),
    alignment=Alignment.bottom_right,
    width_factor=1.5,
    height_factor=2.0,
)
```
#### Alignment
Alignment(x, y) uses normalized coordinates in the range [-1.0, 1.0]:

 - x = -1 → left, 0 → center, 1 → right
 - y = -1 → top, 0 → center, 1 → bottom

Predefined constants:
| Name                      | Value          |
| ------------------------- | -------------- |
| `Alignment.top_left`      | `(-1.0, -1.0)` |
| `Alignment.top_center`    | `(0.0, -1.0)`  |
| `Alignment.top_right`     | `(1.0, -1.0)`  |
| `Alignment.center_left`   | `(-1.0, 0.0)`  |
| `Alignment.center`        | `(0.0, 0.0)`   |
| `Alignment.center_right`  | `(1.0, 0.0)`   |
| `Alignment.bottom_left`   | `(-1.0, 1.0)`  |
| `Alignment.bottom_center` | `(0.0, 1.0)`   |
| `Alignment.bottom_right`  | `(1.0, 1.0)`   |
You can also create custom alignments:
```python
custom = Align(
    child=Text("Custom"),
    alignment=Alignment(0.25, -0.75),  # slightly right of left, near the top
)
```
##### Sizing behavior
 - Stretch (default): If width_factor/height_factor are None, Align expands to the available space (behaves like a full-size container) and positions the child within it.
 - Shrink (factor mode): If a factor is provided, Align reports its own content size as child_size * factor along that axis, effectively collapsing to a size relative to its child (Flutter-like behavior).

### Center
A convenience widget that centers its single child within itself.
Functionally equivalent to Align(alignment=Alignment.center) with optional width_factor / height_factor.
```python
from fluxtual.widgets.center import Center
from fluxtual.widgets.text import Text

# Center a text within available space
centered = Center(
    child=Text("Hello, Fluxtual!")
)
```

---
### Builder
A widget that defers the creation of its child to a builder function.
Useful when you need to rebuild UI based on context or want to construct widgets lazily.
```
from fluxtual.widgets.builder import Builder
from fluxtual.widgets.text import Text

# Simple usage: build a text dynamically
builder = Builder(
    builder=lambda context: Text(f"Hello from {context.app.title}")
)
```

Soon more widgets! Made 6/~300 Flutter widgets

## 🛣️ Roadmap
 - [ ] Layouts (e.g `Column`, `Row`, `Stack`, etc.)
 - [ ] Animations support
 - [ ] Material 3 widgets (`Buttons`, `Switches`, `Dropdowns`, etc.)
 - [ ] Release to PyPI
 - [ ] Add documentation to readthedocs.io
 - [ ] Text direction support

## 📜 License
This project licensed under [MIT](./LICENSE) License

## 🤝 Contributing

This project is still in active development, and your help is highly appreciated!  
If you have ideas, find a bug, or want to add a new widget — feel free to:

- Open a **Pull Request** with your improvements.
- Create an **Issue** to report problems or suggest features.
- ⭐ **Star the repository** to support the project and help it grow.
