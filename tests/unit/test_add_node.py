import tikzpy

tikz = tikzpy.TikzPicture()
# Line
line = tikz.line(
    (0, 0), (1, 1), options="thin, Green", control_pts=[(0.5, 0.9), (1, -2)]
)
# Plot
plot = tikz.plot_coordinates(
    points=[(1, 1), (2, 2), (3, 3), (2, -4)],
    options="purple",
    plot_options="smooth cycle",
)
# Circle
circle = tikz.circle((1, 1), 1, options="fill=red")
# Rectangle
rectangle = tikz.rectangle((2, 2), 1, 2, options="thick")
# Ellipse
ellipse = tikz.ellipse((0, 0), 3, 4, options="fill=Blue")
# Arc
arc = tikz.arc((0, 0), 20, 90, 4, options="fill=purple")


def test_add_node():
    # Add nodes
    line.add_node(options="below", text="$\\int$!")
    plot.add_node(options="above", text="$\\partial$!")
    circle.add_node(options="left", text="hello")
    rectangle.add_node(options="right", text="Wow!")
    ellipse.add_node(options="right", text="Wow!")
    arc.add_node(options="left")

    assert (
        line.code
        == r"\draw[thin, Green] (0, 0) .. controls (0.5, 0.9) and (1, -2)  .. (1, 1) node[below] { $\int$! };"
    )
    assert (
        plot.code
        == r"\draw[purple] plot[smooth cycle] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) } node[above] { $\partial$! };"
    )
    assert circle.code == r"\draw[fill=red] (1, 1) circle (1cm) node[left] { hello };"
    assert (
        rectangle.code == r"\draw[thick] (2, 2) rectangle (3, 4) node[right] { Wow! };"
    )
    assert (
        ellipse.code
        == r"\draw[fill=Blue] (0, 0) ellipse (3cm and 4cm) node[right] { Wow! };"
    )
    assert (
        arc.code
        == r"\draw[fill=purple] (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm] node[left] {  };"
    )


def test_add_and_update():
    # Add nodes
    line.add_node(options="below", text="$\\int$!")
    plot.add_node(options="above", text="$\\partial$!")
    circle.add_node(options="left", text="hello")
    rectangle.add_node(options="right", text="Wow!")
    ellipse.add_node(options="right", text="Wow!")
    arc.add_node(options="left")

    line.node.position = (3, 3)
    line.node.options = "above"
    line.node.text = "Replace"
    assert (
        line.code
        == r"\draw[thin, Green] (0, 0) .. controls (0.5, 0.9) and (1, -2)  .. (1, 1) node[above] at (3, 3) { Replace };"
    )
    plot.node.position = (3, 3)
    plot.node.options = "above"
    plot.node.text = "Replace"
    assert (
        plot.code
        == r"\draw[purple] plot[smooth cycle] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) } node[above] at (3, 3) { Replace };"
    )
    circle.node.position = (3, 3)
    circle.node.options = "above"
    circle.node.text = "Replace"
    assert (
        circle.code
        == r"\draw[fill=red] (1, 1) circle (1cm) node[above] at (3, 3) { Replace };"
    )
    rectangle.node.position = (3, 3)
    rectangle.node.options = "above"
    rectangle.node.text = "Replace"
    assert (
        rectangle.code
        == r"\draw[thick] (2, 2) rectangle (3, 4) node[above] at (3, 3) { Replace };"
    )
    ellipse.node.position = (3, 3)
    ellipse.node.options = "above"
    ellipse.node.text = "Replace"
    assert (
        ellipse.code
        == r"\draw[fill=Blue] (0, 0) ellipse (3cm and 4cm) node[above] at (3, 3) { Replace };"
    )
    arc.node.position = (3, 3)
    arc.node.options = "above"
    arc.node.text = "Replace"
    assert (
        arc.code
        == r"\draw[fill=purple] (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm] node[above] at (3, 3) { Replace };"
    )


def test_add_nodes_manually():
    pass
