import os.path


__all__ = ['rel', 'absolute_path']


rel = lambda p: os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', p)


def absolute_path(path):
    """
    :param path: absolute or relative path.
    :return: returns absolute path, validates that path leads to a folder.
    """
    absolute = rel(path)
    if os.path.isdir(absolute):
        return absolute
    assert os.path.isdir(path), "Folder does not exists."
    return path
