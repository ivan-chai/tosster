from .shuffle import shuffle_imports, shuffle_methods_classes
from .rename import corrupt_names


METHODS = {
    "shuffle_imports": shuffle_imports,
    "shuffle_methods_classes": shuffle_methods_classes,
    "corrupt_names": corrupt_names
}
