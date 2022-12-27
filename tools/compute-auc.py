import argparse
import numpy as np
from sklearn.metrics import roc_auc_score


def parse_args():
    parser = argparse.ArgumentParser("""Compute ROC AUC of similarity predictor.""")
    parser.add_argument("scores", help="Path to the file with pairwise scores.")
    parser.add_argument("labels", help="Path to the file with pairwise labels.")
    return parser.parse_args()


def to_number(s):
    try:
        return int(s)
    except Exception:
        return float(s)


def read_mat(path):
    matrix = []
    with open(path) as fp:
        for line in fp:
            line = line.strip()
            matrix.append(list(map(to_number, line.split())))
    return np.array(matrix)


def main(args):
    predictions = read_mat(args.scores)
    labels = read_mat(args.labels)
    n = len(predictions)
    if (predictions.shape != (n, 1)) or (labels.shape != (n, 1)):
        raise ValueError("Input files format error.")
    auc = roc_auc_score(labels.squeeze(1), predictions.squeeze(1))
    print(max(auc, 1 - auc))


if __name__ == "__main__":
    main(parse_args())
