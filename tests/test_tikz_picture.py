import tempfile
import pytest
import tikzpy

from pathlib import Path
from tikzpy import TikzPicture
from tikzpy.utils.types import CompileError
from unittest.mock import Mock


def completed_process_factory(returncode=0):
    return Mock(returncode=returncode)


def test_tikz_picture_write_tex_file():
    filename = "foobar.tex"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        tikz = TikzPicture(tikz_code_dir=tmp_dir)
        tex_file_path = tmp_dir_path / filename
        tikz.write_tex_file(str(tex_file_path))
        assert tex_file_path.exists()


def test_compile_smoke(mocker):
    # Spy on the subprocess call in the compile method
    spy = mocker.spy(
        tikzpy.tikz_environments.tikz_picture.subprocess,
        "run",
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        pdf_dest = Path(tmp_dir) / "pdf_file.pdf"
        tikz = TikzPicture()
        tikz.circle((0, 0), 3, options="thin, fill=orange!15")
        assert pdf_dest.resolve() == tikz.compile(pdf_dest)
        assert spy.spy_return.returncode == 0


def test_compile_error_no_log_file(mocker):
    # Mock the subprocess call to simulate failure
    mock_completed_process = mocker.patch(
        "tikzpy.tikz_environments.tikz_picture.subprocess.run",
        completed_process_factory(-1),
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tikz = TikzPicture()
        tikz.circle((0, 0), 3, options="thin, fill=orange!15")
        with pytest.raises(CompileError) as e:
            tikz.compile()
        assert "No log file found" in e.value.message


def test_compile_error_log_file_parsing_failed(mocker):
    # Mock the subprocess call to simulate failure
    mock_completed_process = mocker.patch(
        "tikzpy.tikz_environments.tikz_picture.subprocess.run",
        completed_process_factory(-1),
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tikz = TikzPicture()
        tikz.circle((0, 0), 3, options="thin, fill=orange!15")

        # Pretend the log file exists
        mocker.patch(
            "tikzpy.tikz_environments.tikz_picture.Path.exists",
            return_value=True,
        )
        # Make fake log file have no text
        mocker.patch(
            "tikzpy.tikz_environments.tikz_picture.Path.read_text",
            return_value="",
        )
        with pytest.raises(CompileError) as e:
            tikz.compile()
        assert "Failed to parse log file" in e.value.message


def test_compile_compile_error_log_file_parsing(mocker):
    # Spy on the subprocess call in the compile method
    spy = mocker.spy(
        tikzpy.tikz_environments.tikz_picture.subprocess,
        "run",
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        tikz = TikzPicture()
        tikz.circle((0, 0), 3, options="thin, fill=orange!15, meow")
        with pytest.raises(CompileError) as e:
            tikz.compile()
        assert (
            "! Package pgfkeys Error: I do not know the key '/tikz/meow'"
            in e.value.message
        )
        assert spy.spy_return.returncode != 0
