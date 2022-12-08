import ast
import random
import logging


def subset(l, indices):
    return [l[i] for i in indices]


def shuffle_subset(*lists, level=1.0):
    if len(lists) == 0:
        return
    n = len(lists[0])
    for l in lists:
        if len(l) != n:
            raise ValueError("Length mismatch")
    indices = list(range(n))
    random.shuffle(indices)
    indices = indices[:int(len(indices) * level)]
    return [subset(l, indices) for l in lists]


def shuffle_imports(st, level=1.0):
    indices = []
    nodes = []
    for i, node in enumerate(st.body):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            break
        indices.append(i)
        nodes.append(node)
    logging.info(f"Found {len(nodes)} imports at the beginning")
    indices, nodes = shuffle_subset(indices, nodes, level=level)
    random.shuffle(nodes)
    for i, node in zip(indices, nodes):
        st.body[i] = node


def shuffle_methods_classes(st, level=1.0):
    total = 0
    indices = []
    nodes = []
    for i, node in enumerate(st.body):
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, ast.ClassDef):
            total += shuffle_methods_classes(node)
        total += 1
        indices.append(i)
        nodes.append(node)
    indices, nodes = shuffle_subset(indices, nodes, level=level)
    random.shuffle(nodes)
    for i, node in zip(indices, nodes):
        st.body[i] = node
    if isinstance(st, ast.Module):
        logging.info(f"Found {total} functions and classes")
    return total
