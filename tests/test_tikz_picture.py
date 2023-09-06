import tempfile

from pathlib import Path
from tikzpy import TikzPicture


def test_tikz_picture_write_tex_file():
    filename = "foobar.tex"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        tikz = TikzPicture(tikz_code_dir=tmp_dir)
        tex_file_path = tmp_dir_path / filename
        tikz.write_tex_file(str(tex_file_path))
        assert tex_file_path.exists()
