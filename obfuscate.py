import argparse
import ast
import logging
import random
import sys

from methods import METHODS
from postprocess import PROCESSORS


def parse_arguments():
    parser = argparse.ArgumentParser("Obfuscate Python code.")
    parser.add_argument("input", help="Path to the source code.")
    parser.add_argument("-o", "--output", help="Path to the output code. Print by default.")
    parser.add_argument("-m", "--methods", help="Coma-separated methods.")
    parser.add_argument("-p", "--processors", help="Coma-separated post processors.")
    parser.add_argument("-s", "--seed", help="Random seed.", type=int)
    parser.add_argument("-l", "--level", help="Obfuscation level.", type=float, default=0.5)
    return parser.parse_args()


def apply(obj, collection, names=None):
    if names is not None:
        try:
            collection = {k: collection[k] for k in names.split(",")}
        except KeyError:
            print("Available methods:", list(collection))
            raise

    for method in collection.values():
        result = method(obj, level=args.level)
        if result is not None:
            obj = result
    return obj


def main(args):
    logging.getLogger().setLevel(logging.INFO)
    if args.seed is not None:
        random.seed(args.seed)

    with open(args.input) as fp:
        st = ast.parse(fp.read())

    apply(st, METHODS, args.methods)
    result = ast.unparse(st)
    result = apply(result, PROCESSORS, args.processors)

    if args.output is None:
        print(result)
    else:
        with open(args.target, "w") as fp:
            print(result, file=fp)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
