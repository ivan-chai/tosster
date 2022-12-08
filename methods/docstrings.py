import ast
import random
import logging


def corrupt_string(s):
    for _ in range(random.randint(0, len(s))):
        index = random.randint(0, len(s))
        s = s[:index] + chr(random.randint(32, 1024)) + s[index:]
    return s


class DocStringVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        super().generic_visit(node)
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docstring = ast.get_docstring(node)
            if random.random() < 0.5:
                if docstring is not None:
                    # Remove docstring.
                    del node.body[0]
                    return
            if docstring is None:
                if random.random() < 0.5:
                    return
                # Insert docstring.
                node.body.insert(0, ast.Expr(ast.Constant("")))
                docstring = " " * random.randint(1, 20)
            docstring = corrupt_string(docstring)
            node.body[0].value.value = docstring


def corrupt_docstrings(st, level=1.0):
    DocStringVisitor().visit(st)
