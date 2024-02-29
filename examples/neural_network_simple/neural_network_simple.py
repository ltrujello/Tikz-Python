import math
from tikzpy import TikzPicture

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
    tikz = TikzPicture()
    layers = []
    horiz_space = 3
    vert_space = 2.5
    radius=0.25
    epsilon = 0.3

    # x_0 node
    x_0_node = tikz.circle((0, vert_space), radius)
    tikz.node((0, vert_space + radius + epsilon), text="$x_1$")
    # x_2 node
    x_1_node = tikz.circle((0, 0), radius)
    tikz.node((0, 0 + radius + epsilon), text="$x_2$")
    # x_2 node
    x_2_node = tikz.circle((0, -vert_space), radius)
    tikz.node(x_2_node.center + (0, radius + epsilon), text="$1$")

    # h_0 node
    h_0_node = tikz.circle((horiz_space, vert_space), radius)
    tikz.node((horiz_space, vert_space + radius + epsilon), text="$h_1$")
    # h_1 node
    h_1_node = tikz.circle((horiz_space, 0), radius)
    tikz.node((horiz_space, 0 + radius + epsilon), text="$h_2$")
    # h_2 node
    h_2_node = tikz.circle((horiz_space, -vert_space), radius)
    tikz.node((horiz_space, -vert_space + radius + epsilon), text="$1$")

    # Add the final output layer
    x_2 = 1.75*horiz_space
    y_2 = 0

    output_node = tikz.circle((x_2, y_2), radius)
    tikz.node((x_2, y_2 + radius + epsilon), text="$y$")

    layers = [[x_0_node, x_1_node, x_2_node], [h_0_node, h_1_node, h_2_node], [output_node]]

    # Draw labels for hidden layer
    lines = []
    for i in range(len(layers) - 1):
        curr_nodes = layers[i]
        next_nodes = layers[i + 1]

        for ind, node in enumerate(curr_nodes):
            pos_a = node.center
            rad_a = node.radius
            for j, next_node in enumerate(next_nodes):
                if i == 0 and j == len(next_nodes) - 1:
                    continue
                pos_b = next_node.center
                rad_b = next_node.radius
                start, end = calc_start_end_between_nodes(pos_a, rad_a, pos_b, rad_b)
                lines.append(tikz.line(start, end, options="->"))

    # label the weights in the hidden layer
    tikz.node(lines[0].pos_at_t(0.5), options="above", text="3")
    tikz.node(lines[1].pos_at_t(0.2), options="above", text="4")
    tikz.node(lines[2].pos_at_t(0.2), options="above", text="2")
    tikz.node(lines[3].pos_at_t(0.3), options="above", text="3")
    # label the biases in the first layer 
    tikz.node(lines[4].pos_at_t(0.2), options="left", text="-2")
    tikz.node(lines[5].pos_at_t(0.5), options="below", text="-4")

    # label the weights in the final layer 
    tikz.node(lines[6].pos_at_t(0.4), options="right", text="5")
    tikz.node(lines[7].pos_at_t(0.5), options="above", text="-5")
    # label the bias in the final layer 
    tikz.node(lines[8].pos_at_t(0.5), options="left", text="-2")

    tikz.show()
