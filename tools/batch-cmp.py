import argparse
import sys
import Levenshtein

def parse_args():
    parser = argparse.ArgumentParser("""Compare multiple documents via Levenshtein distance.
                                     Read pairs of files from stdin and write similarity score to stdout.""")
    parser.add_argument("-c", "--character", help="Compare by characters, not lines.", action="store_true")
    return parser.parse_args()


def read(path, lines=False):
    with open(path) as fp:
        result = fp.read()
    if lines:
        result = result.split("\n")
    return result


def main(args):
    for line in sys.stdin:
        path1, path2 = line.strip().split()
        file1, file2 = map(lambda path: read(path, lines=not args.character), (path1, path2))
        distance = Levenshtein.distance(file1, file2)
        distance /= max(len(file1), len(file2))
        print(max(1 - distance, 0))


if __name__ == "__main__":
    main(parse_args())
