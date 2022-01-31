from database.configuration import ALLOWED_EXTENSIONS, application
from flask import request, send_from_directory
from werkzeug.utils import secure_filename
import os


def is_allowed(file_name):
    return "." in file_name and file_name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route("/post_image", methods=["POST"])
def post_image():

    if request.method == "POST":

        if "image_file" not in request.files:
            return "A file was not uploaded", 400

        try:
            image = request.files["image_file"]

        except KeyError:
            return "A file was not uploaded, or something else went wrong", 400

        if image.filename == "":
            return "The file uploaded doesn't have a name", 400

        if image and is_allowed(image.filename):

            image_name = secure_filename(image.filename)
            image.save(os.path.join(application.config["UPLOAD_FOLDER"], image_name))
            return "The file was uploaded", 200


@application.route("/get_image/<path:image_name>", methods=["GET"])
def get_image(image_name):

    upload_folder = os.path.join(application.root_path, application.config["UPLOAD_FOLDER"])

    return send_from_directory(directory=upload_folder, path=image_name)
