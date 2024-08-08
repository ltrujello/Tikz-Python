import re
import math
from typing import Tuple
from pathlib import Path, WindowsPath


def brackets(string: str) -> str:
    """Wraps a string with a pair of matching brackets."""
    if len(string) != 0:
        return "[" + string + "]"
    else:
        return ""


def true_posix_path(path_obj: Path) -> str:
    r"""Given a path_obj, we return a string which represents the "true posix" file path
    of the path_obj.

    Long: We need to tell TeX where our tikz_code is. Because TeX's "\input" command expects posix-like paths,
    regardless of the machine it is running, we need things like "/Users/user/Desktop..." and not "C:\Users\user\Desktop..."
    We'd naturally just do str(path_obj.resolve()), which works on linux. But this will cause an error on windows machines
    since such a command returns something like "C:\Users\user\Desktop..."
    Since pathlib does not happen to have a method for this, we write one.
    """
    full_path = path_obj.resolve()
    if isinstance(path_obj, WindowsPath):
        drive = full_path.drive  # C:, E:, etc.
        return "/" + str(
            full_path.relative_to(f"{drive}/").as_posix()
        )  # Need / so we may obtain /Users/... not Users/...
    else:
        return str(full_path)


def replace_code(
    begin_delim: str, end_delim: str, content: str, new_code: str
) -> Tuple[str, int]:
    """Replaces text delimited by `begin_delim` and `end_delim` appearing in `content`, with `new_code`.
    Returns new string and number of matches made."""
    return re.subn(
        rf"{re.escape(begin_delim)}([\s\S]*?){re.escape(end_delim)}",
        new_code.replace(
            "\\", "\\\\"
        ),  # Need to escape backslashes twice for re package
        content,
    )


def find_image_start_boundary(img_data):
    ind = 0
    while ind < len(img_data):
        row = img_data[ind]
        found = False
        for col in row:
            if col < 255:
                found = True
                break
        if found:
            break
        ind += 1
    return ind


def find_image_end_boundary(img_data):
    ind = len(img_data) - 1
    while ind > 0:
        row = img_data[ind]
        found = False
        for col in row:
            if col < 255:
                found = True
                break
        if found:
            break
        ind -= 1
    return ind


def extract_error_content(log_lines: list[str]) -> str:
    """
    Scans the provided text for LaTeX error messages.

    This function searches the given text for lines that begin with "! " which
    typically indicates the start of an error message in LaTeX logs. It then
    continues to collect all subsequent lines until it encounters a line that
    begins with "? ", which usually indicates the end of the error message.
    All collected lines are appended to a list and returned.

    Parameters:
    text (str): The input text to scan for error messages.

    Returns:
    list: A list of strings containing the lines of the error message.
          If no error message is found, the list will be empty.
    """
    error_lines = []
    recording = False

    for line in log_lines:
        if line.startswith("! "):
            recording = True
        if recording:
            error_lines.append(line)
            if line.startswith("?"):
                break

    if len(error_lines) == 0:
        return None

    return "".join(error_lines)
