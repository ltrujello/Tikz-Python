# `Scope`
The `Scope` class is meant to handle the `scope` environment in TikZ. 
Scoping is useful as it can be used to nest a set of commands in a TikZ picture, or it can be used in conjunction with the TikZ `clip` command to "clip out" drawings. 

This class is analagous to the TikZ command 
```
\begin{scope}
    ...
\end{scope}
```

The signature of the class is given below.
```python
from tikzpy import Scope

scope = Scope(options)
```

| Parameter            | Description                                                                            | Default   |
| -------------------- | -------------------------------------------------------------------------------------- | --------- |
| `options` (str)      | A string of valid Tikz         options.                                                | `""`      |

## Methods

### `Scope.append(draw_obj)`
Appends any drawing object `draw_obj` to the scope environment. If one updates an attribute of a drawing object even after it has been appended, the updates are reflected in scope. 

### `Scope.remove(draw_obj)`
Removes a drawing object `draw_obj` which has been appended to the scoping environment.

### `Scope.clip(draw_obj, draw)`
Clips the drawing object `draw_obj` from the scope environment by creating an instance of the class `Clip`. Here, `draw` is a boolean regarding whether or not you want to actually draw what you are clipping. It is set to `False` by default. 

The class `Scope` also as access to methods `.shift()`, `.scale()`, `.rotate()`. In this case, such operations are applied to every single member of the scoping environment, made possible by the fact that every drawing object itself has access to these methods. These work as one would expect, which is unlike Tikz, since sometimes applying transformations to scoping environments in Tikz does not behave intuitively. 

