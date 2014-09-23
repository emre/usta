

import os.path
import sys

import requests

from utils import get_config, get_cli_arguments


def main():
    args = get_cli_arguments(for_client=True)
    config = get_config(args.config)

    if not os.path.exists(args.file):
        sys.exit("error: file doesn't exists: {}".format(args.file))

    if not 'client' in config:
        sys.exit("error: client section is empty on your config file.")

    request_parameters = {}

    if 'username' in config.get("client") and 'password' in config.get("client"):
        request_parameters.update({
            "auth": (config["client"]["username"], config["client"]["password"]),
        })

    with open(args.file, 'r') as payload:
        request_parameters.update({
            "files": {"file": payload},
        })

        r = requests.post(config["client"]["endpoint"], **request_parameters)

        print r.status_code


if __name__ == '__main__':
    main()

