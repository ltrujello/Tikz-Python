import tempfile

from pathlib import Path
from tikzpy import TikzPicture


def test_tikz_picture_write_tex_file():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tikz = TikzPicture(tikz_code_dir=tmp_dir)
        tikz.write_tex_file()
        assert tikz.tex_file.exists()
        assert tikz.tex_file.resolve() == Path(tmp_dir) / "tex" / "tex_file.tex"
