import argparse
import os
import shutil
import random
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser("""Create pairs and labels.""")
    parser.add_argument("input_dirs", nargs="+", help="Directories with input files. Filse with the same name are considered similar.")
    parser.add_argument("--output-dir", help="Output directory with files and labels.", required=True)
    parser.add_argument("--seed", help="Random seed.", type=int, default=0)
    return parser.parse_args()


def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_path(root, base_name, variant):
    return os.path.join(root, "{}-{}.py".format(base_name, variant))


def main(args):
    random.seed(args.seed)
    by_name = defaultdict(list)
    for folder in args.input_dirs:
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            if not os.path.isfile(path):
                continue
            by_name[filename].append(path)
    by_name = list(by_name.items())
    output_files = os.path.join(args.output_dir, "files")
    mkdir(args.output_dir)
    mkdir(output_files)
    with open(os.path.join(args.output_dir, "pairs"), "w") as fp_pairs, \
         open(os.path.join(args.output_dir, "labels"), "w") as fp_labels:
        for i, (filename, paths) in enumerate(by_name):
            for j, path in enumerate(paths):
                shutil.copy(path, get_path(output_files, i, j))
                print(get_path("files", i, j), get_path("files", i, random.randint(0, len(paths) - 1)), file=fp_pairs)
                print(1, file=fp_labels)
            for _ in range(len(paths)):
                j = random.randint(0, len(by_name) - 2)
                if j == i:
                    j = len(by_name) - 1
                assert i != j
                print(get_path("files", i, random.randint(0, len(by_name[i][1]) - 1)),
                      get_path("files", j, random.randint(0, len(by_name[j][1]) - 1)),
                      file=fp_pairs)
                print(0, file=fp_labels)


if __name__ == "__main__":
    main(parse_args())
