
import os.path
import sys


import requests
import requests.auth

from utils import get_config, get_cli_arguments


def main():
    args = get_cli_arguments(for_client=True)
    config = get_config(args.config)

    if not os.path.exists(args.file):
        sys.exit("error: file doesn't exists: {}".format(args.file))

    if not 'client' in config:
        sys.exit("error: client section is empty on your config file.")

    request_parameters = {}

    if 'user' in config.get("client") and 'pass' in config.get("client"):
        request_parameters.update({
            "auth": requests.auth.HTTPBasicAuth(config["client"]["user"], config["client"]["pass"]),
        })

    with open(args.file, 'r') as payload:
        request_parameters.update({
            "files": {"file": payload},
        })
        try:
            r = requests.post(config["client"]["endpoint"], **request_parameters)
        except requests.exceptions.ConnectionError:
            # @todo: how exactly requests library seperate requests with bad auth and requests with bad url?
            sys.exit("invalid URL or invalid credentials.")

        if r.status_code == 201:
            print "file successfully uploaded. {}{}".format(config.get("SERVE_URL"), r.content)
        else:
            sys.exit("error: {}".format(r.content))

if __name__ == '__main__':
    main()

