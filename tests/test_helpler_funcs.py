from tikzpy.utils.helpers import brackets, replace_code


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
