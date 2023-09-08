# `TikzPicture`

The `TikzPicture` class acts a canvas in which users can append drawings to. In the background, the `TikzPicture` manages the creation of the tikz code.
The signature of the class is given below.

```python
TikzPicture(center=center, options=options)
```

| Parameter       | Description                                                              | Default |
| --------------- | ------------------------------------------------------------------------ | ------- |
| `center` (bool) | True if you would like your tikzpicture to be centered, false otherwise. | `False` |
| `options` (str) | A string containing valid Tikz options.                                  | `""`    |


# Methods 
## `TikzPicture.line()`

Draws a line 
```python
line(
    start: Union[Tuple[float, float], Point],
    end: Union[Tuple[float, float], Point],
    options: str = "",
    to_options: str = "",
    control_pts: list = [],
    action: str = "draw",
) -> Line:
```

## `TikzPicture.plot_coordinates`
```
plot_coordinates(
    points: Union[List[tuple], List[Point]],
    options: str = "",
    plot_options: str = "",
    action: str = "draw",
) -> PlotCoordinates:
```

## `TikzPicture.circle`
```python
def circle(
    self,
    center: Union[Tuple[float, float], Point],
    radius: float,
    options: str = "",
    action: str = "draw",
) -> Circle:
```

## `TikzPicture.node`
```python
def node(
    self,
    position: Union[Tuple[float, float], Point],
    options: str = "",
    text: str = "",
) -> Node:
```

## `TikzPicture.rectangle`
```python
def rectangle(
    self,
    left_corner: Union[Tuple[float, float], Point] = Point(0, 0),
    right_corner: Union[Tuple[float, float], Point] = Point(0, 0),
    options: str = "",
    action: str = "draw",
) -> Rectangle:
```

## `TikzPicture.ellipse`
```python
def ellipse(
    self,
    center: Union[Tuple[float, float], Point],
    x_axis: float,
    y_axis: float,
    options: str = "",
    action: str = "draw",
) -> Ellipse:
```

## `TikzPicture.arc`
```python
def arc(
    self,
    position: Union[Tuple[float, float], Point],
    start_angle: float,
    end_angle: float,
    radius: float = None,
    x_radius: float = None,
    y_radius: float = None,
    options: str = "",
    radians: bool = False,
    draw_from_start: bool = True,
    action: str = "draw",
) -> Arc:
```



## `TikzPicture.show()`
Compiles the TikZ code currently created and displays it to the user. This should either open the PDF viewer on the user's computer with the graphic, or open the PDF in the user's browser. 

## `TikzPicture.write(file)`
Writes the currently recorded Tikz code into the the desired `file`. If `file` is empty. The default value of this parameter is `tikz_code.tex`.

## `TikzPicture.compile()`
Compiles the tikz code and moves the compiled PDF to the user's current working directory.

## `TikzPicture.write_tex_file(file)`
Writes the entire tex code, in addition to the Tikz code, into the the desired `file`. If `file` is empty. The default value of this parameter is `tikz_code.tex`.







