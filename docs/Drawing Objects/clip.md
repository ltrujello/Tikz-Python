# `Clip`
A class to clip a single drawing object `draw_obj`. This is meant to be used in 
conjunction with the `Scope` class. It is analagous to the tikz code

```
\clip ... # some drawing object
```
Below is the signature of the `Clip` class.

```python
from tikzpy import Clip

clip = Clip(draw_obj, draw).
```

| Parameter            | Description                                                                            | Default   |
| -------------------- | -------------------------------------------------------------------------------------- | --------- |
| `draw_ob` (DrawingObject)      | A tikz-python DrawingObject (e.g. `Line`, `Circle`, etc.)                        | `""`      |
| `draw` (bool)      | If `True`, the clipped object is drawn to the graphic, otherwise it is hidden.               | `False`      |

The class `Clip` has access to methods `.shift()`, `.scale()`, `.rotate()`, although this is more for consistency 
(e.g., in case a `Scope` environment changes) and less for direct use of the user. 

