from tikzpy import (
    TikzPicture,
    Rectangle,
    Point,
    Line,
    PlotCoordinates,
    Scope,
)

tikz = TikzPicture(center=True)

# Positions
ORIGIN = Point(0, 0)
input_pos = ORIGIN
output_pos = ORIGIN + (4.5, 0)
encoder_pos = ORIGIN + (0, 3)
decoder_pos = ORIGIN + (output_pos.x - 0.5, 3)

# Encoder block dimensions
encoder_w = 4.5
encoder_h = 8

# Decoder block dimensions
decoder_w = encoder_w
decoder_h = 12.7

# Other layer block dimensions
layer_block_width = 3
embedding_h = 1.25
linear_h = 0.5


def input_block(position):
    input = tikz.rectangle_from_center(
        position, width=layer_block_width, height=embedding_h, options="fill=red!10"
    )
    tikz.node(input.center, options="align=center", text="Input \\\\ Embedding")
    tikz.node(input.south - (0, 1), text="Inputs")
    tikz.line(input.south - (0, 0.7), input.south)
    return input


def output_block(position):
    output = tikz.rectangle_from_center(
        position, width=layer_block_width, height=embedding_h, options="fill=red!10"
    )
    tikz.node(output.center, options="align=center", text="Output \\\\ Embedding")
    tikz.line(output.south - (0, 0.7), output.south)
    tikz.node(
        output.south - (0, 1.25),
        options="align=center",
        text="Outputs \\\\ (shifted right)",
    )
    return output


def encoder_block(position):
    encoder = tikz.rectangle_from_south(
        position, width=encoder_w, height=encoder_h, options="fill=gray!10"
    )
    return encoder


def decoder_block(position):
    decoder = tikz.rectangle_from_south(
        position, width=decoder_w, height=decoder_h, options="fill=gray!10"
    )
    return decoder


def linear_block(position):
    linear = tikz.rectangle_from_south(
        position, width=layer_block_width, height=linear_h, options="fill=gray!10"
    )
    tikz.node(linear.center, options="align=center", text="Linear")
    return linear


def softmax_block(position):
    softmax = tikz.rectangle_from_south(
        position, width=layer_block_width, height=linear_h, options="fill=green!10"
    )
    tikz.node(softmax.center, options="align=center", text="Softmax")
    output_arrow = tikz.line(softmax.north, softmax.north + (0, 0.5))
    tikz.node(
        output_arrow.end + (0, 0.6),
        options="align=center",
        text="Output \\\\ Probabilities",
    )
    return softmax


def multihead_attention(position):
    attn = tikz.rectangle_from_south(
        position,
        width=layer_block_width,
        height=embedding_h,
        options="fill=Orange!10",
    )
    tikz.node(attn.center, options="align=center", text="Multi-Head \\\\ Attention")
    return attn


def masked_multihead_attention(position):
    attn = tikz.rectangle_from_south(
        position,
        width=layer_block_width,
        height=embedding_h + 0.5,
        options="fill=Orange!10",
    )
    tikz.node(
        attn.center,
        options="align=center",
        text="Masked \\\\ Multi-Head \\\\ Attention",
    )
    return attn


def add_block(position):
    add = tikz.rectangle_from_south(
        position,
        width=layer_block_width,
        height=linear_h,
        options="fill=Yellow!10",
    )
    tikz.node(add.center, text="Add")
    return add


def feedforward(position):
    ff = tikz.rectangle_from_south(
        position,
        width=layer_block_width,
        height=embedding_h,
        options="fill=ProcessBlue!10",
    )
    tikz.node(ff.center, options="align=center", text="Feed \\\\ Forward")
    return ff


def layer_norm(position):
    layer_norm = tikz.rectangle_from_south(
        position,
        width=layer_block_width,
        height=linear_h,
        options="fill=Purple!10",
    )
    tikz.node(layer_norm.center, options="align=center", text="LayerNorm")
    return layer_norm


def positional_encoding(pos):
    scope = Scope()
    circle = scope.circle(pos, radius=0.5, options="ultra thick")
    scope.arc(
        circle.center, 0, 180, radius=0.25, draw_from_start=True, options="very thick"
    )
    scope.arc(
        circle.center, 180, 360, radius=0.25, draw_from_start=True, options="very thick"
    )
    tikz.draw(scope)
    return circle


def add_symbol(pos, flip=True):
    scope = Scope()
    eps = 0.1
    circle = scope.circle(pos, radius=0.25, options="very thick")
    scope.line(circle.north - (0, eps), circle.south + (0, eps), options="very thick")
    scope.line(circle.west + (eps, 0), circle.east - (eps, 0), options="very thick")
    tikz.draw(scope)

    if flip:
        pos_enc = positional_encoding(circle.east + (2, 0))
        tikz.line(pos_enc.west, circle.east, options=" ")
        tikz.node(
            pos_enc.east + (1.2, 0),
            options="align=center",
            text="Positional \\\\ Encoding",
        )
    else:
        pos_enc = positional_encoding(circle.west - (2, 0))
        tikz.line(pos_enc.east, circle.west, options=" ")
        tikz.node(
            pos_enc.west - (1.2, 0),
            options="align=center",
            text="Positional \\\\ Encoding",
        )

    return circle

def draw_fork_line(start, end):
    line = tikz.line(start, end)
    tikz.plot_coordinates(
        [line.pos_at_t(0.4), line.pos_at_t(0.4) + (1, 0), end + (1, 0)]
    )
    tikz.plot_coordinates(
        [line.pos_at_t(0.4), line.pos_at_t(0.4) - (1, 0), end - (1, 0)]
    )
    return line

def draw_three_parallel_lines(start, end):
    line = tikz.line(start, end)
    tikz.line(
        start - (1, 0), end - (1, 0)
    )
    tikz.line(
        start + (1, 0), end + (1, 0)
    )
    return line

def draw_left_rectangular_arrow(start, end):
    left_shift = 2.45
    tikz.plot_coordinates(
        [
            start,
            start - (left_shift, 0),
            ((start + (-left_shift, 0)).x, end.y),
            end,
        ]
    )

def draw_right_rectangular_arrow(start, end):
    right_shift = 2.25
    tikz.plot_coordinates(
        [
            start,
            start + (right_shift, 0),
            ((start + (right_shift, 0)).x, end.y),
            end,
        ]
    )

# Input/Output blocks
input = input_block(input_pos)
output = output_block(output_pos)

# Endoder/Decoder blocks
encoder = encoder_block(input.north + (-0.4, 2))
decoder = decoder_block(output.north + (0.4, 2))

# Linear layer block
linear = linear_block((output_pos.x, decoder.north.y + 0.5))

# Softmax layer block
softmax = softmax_block(linear.north + (0, 0.5))

# Encoder components
encoder_layer_norm_1 = layer_norm((input_pos.x, encoder.south.y + 0.75))
encoder_attn = multihead_attention(encoder_layer_norm_1.north + (0, 0.7))
encoder_add_1 = add_block(encoder_attn.north + (0, 0.15))
encoder_layer_norm_2 = layer_norm(encoder_add_1.north + (0, 0.75))
encoder_feed_forward = feedforward(encoder_layer_norm_2.north + (0, 0.7))
encoder_add_2 = add_block(encoder_feed_forward.north + (0, 0.15))

# Decoder components
decoder_layer_norm_1 = layer_norm((output_pos.x, decoder.south.y + 0.75))
decoder_attn = masked_multihead_attention(decoder_layer_norm_1.north + (0, 0.7))
decoder_add_1 = add_block(decoder_attn.north + (0, 0.15))
decoder_layer_norm_2 = layer_norm(decoder_add_1.north + (0, 1))
encoder_decoder_attn = multihead_attention(decoder_layer_norm_2.north + (0, 0.7))
decoder_add_2 = add_block(encoder_decoder_attn.north + (0, 0.15))
decoder_layer_norm_3 = layer_norm(decoder_add_2.north + (0, 0.75))
decoder_feed_forward = feedforward(decoder_layer_norm_3.north + (0, 0.7))
decoder_add_3 = add_block(decoder_feed_forward.north + (0, 0.15))

# Encoder connections
draw_left_rectangular_arrow(encoder_layer_norm_1.south - (0, 0.5), encoder_add_1.west)
line = tikz.line(encoder_add_1.north, encoder_layer_norm_2.south)
draw_left_rectangular_arrow(line.pos_at_t(0.5), encoder_add_2.west)

# Encoder to Decoder connection
encoder_decoder_line = tikz.plot_relative_coordinates(
    [encoder_add_2.north, (0, 0.7), (2.3, 0), (0, -3.7), (0.5, 0)],
    options=" ",
)
tikz.plot_coordinates(
    [
        encoder_decoder_line.points[-1],
        (decoder_layer_norm_2.south.x - 1, encoder_decoder_line.points[-1].y),
        decoder_layer_norm_2.south - (1, 0),
    ]
)
tikz.plot_coordinates(
    [
        encoder_decoder_line.points[-1],
        (decoder_layer_norm_2.south.x, encoder_decoder_line.points[-1].y),
        decoder_layer_norm_2.south,
    ]
)

# Decoder connections
draw_right_rectangular_arrow(decoder_layer_norm_1.south - (0, 0.5), decoder_add_1.east)
tikz.plot_relative_coordinates([decoder_add_1.north, (0, 0.5), (1, 0), (0, 0.5)])
draw_right_rectangular_arrow(decoder_add_1.north + (0, 0.25), decoder_add_2.east)
line = tikz.line(decoder_add_2.north, decoder_layer_norm_3.south)
draw_right_rectangular_arrow(line.pos_at_t(0.5), decoder_add_3.east)
draw_three_parallel_lines(decoder_layer_norm_2.north, encoder_decoder_attn.south)

# Three prong fork connections
draw_fork_line(encoder_layer_norm_1.north, encoder_attn.south)
draw_fork_line(decoder_layer_norm_1.north, decoder_attn.south)

# Straight line connections
tikz.line(encoder_layer_norm_2.north, encoder_feed_forward.south)
tikz.line(decoder_layer_norm_3.north, decoder_feed_forward.south)

# Connections to add blocks, they don't have arrow tips.
tikz.line(encoder_attn.north, encoder_add_1.south, options=" ")
tikz.line(encoder_feed_forward.north, encoder_add_2.south, options=" ")
tikz.line(decoder_attn.north, decoder_add_1.south, options=" ")
tikz.line(encoder_decoder_attn.north, decoder_add_2.south, options=" ")
tikz.line(decoder_feed_forward.north, decoder_add_3.south, options=" ")

# Linear and softmax connections
tikz.line(decoder_add_3.north, linear.south)
tikz.line(linear.north, softmax.south)

# Encoder add symbol and input connection 
encoder_add_symbol = add_symbol(input.north + (0, 0.9), flip=False)
tikz.line(input.north, encoder_add_symbol.south)
tikz.line(encoder_add_symbol.north, encoder_layer_norm_1.south)

# Decoder add symbol and output connection
decoder_add_symbol = add_symbol(output.north + (0, 0.9))
tikz.line(output.north, decoder_add_symbol.south)
tikz.line(decoder_add_symbol.north, decoder_layer_norm_1.south)

# Labels
tikz.node(encoder.west - (0.7, 0), text="$N \\times$")
tikz.node(decoder.east + (0.7, 0), text="$N \\times$")

# Styling
for obj in tikz.drawing_objects:
    if isinstance(obj, Rectangle):
        obj.options = f"{obj.options}, rounded corners=4pt, ultra thick"

    if isinstance(obj, Line):
        if len(obj.options) == 0:
            obj.options = "ultra thick, ->, >=stealth"
        else:
            obj.options = "ultra thick"

    if isinstance(obj, PlotCoordinates):
        if len(obj.options) == 0:
            obj.options = (
                "rounded corners, rounded corners=7pt, ultra thick, ->, >=stealth"
            )
        else:
            obj.options = (
                "rounded corners, rounded corners=7pt, ultra thick"
            )
tikz.show()
