from tikzpy import TikzPicture

""" #3
    We test that the construction of self.action returns the correct Tikz code. 
    #4, #5, #6, #7
    We also test that reassigning class attributes returns the correct Tikz code.
"""

tikz = TikzPicture()

# Line : \fill
line_fill = tikz.line(
    (0, 0),
    (1, 1),
    options="thick, blue",
    control_pts=[(0.25, 0.25), (0.75, 0.75)],
    action="fill",
)
# Line : \filldraw
line_filldraw = tikz.line(
    (0, 0),
    (1, 1),
    options="thick, blue",
    control_pts=[(0.25, 0.25), (0.75, 0.75)],
    action="filldraw",
)
# Line : \path
line_path = tikz.line(
    (0, 0),
    (1, 1),
    options="thick, blue",
    control_pts=[(0.25, 0.25), (0.75, 0.75)],
    action="path",
)
# Plot : \fill
plot_fill = tikz.plot_coordinates(
    options="green",
    plot_options="smooth ",
    points=[(1, 1), (2, 2), (3, 3), (2, -4)],
    action="fill",
)
# Plot : \filldraw
plot_filldraw = tikz.plot_coordinates(
    options="green",
    plot_options="smooth ",
    points=[(1, 1), (2, 2), (3, 3), (2, -4)],
    action="filldraw",
)
# Plot : \path
plot_path = tikz.plot_coordinates(
    options="green",
    plot_options="smooth ",
    points=[(1, 1), (2, 2), (3, 3), (2, -4)],
    action="path",
)

# Circle : \fill
circle_fill = tikz.circle((1, 1), 1, options="fill = purple", action="fill")
# Circle : \filldraw
circle_filldraw = tikz.circle((1, 1), 1, options="fill = purple", action="filldraw")
# Circle : \path
circle_path = tikz.circle((1, 1), 1, options="fill = purple", action="path")
# Rectangle : \fill
rectangle_fill = tikz.rectangle((2, 2), 1, 2, options="Blue", action="fill")
# Rectangle : \filldraw
rectangle_filldraw = tikz.rectangle((2, 2), 1, 2, options="Blue", action="filldraw")
# Rectangle : \path
rectangle_path = tikz.rectangle((2, 2), 1, 2, options="Blue", action="path")
# Ellipse : \fill
ellipse_fill = tikz.ellipse((0, 0), 3, 4, action="fill")
# Ellipse : \filldraw
ellipse_filldraw = tikz.ellipse((0, 0), 3, 4, action="filldraw")
# Ellipse : \path
ellipse_path = tikz.ellipse((0, 0), 3, 4, action="path")
# Arc : \fill
arc_fill = tikz.arc((0, 0), 20, 90, 4, action="fill")
# Arc : \filldraw
arc_filldraw = tikz.arc((0, 0), 20, 90, 4, action="filldraw")
# Arc : \path
arc_path = tikz.arc((0, 0), 20, 90, 4, action="path")


def test_action_construction():
    """#3 : Test that the action argument returns the correct code."""
    # Test Line : \fill
    assert (
        line_fill.code
        == "\\fill[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \filldraw
    assert (
        line_filldraw.code
        == "\\filldraw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \path
    assert (
        line_path.code
        == "\\path[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Plot : \fill
    assert (
        plot_fill.code
        == "\\fill[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \filldraw
    assert (
        plot_filldraw.code
        == "\\filldraw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \path
    assert (
        plot_path.code
        == "\\path[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Circle : \fill
    assert circle_fill.code == "\\fill[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \filldraw
    assert circle_filldraw.code == "\\filldraw[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \path
    assert circle_path.code == "\\path[fill = purple] (1, 1) circle (1cm);"
    # Rectangle : \fill
    assert rectangle_fill.code == "\\fill[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \filldraw
    assert rectangle_filldraw.code == "\\filldraw[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \path
    assert rectangle_path.code == "\\path[Blue] (2, 2) rectangle (3, 4);"
    # Ellipse : \fill
    assert ellipse_fill.code == "\\fill (0, 0) ellipse (3cm and 4cm);"
    # Ellipse : \filldraw
    assert ellipse_filldraw.code == "\\filldraw (0, 0) ellipse (3cm and 4cm);"
    # Ellipse :path
    assert ellipse_path.code == "\\path (0, 0) ellipse (3cm and 4cm);"
    # Arc : \fill
    assert (
        arc_fill.code
        == "\\fill (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \filldraw
    assert (
        arc_filldraw.code
        == "\\filldraw (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \path
    assert (
        arc_path.code
        == "\\path (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )


fills = [line_fill, plot_fill, circle_fill, rectangle_fill, ellipse_fill, arc_fill]
filldraws = [
    line_filldraw,
    plot_filldraw,
    circle_filldraw,
    rectangle_filldraw,
    ellipse_filldraw,
    arc_filldraw,
]
paths = [line_path, plot_path, circle_path, rectangle_path, ellipse_path, arc_path]


def test_action_reset_to_draw():
    """Test that resetting the action to "draw" returns the correct code."""
    for draw_obj in fills + filldraws + paths:
        draw_obj.action = "draw"
    assert (
        line_fill.code
        == "\\draw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \filldraw
    assert (
        line_filldraw.code
        == "\\draw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \path
    assert (
        line_path.code
        == "\\draw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Plot : \fill
    assert (
        plot_fill.code
        == "\\draw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \filldraw
    assert (
        plot_filldraw.code
        == "\\draw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \path
    assert (
        plot_path.code
        == "\\draw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Circle : \fill
    assert circle_fill.code == "\\draw[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \filldraw
    assert circle_filldraw.code == "\\draw[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \path
    assert circle_path.code == "\\draw[fill = purple] (1, 1) circle (1cm);"
    # Rectangle : \fill
    assert rectangle_fill.code == "\\draw[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \filldraw
    assert rectangle_filldraw.code == "\\draw[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \path
    assert rectangle_path.code == "\\draw[Blue] (2, 2) rectangle (3, 4);"
    # Ellipse : \fill
    assert ellipse_fill.code == "\\draw (0, 0) ellipse (3cm and 4cm);"
    # Ellipse : \filldraw
    assert ellipse_filldraw.code == "\\draw (0, 0) ellipse (3cm and 4cm);"
    # Ellipse :path
    assert ellipse_path.code == "\\draw (0, 0) ellipse (3cm and 4cm);"
    # Arc : \fill
    assert (
        arc_fill.code
        == "\\draw (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \filldraw
    assert (
        arc_filldraw.code
        == "\\draw (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \path
    assert (
        arc_path.code
        == "\\draw (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )


def test_action_reset_to_fill():
    """Test that resetting the action to "fill" returns the correct code."""
    for draw_obj in fills + filldraws + paths:
        draw_obj.action = "fill"
    assert (
        line_fill.code
        == "\\fill[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \filldraw
    assert (
        line_filldraw.code
        == "\\fill[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \path
    assert (
        line_path.code
        == "\\fill[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Plot : \fill
    assert (
        plot_fill.code
        == "\\fill[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \filldraw
    assert (
        plot_filldraw.code
        == "\\fill[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \path
    assert (
        plot_path.code
        == "\\fill[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Circle : \fill
    assert circle_fill.code == "\\fill[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \filldraw
    assert circle_filldraw.code == "\\fill[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \path
    assert circle_path.code == "\\fill[fill = purple] (1, 1) circle (1cm);"
    # Rectangle : \fill
    assert rectangle_fill.code == "\\fill[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \filldraw
    assert rectangle_filldraw.code == "\\fill[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \path
    assert rectangle_path.code == "\\fill[Blue] (2, 2) rectangle (3, 4);"
    # Ellipse : \fill
    assert ellipse_fill.code == "\\fill (0, 0) ellipse (3cm and 4cm);"
    # Ellipse : \filldraw
    assert ellipse_filldraw.code == "\\fill (0, 0) ellipse (3cm and 4cm);"
    # Ellipse :path
    assert ellipse_path.code == "\\fill (0, 0) ellipse (3cm and 4cm);"
    # Arc : \fill
    assert (
        arc_fill.code
        == "\\fill (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \filldraw
    assert (
        arc_filldraw.code
        == "\\fill (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \path
    assert (
        arc_path.code
        == "\\fill (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )


def test_action_reset_to_filldraw():
    """Test that resetting the action to "filldraw" returns the correct code."""
    for draw_obj in fills + filldraws + paths:
        draw_obj.action = "filldraw"
    assert (
        line_fill.code
        == "\\filldraw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \filldraw
    assert (
        line_filldraw.code
        == "\\filldraw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \path
    assert (
        line_path.code
        == "\\filldraw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Plot : \fill
    assert (
        plot_fill.code
        == "\\filldraw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \filldraw
    assert (
        plot_filldraw.code
        == "\\filldraw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \path
    assert (
        plot_path.code
        == "\\filldraw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Circle : \fill
    assert circle_fill.code == "\\filldraw[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \filldraw
    assert circle_filldraw.code == "\\filldraw[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \path
    assert circle_path.code == "\\filldraw[fill = purple] (1, 1) circle (1cm);"
    # Rectangle : \fill
    assert rectangle_fill.code == "\\filldraw[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \filldraw
    assert rectangle_filldraw.code == "\\filldraw[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \path
    assert rectangle_path.code == "\\filldraw[Blue] (2, 2) rectangle (3, 4);"
    # Ellipse : \fill
    assert ellipse_fill.code == "\\filldraw (0, 0) ellipse (3cm and 4cm);"
    # Ellipse : \filldraw
    assert ellipse_filldraw.code == "\\filldraw (0, 0) ellipse (3cm and 4cm);"
    # Ellipse :path
    assert ellipse_path.code == "\\filldraw (0, 0) ellipse (3cm and 4cm);"
    # Arc : \fill
    assert (
        arc_fill.code
        == "\\filldraw (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \filldraw
    assert (
        arc_filldraw.code
        == "\\filldraw (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \path
    assert (
        arc_path.code
        == "\\filldraw (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )


def test_action_reset_to_path():
    """Test that resetting the action to "path" returns the correct code."""
    for draw_obj in fills + filldraws + paths:
        draw_obj.action = "path"
    assert (
        line_fill.code
        == "\\path[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \filldraw
    assert (
        line_filldraw.code
        == "\\path[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Line : \path
    assert (
        line_path.code
        == "\\path[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Plot : \fill
    assert (
        plot_fill.code
        == "\\path[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \filldraw
    assert (
        plot_filldraw.code
        == "\\path[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Plot : \path
    assert (
        plot_path.code
        == "\\path[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Circle : \fill
    assert circle_fill.code == "\\path[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \filldraw
    assert circle_filldraw.code == "\\path[fill = purple] (1, 1) circle (1cm);"
    # Test Circle : \path
    assert circle_path.code == "\\path[fill = purple] (1, 1) circle (1cm);"
    # Rectangle : \fill
    assert rectangle_fill.code == "\\path[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \filldraw
    assert rectangle_filldraw.code == "\\path[Blue] (2, 2) rectangle (3, 4);"
    # Rectangle : \path
    assert rectangle_path.code == "\\path[Blue] (2, 2) rectangle (3, 4);"
    # Ellipse : \fill
    assert ellipse_fill.code == "\\path (0, 0) ellipse (3cm and 4cm);"
    # Ellipse : \filldraw
    assert ellipse_filldraw.code == "\\path (0, 0) ellipse (3cm and 4cm);"
    # Ellipse :path
    assert ellipse_path.code == "\\path (0, 0) ellipse (3cm and 4cm);"
    # Arc : \fill
    assert (
        arc_fill.code
        == "\\path (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \filldraw
    assert (
        arc_filldraw.code
        == "\\path (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
    # Arc : \path
    assert (
        arc_path.code
        == "\\path (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
