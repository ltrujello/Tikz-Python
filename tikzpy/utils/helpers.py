from pathlib import WindowsPath


def brackets(string):
    """A helper function for creating tikz code.
    Basically, if the string is empty, we don't obtain brackets [].
    """
    if len(string) != 0:
        return "[" + string + "]"
    else:
        return ""


def true_posix_path(path_obj):
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
        return str(full_path.relative_to(f"{drive}/").as_posix())
    else:
        # Must be PosixPath (We use Path, and pathlib automatically uses either WindowsPath or PosixPath)
        return str(full_path.resolve())
