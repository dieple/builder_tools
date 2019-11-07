import argparse
import os

from .templates import process_file


def main():
    parser = argparse.ArgumentParser(description="Retrieve Secrets form AWS Secret Manager")
    parser.add_argument("--folder", help="folder to parse", default=".")
    parser.add_argument(
        "--file", help="filename to look for ", default="values.yaml"
    )

    args = parser.parse_args()

    input_folder = args.folder
    input_file = args.file

    print("Looking for {} in {}".format(input_file, input_folder))
    # Find all files that match a pattern
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if input_file.casefold() == file.casefold():
                filepath = os.path.join(root, file)
                print("Processing file: {}...".format(filepath))
                secrets_replaced = process_file(filepath)
                if secrets_replaced > 0:
                    print("---> {} secrets replaced".format(secrets_replaced))
    print("Done!")
