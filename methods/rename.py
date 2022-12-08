import ast
import itertools
import logging
import random
import string
from abc import ABC, abstractmethod


class IdentifierVisitor(ABC, ast.NodeVisitor):
    def __init__(self, ignore_names=None):
        self._ignore_names = ignore_names or set()

    @abstractmethod
    def visit_identifier(self, name):
        pass

    def _visit(self, name):
        if name in self._ignore_names:
            return name
        new = self.visit_identifier(name)
        return name if new is None else new

    def generic_visit(self, node):
        if isinstance(node, ast.Attribute):
            # Don't visit attr.
            self.generic_visit(node.value)
            return
        if isinstance(node, ast.alias):
            if node.asname:
                node.asname = self._visit(node.asname)
            else:
                node.name = self._visit(node.name)
            return
        if isinstance(node, ast.keyword):
            # Don't visit arg.
            self.generic_visit(node.value)
            return
        super().generic_visit(node)
        for key in ["name", "id", "attr", "arg"]:
            if hasattr(node, key) and (getattr(node, key) is not None):
                setattr(node, key, self._visit(getattr(node, key)))
        if hasattr(node, "names"):
            for i in range(len(node.names)):
                if isinstance(node.names[i], ast.alias):
                    self.generic_visit(node.names[i])
                else:
                    node.names[i] = self._visit(node.names[i])


class NamesCollector(IdentifierVisitor):
    def __init__(self, ignore_names=None):
        super().__init__(ignore_names)
        self.names = set()

    def visit_identifier(self, name):
        if name.startswith("__"):
            return
        self.names.add(name)


class ImportNamesCollector(ast.NodeVisitor):
    def __init__(self):
        self.names = set()

    def visit_Import(self, node):
        for name in node.names:
            if name.asname:
                self.names.add(name.asname)
            else:
                self.names.add(name.name)

    def visit_ImportFrom(self, node):
        self.visit_Import(node)


class NamesMapper(IdentifierVisitor):
    def __init__(self, mapping):
        super().__init__()
        self.mapping = mapping

    def visit_identifier(self, name):
        return self.mapping.get(name, name)


def corrupt_name(name):
    if (len(name) > 1) and (random.random() < 0.3):
        # Truncate.
        index = random.randint(1, len(name) - 1)
        name = name[:index]
    elif random.random() < 0.3:
        # Insert underscore.
        index = random.randint(0, len(name))
        name = name[:index] + "_" + name[index:]
    elif random.random() < 0.3:
        # Append suffix.
        for _ in range(random.randint(1, 5)):
            name = name + random.choice(string.ascii_letters)
    elif random.random() < 0.3:
        name = name.upper()
    else:
        name = name.lower()
    return name


def corrupt_names(st, level=1.0):
    # Gen names from imports.
    collector = ImportNamesCollector()
    collector.visit(st)
    import_names = collector.names

    # Replace other names.
    collector = NamesCollector(import_names)
    collector.visit(st)
    seen_names = set()
    mapping = {}
    for name in collector.names:
        if random.random() < level:
            new_name = corrupt_name(name)
            while new_name in seen_names:
                new_name = new_name + random.choice(string.ascii_letters)
        else:
            new_name = name
        mapping[name] = new_name
        seen_names.add(new_name)
    logging.info(f"Name mapping: {mapping}")
    logging.info(f"Found {len(mapping)} names")
    NamesMapper(mapping).visit(st)
