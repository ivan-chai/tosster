import argparse
import ast
import logging
import random
import sys

from methods import METHODS


def parse_arguments():
    parser = argparse.ArgumentParser("Obfuscate Python code.")
    parser.add_argument("input", help="Path to the source code.")
    parser.add_argument("-o", "--output", help="Path to the output code. Print by default.")
    parser.add_argument("-m", "--methods", help="Coma-separated methods.")
    parser.add_argument("-s", "--seed", help="Random seed.", type=int)
    parser.add_argument("-l", "--level", help="Obfuscation level.", type=float, default=0.5)
    return parser.parse_args()


def main(args):
    logging.getLogger().setLevel(logging.INFO)
    if args.seed is not None:
        random.seed(args.seed)

    methods = METHODS
    if args.methods is not None:
        try:
            methods = {k: methods[k] for k in args.methods.split(",")}
        except KeyError:
            print("Available methods:", list(methods))
            raise

    with open(args.input) as fp:
        st = ast.parse(fp.read())

    for method in methods.values():
        method(st, level=args.level)

    result = ast.unparse(st)
    if args.output is None:
        print(result)
    else:
        with open(args.target, "w") as fp:
            print(result, file=fp)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
