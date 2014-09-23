import json
import os.path
import argparse


def get_config(filename):

    if not filename:
        filename = os.path.expanduser("~/.usta.config")

    if not os.path.exists(filename):
        raise LookupError("config file doesn't exists. {}".format(filename))

    with open(filename) as file_handle:
        config_data = json.loads(file_handle.read())

    return config_data


def get_cli_arguments(for_client=False):

    parser = argparse.ArgumentParser(
        epilog='usta is a simple file server for personal use.'
    )

    parser.add_argument("-c", "--config", help="config file")
    if for_client:
        parser.add_argument("-f", "--file", help="file to upload", required=True)

    args = parser.parse_args()

    return args