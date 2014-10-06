import json
import os.path
import argparse
import itertools

from flask import request, Response


def get_config_filename(filename):

    if not filename:
        filename = os.path.expanduser("~/.usta.config")

    if not os.path.exists(filename):
        raise LookupError("config file doesn't exists. {}".format(filename))

    return filename


def get_config(filename):

    filename = get_config_filename(filename)

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


def authenticate():
    return Response(
        'you have to login with proper credentials.',
        401,
        {'WWW-Authenticate': 'Basic realm="login required"'}
    )


def allowed_file(filename, config):
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


def check_auth(config):
    auth = request.authorization
    if not auth or (auth.username != config["client"]["user"] or auth.password != config["client"]["pass"]):
        return authenticate()