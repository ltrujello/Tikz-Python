import shutil
import re
import tempfile
from pathlib import Path
from tikzpy import TikzPicture
from tikzpy.utils.helpers import true_posix_path


def test_pdf_creation():
    """Test that the pdf file is generated as tikz_code/tex_file.pdf."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tikz = TikzPicture(tikz_code_dir=tmp_dir)
        # Line
        tikz.line(
            (0, 0),
            (1, 1),
            options="thick, blue",
            control_pts=[(0.25, 0.25), (0.75, 0.75)],
        )
        tikz.write()
        pdf_location = tikz.compile()
        correct_pdf_file = Path(tmp_dir, "tex_file.pdf")
        assert correct_pdf_file.exists()
        assert pdf_location.resolve() == correct_pdf_file.resolve()


def test_tikz_file_creation():
    """Test that the tikz code file is generated as tikz_code/tikz_code.tex."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tikz = TikzPicture(tikz_code_dir=tmp_dir)
        tikz.circle((1, 1), 7)
        tikz.write()
        correct_tikz_file = Path(tmp_dir, "tikz_code.tex")
        assert correct_tikz_file.exists()


def test_tex_file_creation():
    """Test that the tex file is generated as tikz_code/tex/tex_file directory"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tikz = TikzPicture(tikz_code_dir=tmp_dir)
        tikz.arc((1, 1), 90, 180, 3)
        tikz.write_tex_file("tex_file.tex")
        correct_tex_file = Path(tmp_dir, "tex_file.tex")
        assert correct_tex_file.exists()