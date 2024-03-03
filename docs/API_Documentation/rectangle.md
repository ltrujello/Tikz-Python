# Rectangle

::: tikzpy.drawing_objects.rectangle.Rectangle

## Example
Rectangles are often used as a background to many figures; in this case, 
we create a fancy colored background.

```python
import tikzpy
import math

tikz = tikzpy.TikzPicture(center=True)

tikz.rectangle_from_center((0, 0), width=7, height=5, options="rounded corners, Yellow!30",action="filldraw")
# Params
r = 2
n_nodes = 7
nodes = []
# Draw the nodes
for i in range(1, n_nodes + 1):
    angle = 2 * math.pi * i / n_nodes
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    node = tikz.node((x, y), text=f"$A_{{{i}}}$")
    nodes.append(node)

# Draw the lines between the nodes
for i in range(len(nodes)):
    start = nodes[i].position
    end = nodes[(i + 1) % len(nodes)].position
    tikz.line(start, end, options="->, shorten >= 10pt, shorten <=10pt")
tikz.show()
```

<img src="../../png/rectangle_ex_1.png"/>
