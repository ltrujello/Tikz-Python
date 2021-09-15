import re
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
    full_path = path_obj
    if isinstance(path_obj, WindowsPath):
        drive = full_path.drive  # C:, E:, etc.
        return "/" + str(
            full_path.relative_to(f"{drive}/").as_posix()
        )  # Need / so we may obtain /Users/... not Users/...
    else:
        return str(full_path.resolve())


def replace_code(begin_delim, end_delim, content, new_code) -> tuple[str, int]:
    """Replaces text delimited by `begin_delim` and `end_delim` appearing in `content`, with `new_code`.
    Returns new string and number of matches made."""
    return re.subn(
        fr"{re.escape(begin_delim)}([\s\S]*?){re.escape(end_delim)}",
        new_code.replace(
            "\\", "\\\\"
        ),  # Need to escape backslashes twice for re package
        content,
    )
