import pytest
import tikzpy
from tikzpy.utils.helpers import replace_code


def test_replacement_1():
    # Test primary update functionality given the existence of valid delimiters to update text in
    begin_delim = "start"
    end_delim = "end"
    content = """
    start
    This } ! @ is $ % a ^ test, & * I'm going to ( ~ ` get ) = _ - { replaced. 
    end
    It doesn't grab this end, right?
    """
    replacement_text = "start Hi! end"
    updated_text, num_matches = replace_code(
        begin_delim, end_delim, content, replacement_text
    )
    assert (
        updated_text
        == """
    start Hi! end
    It doesn't grab this end, right?
    """
    )


def test_multiple_environments():
    # Test that multiple environments can be used and updated independently
    tikz = tikzpy.TikzPicture()
    tikz.circle((0, 0), 3, options="thin, fill=orange!15")

    arc_one = tikz.arc((3, 0), 0, 180, x_radius=3, y_radius=1.5, options=f"dashed")
    arc_two = tikz.arc((-3, 0), 180, 360, x_radius=3, y_radius=1.5)

    tikz.write()  # Writes the Tikz code into a file
