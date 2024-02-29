# Line

::: tikzpy.drawing_objects.line.Line

# Examples

Here's an example of us using the `Line` class.
```python
import tikzpy

tikz = tikzpy.TikzPicture()
tikz.line((0, 0), (4, 0), options="->", control_pts=[(1, 1), (3, -1)]
```
which generates 
<img src="../../png/line_ex_1.png">

