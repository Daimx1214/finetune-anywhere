"""Resolve a model alias from the single model registry."""

import argparse

from common import model_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("alias", nargs="?")
    args = parser.parse_args()
    try:
        print(model_id(args.alias))
    except ValueError as exc:
        parser.error(str(exc))
