from .docstrings import corrupt_docstrings
from .rename import corrupt_names
from .shuffle import shuffle_imports, shuffle_methods_classes


METHODS = {
    "shuffle_imports": shuffle_imports,
    "shuffle_methods_classes": shuffle_methods_classes,
    "corrupt_names": corrupt_names,
    "corrupt_docstrings": corrupt_docstrings
}
