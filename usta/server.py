
import os
import os.path

from flask import Flask, request
from werkzeug import secure_filename
from clint.textui import puts, indent, colored
from gevent.wsgi import WSGIServer

from utils import (get_config, get_cli_arguments, check_auth, allowed_file, get_available_filename, get_config_filename)


def get_app(usta_config):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = usta_config.get("MAX_UPLOAD_LIMIT")
    app.config['UPLOAD_FOLDER'] = usta_config["UPLOAD_FOLDER"]

    return app


def main():

    args = get_cli_arguments()
    config = get_config(args.config)
    app = get_app(config)


    @app.route('/upload/', methods=['POST'])
    def upload():

        if 'client' in config and 'user' in config["client"] and 'pass' in config["client"]:
            auth_control = check_auth(config)
            if auth_control:
                return auth_control

        _file = request.files.get("file")
        if not _file:
            return "a file named as 'file' required", 400

        if not allowed_file(_file.filename, config):
            return "invalid file type", 400

        filename = secure_filename(_file.filename)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            full_filename = get_available_filename(full_filename)
        except ValueError as error:
            return error.message, 400

        _file.save(full_filename)

        return os.path.split(full_filename)[1], 201

    app.debug = True

    with indent(2):
        puts("{} starting at {}:{}".format(colored.magenta("server"), config.get("HOST"), config.get("PORT")))
        puts("{} {}".format(colored.green("config"), get_config_filename(args.config)))

    http_server = WSGIServer(('', int(config.get("PORT"))), app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
