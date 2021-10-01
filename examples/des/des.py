from tikzpy import TikzPicture

tikz = TikzPicture(center=True, options=">=stealth, thick")

# Plaintext
plaintext = tikz.rectangle((0, 0), (4, 0.8))
tikz.node(plaintext.center, text="Plaintext")

to_IP = tikz.line(plaintext.south, plaintext.south - (0, 0.5), options="->")
# IP
IP = tikz.rectangle(options="rounded corners").set_north(to_IP.end, height=0.7, width=2)  # Rectangle who's .north position is the end of IP
tikz.node(IP.center, text="IP")
vertical = tikz.line(IP.south, IP.south - (0, 0.8))

# Horizontal lines 
h1 = tikz.line(vertical.end, vertical.end - (5, 0))
h2 = tikz.line(vertical.end, vertical.end + (5, 0))

# To the blocks
to_left_block = tikz.line(h1.end, h1.end - (0, 0.5), options="->")
to_right_block = tikz.line(h2.end, h2.end - (0, 0.5), options="->")

def DES_round(to_left_block, to_right_block, left_label, right_label, K_i=None, dotted=False, is_last_block=False):
    # Left block
    L_0 = tikz.rectangle().set_north(to_left_block.end, height=1, width=5)
    tikz.node(L_0.center, text=left_label)
    
    # Right block
    R_0 = tikz.rectangle().set_north(to_right_block.end, height=1, width=5)
    tikz.node(R_0.center, text=right_label)

    # Line to the XOR symbol
    to_xor = tikz.line(L_0.south, L_0.south - (0, 0.5))

    # Draw the XOR symbol
    XOR = tikz.circle(to_xor.end - (0, 0.25), radius=0.25)
    tikz.line(XOR.north, XOR.south)
    tikz.line(XOR.west, XOR.east)
    
    # Line to the dot
    to_dot = tikz.line(R_0.south, (R_0.south.x, XOR.center.y))
    # Draw the dot symbol
    dot = tikz.circle(to_dot.end, radius=0.1, options="fill")

    # Function f 
    function_f = tikz.circle((dot.center + XOR.center) / 2 , radius = 0.5)
    tikz.node(function_f.center, text="$f$")

    # Line from dot to function f
    to_f = tikz.line(dot.west, function_f.east, options="->")
    # Line from function f to XOR symbol
    from_f = tikz.line(function_f.west, XOR.east, options="->")

    # From XOR to the right block
    from_XOR = tikz.line(XOR.south, (XOR.south.x, dot.south.y - 0.5))
    XOR_diagonal = tikz.line(from_XOR.end, (dot.center.x, from_XOR.end.y - 0.75))
    to_next_right_block = tikz.line(XOR_diagonal.end, XOR_diagonal.end - (0, 0.25),  options="->")    

    # From dot to left block block
    from_dot = tikz.line(dot.south, dot.south - (0, 0.5))
    dot_diagonal = tikz.line(from_dot.end, (XOR.center.x, from_dot.end.y - 0.75))
    to_next_left_block = tikz.line(dot_diagonal.end, dot_diagonal.end - (0, 0.25), options="->")
    
    # Dot the diagonal lines to show there are hidden steps
    if dotted:
        XOR_diagonal.options = "dotted"
        dot_diagonal.options = "dotted"

    # Incoming key 
    if K_i is not None:
        joint = tikz.line(from_dot.midpoint() + (1, -0.2), (to_f.midpoint().x, from_dot.midpoint().y - 0.2))
        tikz.line(joint.end, function_f.point_at_arg(-30), options="->")
        tikz.node(joint.start + (0.3, 0), text=K_i)    

    # If last block, straighten the diagonals so that they are vertical lines
    if is_last_block:
        XOR_diagonal.end = (XOR_diagonal.start.x, XOR_diagonal.end.y)
        dot_diagonal.end = (dot_diagonal.start.x, dot_diagonal.end.y)


    return to_next_left_block, to_next_right_block


next_left_block, next_right_block = DES_round(to_left_block, to_right_block, "$L_0$", "$R_0$", "$K_1$" )
next_left_block, next_right_block = DES_round(next_left_block, next_right_block, "$L_1=R_0$", "$R_1 = L_0 \oplus f(R_0, K_1)$", "$K_2$")
next_left_block, next_right_block = DES_round(next_left_block, next_right_block, "$L_2=R_1$", "$R_2 = L_1 \oplus f(R_1, K_2)$", dotted=True)
next_left_block, next_right_block = DES_round(next_left_block, next_right_block, "$L_{15}=R_{14}$", "$R_{15} = L_{14} \oplus f(R_{14}, K_{15})$", "$K_{16}$", is_last_block=True)

# Left block
L_0 = tikz.rectangle().set_north(next_left_block.end, height=1, width=5)
tikz.node(L_0.center, text="$R_{16} = L_{15}\oplus f(R_{15}, K_{16})$")

# Right block
R_0 = tikz.rectangle().set_north(next_right_block.end, height=1, width=5)
tikz.node(R_0.center, text="$L_{16} = R_{15}$")

# Leaving the blocks 
from_left_block = tikz.line(L_0.south, L_0.south - (0, 0.5))
from_right_block = tikz.line(R_0.south, R_0.south - (0, 0.5))

# Horizontal lines to the middle
h1 = tikz.line(from_left_block.end, (to_IP.end.x, from_left_block.end.y))
h2 = tikz.line(from_right_block.end, (to_IP.end.x, from_right_block.end.y))

# Line to IP inverse
to_IP_inv = tikz.line(h1.end, h1.end - (0, 0.5), options="->")
IP_inv = tikz.rectangle(options="rounded corners").set_north(to_IP_inv.end, height=0.7, width=2)

# IP rectangle
tikz.node(IP_inv.center, text="$\\text{IP}^{-1}$")
to_cipher_text = tikz.line(IP_inv.south, IP_inv.south - (0, 0.5), options="->")

# Ciphertext rectangle
cipher_text = tikz.rectangle().set_north(to_cipher_text.end, height=0.8, width=4)
tikz.node(cipher_text.center, text="Ciphertext")
tikz.write()
tikz.show()


