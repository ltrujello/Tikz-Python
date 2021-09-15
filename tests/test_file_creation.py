import shutil
import re
from pathlib import Path
from tikzpy import TikzPicture
from tikzpy.utils.helpers import true_posix_path


def clear_test_code():
    """Reset the tikzpy picture count and clear the tikz_code directory."""
    TikzPicture.NUM_TIKZS = 0
    tikz_code_dir = Path("tikz_code")
    if tikz_code_dir.exists():
        shutil.rmtree(tikz_code_dir)


def test_pdf_creation():
    """Test that the pdf file is generated as tikz_code/tex_file.pdf."""
    clear_test_code()
    tikz = TikzPicture()
    # Line
    tikz.line(
        (0, 0),
        (1, 1),
        options="thick, blue",
        control_pts=[(0.25, 0.25), (0.75, 0.75)],
    )
    tikz.write()
    pdf_location = tikz.compile()
    assert Path("tikz_code/tex_file.pdf").exists()
    assert pdf_location.resolve() == Path("tikz_code/tex_file.pdf").resolve()
    clear_test_code()


def test_tikz_file_creation():
    """Test that the tikz code file is generated as tikz_code/tikz_code.tex."""
    clear_test_code()
    tikz = TikzPicture()
    tikz.circle((1, 1), 7)
    tikz.write()
    assert Path("tikz_code/tikz_code.tex").exists()
    assert tikz.tikz_file.resolve() == Path("tikz_code/tikz_code.tex").resolve()
    clear_test_code()


def test_tex_file_creation():
    """Test that the tex file is generated as tikz_code/tex/tex_file directory"""
    clear_test_code()
    tikz = TikzPicture()
    tikz.arc((1, 1), 90, 180, 3)
    tikz.write()
    tikz.compile()
    assert Path("tikz_code/tex/tex_file.tex").exists()
    assert tikz.tex_file.resolve() == Path("tikz_code/tex/tex_file.tex").resolve()
    clear_test_code()


def test_tikz_file_path():
    """Test that the \\input command in the tex file correctly points to the tikz file."""
    clear_test_code()
    tikz = TikzPicture()
    tikz.rectangle((0, 0), (4, 4), options="fill")
    tikz.write()
    tikz.compile()
    begin_delim = "\\input{"
    end_delim = "}"
    content = tikz.tex_file.read_text()
    match = re.search(
        fr"{re.escape(begin_delim)}([\s\S]*?){re.escape(end_delim)}", content
    )
    assert match.group(1) == true_posix_path(tikz.tikz_file)
    clear_test_code()
