import math
from tikzpy import TikzPicture, Point
tikz = TikzPicture()
radius = 0.25

x_2 = 6
y_2 = 2
epsilon = 0.3

horiz_space = 3
vert_space = 1.25
def calc_start_end_between_nodes(pos_a, rad_a, pos_b, rad_b):
    x_1, y_1 = pos_a
    x_2, y_2 = pos_b
    if y_1 - y_2 == 0:
        theta = math.pi/2
    else:
        theta = math.atan(abs(x_2 - x_1) / abs(y_1 - y_2))

    if y_2 > y_1:
        start = (x_1 + radius * math.sin(theta), y_1 + radius* math.cos(theta))
        end = (x_2 - radius * math.sin(theta), y_2 - radius * math.cos(theta))
    else:
        start = (x_1 + radius * math.sin(theta), y_1 - radius* math.cos(theta))
        end = (x_2 - radius * math.sin(theta), y_2 + radius * math.cos(theta))
    return start, end

if __name__ == "__main__":
    layers = []
    num_nodes = 4
    for layer in range(2):
        layer_nodes = []
        for i in range(num_nodes):
            x_1 = layer * horiz_space
            y_1 = (num_nodes - 1 - i) * vert_space

            layer_node = tikz.circle((x_1, y_1), radius)
            # Draw the input x_i or hidden layer
            if layer == 0:
                tikz.node((x_1, y_1 + radius + epsilon), text=f"$x_{i + 1}$")
            else:
                tikz.node((x_1, y_1 + radius + epsilon), text=f"$h_{i + 1}$")
            layer_nodes.append(layer_node)
        layers.append(layer_nodes)
    # Add the final output layer
    layer_node = tikz.circle((x_2, y_2), radius)
    layers.append([layer_node])
    # Draw label for output node
    tikz.node((x_2, y_2 + radius + epsilon), text="$y$")

    for i in range(len(layers) - 1):
        curr_nodes = layers[i]
        next_nodes = layers[i + 1]

        for node in curr_nodes:
            pos_a = node.center
            rad_a = node.radius
            for next_node in next_nodes:
                pos_b = next_node.center
                rad_b = next_node.radius
                start, end = calc_start_end_between_nodes(pos_a, rad_a, pos_b, rad_b)
                tikz.line(start, end, options="->")

    tikz.show()
