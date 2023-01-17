import sys
import pickle
import os


def load_save():
    if not os.path.isfile('input.pk'):
        return None

    with open('input.pk', 'rb') as fi:
        input = pickle.load(fi)
    return input


def main(input):
    filename = 'input.pk'
    with open(filename, 'wb') as f:
        pickle.dump(input, f)
    print(f"{input} saved")


if __name__ == "__main__":
    main(sys.argv[1])
