import tikzpy

tikz = tikzpy.TikzPicture()
tikz.circle((0, 0), 3, options="thick, gray!10", action="filldraw")
arc_one = tikz.arc((2, 0), 0, 180, x_radius=2, y_radius=1, options="dashed, blue")
arc_two = tikz.arc((2, 0), 180, 360, x_radius=2, y_radius=1, options="blue")

tikz.write()
tikz.show()