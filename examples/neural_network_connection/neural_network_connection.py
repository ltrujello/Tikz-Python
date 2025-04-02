from tikzpy import TikzPicture

tikz = TikzPicture(center=True) # center it in the PDF
radius = 0.25
pos_a = (0, 0)
pos_b = (4, 1)

# Draw the nodes
node_a = tikz.circle(pos_a, radius)
node_b = tikz.circle(pos_b, radius)

# Draw the line between the nodes
line = tikz.connect_circle_edges(node_a, node_b)
line.options = "->"

# Annotate the drawing with mathematical variables
h_j = tikz.node(node_a.center + (0.3, 0.75), text="$h_j^{(n-1)}$")
h_i = tikz.node(node_b.center + (0.3, 0.75), text="$h_i^{(n)}$")
w_ij = tikz.node(line.pos_at_t(0.5) + (0, 0.5), text="$w_{ij}^{(n)}$")

# Add ellipses on each side to illustrate more nodes are present
tikz.node(node_a.center + (0, 1.5), text="\\vdots")
tikz.node(node_a.center + (0, -0.75), text="\\vdots")
tikz.node(node_b.center + (0, 1.5), text="\\vdots")
tikz.node(node_b.center + (0, -0.75), text="\\vdots")
tikz.show()

