import shutil
from tikzpy import TikzPicture
from pathlib import Path
from tikzpy.utils.helpers import replace_code

# Run with: pytest -vv -s test_code_update.py
# The tests make sure the file input and update procedures work correctly.


def clear_test_code():
    """Reset the tikzpy picture count and clear the tikz_code directory."""
    TikzPicture.NUM_TIKZS = 0
    tikz_code_dir = Path("tikz_code")
    if tikz_code_dir.exists():
        shutil.rmtree(tikz_code_dir)


def test_replace_code():
    """Test the function replace_code and its update functionality. Check that it correctly replaces text surrounded
    by delimiters."""
    delimiter_pairs = [
        ("start", "end"),
        ("<", ">"),
        ("%__begin__@TikzPy__#id__==__(0)", "%__end__@TikzPy__#id__==__(0)"),
        ("%__begin__@TikzPy__#id__==__(10)", "%__end__@TikzPy__#id__==__(10)"),
    ]
    for delimiter_pair in delimiter_pairs:
        begin, end = delimiter_pair
        content = f"""
        {begin} This ! @ is $ % a 
        ^ test, & * I'm 
        going to ( ~ ` 
        get ) = _ - replaced.
        {end}
        It doesn't grab this end, right?
        """
        replacement_text = f"{begin} Hi! {end}"
        updated_text, num_matches = replace_code(begin, end, content, replacement_text)
        assert (
            updated_text
            == f"""
        {begin} Hi! {end}
        It doesn't grab this end, right?
        """
        )


def test_updating_environment():
    """Test that making a second change to a Tikz environment, after initially compiling, works correctly."""
    clear_test_code()
    code_dir = Path("test_code_update") / "test_updating_environment"

    tikz = TikzPicture()
    tikz.rectangle((0, 0), (3, 3), options="fill=red")
    tikz.write()
    before_code = code_dir / "before.tex"

    assert tikz.tikz_file.read_text() == before_code.read_text()

    # Now update the environment
    tikz.arc((3, 3), start_angle=20, end_angle=90, radius=5, options="Blue!40")
    tikz.write()
    after_code = code_dir / "after.tex"

    assert tikz.tikz_file.read_text() == after_code.read_text()


def test_creating_multiple_environments():
    """Test that we can create multiple independent tikz environments in the same process."""
    clear_test_code()
    code_dir = Path("test_code_update") / "test_creating_multiple_environments"

    # First environment
    first_tikz = TikzPicture()
    first_tikz.circle((0, 0), 3, options="thin, fill=orange!15")
    first_tikz.write()  # Writes the Tikz code into a file
    first_environment = code_dir / "first_environment.tex"

    assert first_tikz._id == "@TikzPy__#id__==__(0)"
    assert first_tikz.tikz_file.read_text() == first_environment.read_text()

    # Second environment
    second_tikz = TikzPicture()
    second_tikz.ellipse((2, 2), 4, 2, options="fill, Green!20")
    second_tikz.write()
    second_environment = code_dir / "second_environment.tex"

    assert second_tikz._id == "@TikzPy__#id__==__(1)"
    assert second_tikz.tikz_file.read_text() == second_environment.read_text()

    # Third environment
    third_tikz = TikzPicture()
    third_tikz.line((4, 4), (4, 0), options="<->, thick, dashed")
    third_tikz.write()
    third_environment = code_dir / "third_environment.tex"

    assert third_tikz._id == "@TikzPy__#id__==__(2)"
    assert third_tikz.tikz_file.read_text() == third_environment.read_text()


def test_updating_multiple_environments():
    """Test that we can independently update multiple tikz environments created in one process."""
    clear_test_code()
    code_dir = Path("test_code_update") / "test_updating_multiple_environments"

    # First environment
    first_tikz = TikzPicture()
    circle = first_tikz.circle((0, 0), 3, options="thin, fill=orange!15")
    first_tikz.write()

    # Second environment
    second_tikz = TikzPicture()
    ellipse = second_tikz.ellipse((2, 2), 4, 2, options="fill, Green!20")
    second_tikz.write()

    # Third environment
    third_tikz = TikzPicture()
    line = third_tikz.line((4, 4), (4, 0), options="<->, thick, dashed")
    third_tikz.write()

    # Now compile everything
    original = code_dir / "original.tex"
    assert third_tikz.tikz_file.read_text() == original.read_text()

    # Test updating second environment
    ellipse.y_axis = 5
    ellipse.options += ", dashed"
    second_tikz.rectangle((0, 0), (1, 1))
    second_tikz.write()
    first_update = code_dir / "first_update.tex"
    assert second_tikz.tikz_file.read_text() == first_update.read_text()

    # Test updating third environment
    line.end = (0, 4)
    line.options = ", ->, dashed"
    third_tikz.arc((0, 0), start_angle=45, end_angle=90, radius=2)
    third_tikz.write()
    second_update = code_dir / "second_update.tex"
    assert third_tikz.tikz_file.read_text() == second_update.read_text()

    # Test updating first environment
    circle.radius = 1
    first_tikz.line((2, 2), (5, 5))
    first_tikz.write()
    third_update = code_dir / "third_update.tex"
    assert first_tikz.tikz_file.read_text() == third_update.read_text()
