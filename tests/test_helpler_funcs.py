import pytest
from tikzpy.utils.helpers import brackets, replace_code, extract_error_content


@pytest.fixture
def mock_latex_error_msg():
    return """\
! Package pgfkeys Error: I do not know the key '/tikz/dashed meow' and I am goi
ng to ignore it. Perhaps you misspelled it.

See the pgfkeys package documentation for explanation.
Type  H <return>  for immediate help.
 ...

l.28     \draw[dashed meow]
                            (3, 0) arc [start angle = 0.0, end angle = 179.9...

?
"""


def test_brackets():
    """Test the brackets function to correctly surround nonempty text with brackets."""
    string = "This is \nnot empty"
    empty_string = ""
    assert brackets(string) == "[This is \nnot empty]"
    assert brackets(empty_string) == ""


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


def test_extract_error_content(mock_latex_error_msg):
    new_mock_latex_error_msg = mock_latex_error_msg + "\nFoo Bar"
    lines = new_mock_latex_error_msg.splitlines(keepends=True)
    assert mock_latex_error_msg == extract_error_content(lines)


def test_extract_error_content_no_question_mark(mock_latex_error_msg):
    new_mock_latex_error_msg = mock_latex_error_msg + "\nFoo bar"
    new_mock_latex_error_msg = new_mock_latex_error_msg.replace("?", "")
    lines = new_mock_latex_error_msg.splitlines(keepends=True)
    assert new_mock_latex_error_msg == extract_error_content(lines)


def test_extract_error_content_no_error_lines(mock_latex_error_msg):
    mock_latex_error_msg = mock_latex_error_msg.replace("!", "")
    lines = mock_latex_error_msg.splitlines(keepends=True)
    assert extract_error_content(lines) is None
