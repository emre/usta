
import argparse
import json
import os
import os.path
import itertools


from flask import Flask, request
from werkzeug import secure_filename


def get_app(usta_config):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = usta_config.get("MAX_UPLOAD_LIMIT")
    app.config['UPLOAD_FOLDER'] = usta_config["UPLOAD_FOLDER"]

    return app


def get_config(filename):

    if not filename:
        filename = os.path.expanduser("~/.usta.config")

    if not os.path.exists(filename):
        raise LookupError("config file doesn't exists. {}".format(filename))

    with open(filename) as file_handle:
        config_data = json.loads(file_handle.read())

    return config_data


def main():

    parser = argparse.ArgumentParser(
        epilog='usta is a simple file server for personal use.'
    )

    parser.add_argument("-c", "--config", help="config file")
    args = parser.parse_args()

    config = get_config(args.config)

    app = get_app(config)

    def allowed_file(filename):
        allowed_extensions = config.get("ALLOWED_EXTENSIONS")
        if allowed_extensions:
            return '.' in filename and \
                   filename.rsplit('.', 1)[1] in allowed_extensions

        # suppose all file formats are okay to upload
        # if the config doesn't have a ALLOWED_EXTENSIONS section.
        return True

    def get_available_filename(filename):
        dir_name, file_name = os.path.split(filename)
        file_root, file_ext = os.path.splitext(filename)

        # if the filename already exists, add an underscore and a number (before
        # the file extension, if one exists) to the filename until the generated
        # filename doesn't exist.
        counter = itertools.count(1)
        while os.path.exists(filename):
            counter_state = next(counter)
            if counter_state > 10:
                raise ValueError("counter limit exceeded for this filename. try renaming it.")
            filename = os.path.join(dir_name, "%s_%s%s" % (file_root, counter_state, file_ext))

        return filename

    @app.route('/upload', methods=['POST'])
    def upload():
        _file = request.files.get("file")
        if not _file:
            return "a file named as 'file' required", 400

        if not allowed_file(_file.filename):
            return "invalid file type", 400

        filename = secure_filename(_file.filename)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if os.path.exists(full_filename):

            try:
                full_filename = get_available_filename(full_filename)
            except ValueError as error:
                return error.message, 400

        print "saving to {}".format(full_filename)
        _file.save(full_filename)

        return '', 201

    app.debug = True
    app.run(
        config.get("HOST"),
        int(config.get("PORT")),
    )


if __name__ == '__main__':
    main()
