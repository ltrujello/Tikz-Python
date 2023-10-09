# `Line`

The `Line` class helps handle the creation of lines in tikz code. It is analagous to the TikZ code 
```
\draw[<options>] <start> to [<to_options>] <end>;
```
Lines in TikZ have even more features, like adding control points, and these features are accessible through the Line class.

The signature of the `Line` class is as follows. 
```
Line(start, end, options, to_options, control_pts, action) # A line is created and drawn
```

| Parameter            | Description                                                                                               | Default   |
| -------------------- | --------------------------------------------------------------------------------------------------------- | --------- |
| `start` (tuple)      | Pair of floats representing the start of the line                                                         |
| `end` (tuple)        | Pair of floats representing the end of the line                                                           |
| `options` (str)      | String containing valid Tikz drawing options, e.g. "Blue"                                                 | `""`      |
| `to_options` (str)   | String containing Tikz specifications for connecting the start to the end (e.g. `"to [bend right = 45]"`) | "--"      |
| `control_pts` (list) | List of control points for the line                                                                       | `[]`      |
| `action` (str)       | An action to perform with plot (e.g., `\draw`, `\fill`, `\filldraw`, `\path`)                             | `"\draw"` |

## Methods

The `Line` class has the following methods.

## `Line.start(point: Union[Tuple, Point])`
Sets the line's start position to the Point object `point`

## `Line.end(point: Union[Tuple, Point])`
Sets the line's end position to the Point object `point`

## `Line.pos_at_t(t: float)`
Returns a `Point` object representing the parametrized point on the line at time `t`, where `0 <= t <= 1`.
Thus, when `t = 0` the start position of the line is returned, and when `t = 1` the end position of the line is returned.

## `Line.midpoint()`
Returns a `Point` object representing the midpoint of the line.

Here's an example of us using the `Line` class.
```python
import tikzpy

tikz = tikzpy.TikzPicture()
tikz.line((0, 0), (4, 0), options="->", control_pts=[(1, 1), (3, -1)]
```
which generates 
<img src="../../png/line_ex_1.png">

