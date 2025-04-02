from tikzpy import TikzPicture, Point

node_radius = 0.5
node_sep = 2
layer_sep = 3

input_layer_pos = (0, 0)
hidden_layer_pos = (layer_sep, 0)

def network_layer(init_pos, num_nodes, symbol, color):
    layer_nodes = []
    for idx, _ in enumerate(range(num_nodes)):
        pos = Point(init_pos) + (0, -node_sep * idx)
        # Draw the circle
        circle = tikz.circle(pos, radius=node_radius, options=f"fill={color}!40")
        # Draw the node
        tikz.node(pos, text=f"${symbol}_{idx}$")
        layer_nodes.append(circle)
    return layer_nodes


def draw_layer_connection(curr_layer, next_layer):
    for curr_node in curr_layer:
        for next_node in next_layer:
            tikz.connect_circle_edges(curr_node, next_node, "->", dst_delta=0.1)

def draw_neural_network(layer_sizes):
    max_size = max(layer_sizes)
    layers = []
    init_pos = Point((0, 0))
    for idx, size in enumerate(layer_sizes):
        x_shift = idx * layer_sep
        y_shift = - (max_size - size) / 2 * node_sep
        pos = init_pos + (x_shift, y_shift)
        if idx == 0:
            symbol = "x"
            color = "green"
        elif idx == len(layer_sizes) - 1:
            symbol = "y"
            color = "red"
        else:
            symbol = f"h^{{({idx})}}"
            color = "blue"

        nodes = network_layer(pos, size, symbol, color)
        layers.append(nodes)

    for idx, layer in enumerate(range(len(layers) - 1)):
        draw_layer_connection(layers[idx], layers[idx + 1])


if __name__ == "__main__":
    tikz = TikzPicture(center=True)
    draw_neural_network([4, 5, 3, 4, 3, 2])
    tikz.show()

