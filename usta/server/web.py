
import argparse
import json
import os
from functools import wraps


from flask import Flask, Response, request


def get_app(usta_config):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = usta_config.get("MAX_UPLOAD_LIMIT")

    return app


def get_config(filename):

    if not os.path.exists(filename):
        raise LookupError("invalid filename for config. {}".format(filename))

    config_data = json.loads(open(filename).read())

    return config_data


def main():

    parser = argparse.ArgumentParser(
        epilog='usta is a simple file server for personal use.'
    )

    parser.add_argument("-c", "--config", help="config file", required=True)
    args = parser.parse_args()

    config = get_config(args.config)

    app = get_app(config)

    @app.route('/upload')
    def upload():
        return "there will be a upload handler here."

    app.run(
        config.get("HOST"),
        int(config.get("PORT")),
    )


if __name__ == '__main__':
    main()
