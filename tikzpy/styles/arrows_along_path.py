from tikzpy.tikz_environments.tikz_style import TikzStyle

""" We implement a style that allows us to draw arrows on paths. This wonderful 
    design was created by Paul Gaborit here:
    https://tex.stackexchange.com/questions/3161/tikz-how-to-draw-an-arrow-in-the-middle-of-the-line/69225#69225
"""

arrows_along_path = TikzStyle(
    "arrows_along_path", "postaction={on each segment={mid arrow=#1}}"
)

on_each_segment = TikzStyle(
    "on each segment",
    """decorate,
    decoration={
      show path construction,
      moveto code={},
      lineto code={
        \\path [#1]
        (\\tikzinputsegmentfirst) -- (\\tikzinputsegmentlast);
      },
      curveto code={
        \\path [#1] (\\tikzinputsegmentfirst)
        .. controls
        (\\tikzinputsegmentsupporta) and (\\tikzinputsegmentsupportb)
        ..
        (\\tikzinputsegmentlast);
      },
      closepath code={
        \\path [#1]
        (\\tikzinputsegmentfirst) -- (\\tikzinputsegmentlast);
      },
    }
    """,
)

mid_arrow = TikzStyle(
    "mid arrow",
    """
    postaction={decorate,decoration={
        markings,
        mark=at position .5 with {\\arrow[#1]{stealth}}
    }}
    """,
)

arrows_along_path_style = [arrows_along_path, on_each_segment, mid_arrow]
