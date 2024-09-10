import os

from sql_transpiler_logic.util.exception_classes.exception_classes import EmptyDirectoryException


def fs_create_directory(__output_directory):
    """
    Create a directory if it does not exist.
    :param __output_directory: Directory path (absolute or relative).
    :return: None
    """

    if not __output_directory:
        raise EmptyDirectoryException("No output_directory is set!")
    elif not os.path.exists(__output_directory):
        os.makedirs(__output_directory)


def extract_directory(file_path: str):
    """
    Extracts the directory path from a full file path.
    :param file_path: Full file path.
    :return: Directory path.
    """
    if file_path is None: return None
    if file_path == "": return ""
    directory = os.path.dirname(file_path)
    return directory