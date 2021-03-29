import re

"""
    Functions for colors
"""


def rgb(r, g, b):
    """A wrapper function that outputs xcolor/Tikz code for coloring via rgb values.

    When calling rgb, it is necessary to specify "color = " or "fill =" right before.
    E.g., tikz.line(... options = "color =" + rgb(r,g,b) ...)

    This is an annoying aspect with Tikz.
    """
    return f"{{ rgb,255:red, {r}; green, {g}; blue, {b} }}"


def rainbow_colors(i):
    """A wrapper function for obtaining rainbow colors.
    Any integer can be passed in.
    """
    return rainbow_cols[i % len(rainbow_cols)]


def xcolors(i):
    """A wrapper function to obtain xcolors.
    Any integer is valid.
    """
    return xcols[i % len(xcols)]


"""
    Miscellaneous Helpers
"""


def brackets(string):
    """A helper function for creating tikz code.
    Basically, if the string is empty, we don't obtain brackets [].
    """
    if len(string) != 0:
        return "[" + string + "]"
    else:
        return ""


def tex_escape(text):
    """
    :param text: a plain text message
    :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }
    regex = re.compile(
        "|".join(
            re.escape(str(key))
            for key in sorted(conv.keys(), key=lambda item: -len(item))
        )
    )
    return regex.sub(lambda match: conv[match.group()], text)


# Collect xcolor names
xcols = [
    "Apricot",
    "Aquamarine",
    "Bittersweet",
    "Black",
    "Blue",
    "BlueGreen",
    "BlueViolet",
    "BrickRed",
    "Brown",
    "BurntOrange",
    "CadetBlue",
    "CarnationPink",
    "Cerulean",
    "CornflowerBlue",
    "Cyan",
    "Dandelion",
    "DarkOrchid",
    "Emerald",
    "ForestGreen",
    "Fuchsia",
    "Goldenrod",
    "Gray",
    "Green",
    "GreenYellow",
    "JungleGreen",
    "Lavender",
    "LimeGreen",
    "Magenta",
    "Mahogany",
    "Maroon",
    "Melon",
    "MidnightBlue",
    "Mulberry",
    "NavyBlue",
    "OliveGreen",
    "Orange",
    "OrangeRed",
    "Orchid",
    "Peach",
    "Periwinkle",
    "PineGreen",
    "Plum",
    "ProcessBlue",
    "Purple",
    "RawSienna",
    "Red",
    "RedOrange",
    "RedViolet",
    "Rhodamine",
    "RoyalBlue",
    "RoyalPurple",
    "RubineRed",
    "Salmon",
    "SeaGreen",
    "Sepia",
    "SkyBlue",
    "SpringGreen",
    "Tan",
    "TealBlue",
    "Thistle",
    "Turquoise",
    "Violet",
    "VioletRed",
    "White",
    "WildStrawberry",
    "Yellow",
    "YellowGreen",
    "YellowOrange",
]

rainbow_cols = [
    "{rgb,255:red, 255; green, 0; blue, 0 }",  # red
    "{rgb,255:red, 255; green, 125; blue, 0 }",  # orange
    "{rgb,255:red, 255; green, 255; blue, 0 }",  # yellow
    "{rgb,255:red, 125; green, 255; blue, 0 }",  # spring
    "{rgb,255:red, 0; green, 255; blue, 0 }",  # green
    "{rgb,255:red, 0; green, 255; blue, 125 }",  # turquoise
    "{rgb,255:red, 0; green, 255; blue, 255 }",  # cyan
    "{rgb,255:red, 0; green, 125; blue, 255 }",  # ocean
    "{rgb,255:red, 0; green, 0; blue, 255 }",  # blue
    "{rgb,255:red, 125; green, 0; blue, 255 }",  # violet
    "{rgb,255:red, 255; green, 0; blue, 12 }",  # magenta
    "{rgb,255:red, 255; green, 0; blue, 255 }",  # raspberry
]
