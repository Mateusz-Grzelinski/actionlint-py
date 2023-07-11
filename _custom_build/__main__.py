import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", "-v", action="store_true")
    args = parser.parse_args()
    if args.version:
        from . import VERSION

        print(VERSION)


if __name__ == "__main__":
    main()
