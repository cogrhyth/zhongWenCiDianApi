from database.configuration import ALLOWED_EXTENSIONS, application
from database.database import initialize_database, database
from models.word import Word
from os import listdir
from os.path import isfile, join
from flask import request, send_from_directory
from werkzeug.utils import secure_filename
import os

initialize_database(application)


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

            resources = os.path.join(application.root_path, application.config["UPLOAD_FOLDER"])

            image.save(os.path.join(resources, image_name))
            return "The file was uploaded", 200


@application.route("/get_image/<path:image_name>", methods=["GET"])
def get_image(image_name):

    upload_folder = os.path.join(application.root_path, application.config["UPLOAD_FOLDER"])

    return send_from_directory(directory=upload_folder, path=image_name)


@application.route("/get_resources", methods=["GET"])
def get_resources():

    resources = os.path.join(application.root_path, application.config["UPLOAD_FOLDER"])

    files = []

    for file in listdir(resources):

        if isfile:
            file = (join(resources, file))

        files.append({"file": file})

    return {"files": files}, 200


@application.route("/delete_image/<path:image_name>", methods=["DELETE"])
def delete_image(image_name):

    resources = os.path.join(application.root_path, application.config["UPLOAD_FOLDER"])

    os.remove(os.path.join(resources, image_name))

    return "The file was deleted", 200


def initialize_word(new_word):

    database.session.add(new_word)
    database.session.commit()

    data = {"english": new_word.english, "pinyin": new_word.pinyin, "plainPinyin": new_word.plain_pinyin,
            "hanzi": new_word.han_zi, "image": new_word.image, "mimetype": new_word.mimetype}

    return data, 200


def image_not_exist(image):

    return database.session.query(Word).filter(Word.image == image).count() == 0


def not_exist(english):

    return database.session.query(Word).filter(Word.english == english).count() == 0


def insert_word(form):

    english = form["english"]
    pinyin = form["pinyin"]
    plain_pinyin = form["plain_pinyin"]
    han_zi = form["hanzi"]

    if not_exist(english):

        new_word = Word(english, pinyin, plain_pinyin, han_zi)
        return initialize_word(new_word)

    else:

        return {"message": f"The word '{english}' already exists in the database"}, 409


def check_the_problem(word_is_unique, english, image):

    if not word_is_unique:

        return {"message": f"the word '{english}' already exists in the database"}, 409

    else:

        return {"message": f"the name '{image}' is not allowed"}, 409


@application.route("/words", methods=["POST"])
def post_word():

    if request.method == "POST":

        form = request.form
        image_file = request.files["image"]

        try:

            english = form["english"]
            pinyin = form["pinyin"]
            plain_pinyin = form["plain_pinyin"]
            han_zi = form["hanzi"]
            image = secure_filename(image_file.filename)
            mimetype = request.files["image"].mimetype

            word_is_unique = not_exist(english)

            if word_is_unique and is_allowed(image):

                resources = os.path.join(application.root_path, application.config["UPLOAD_FOLDER"])

                image_file.save(os.path.join(resources, image))

                new_word = Word(english, pinyin, plain_pinyin, han_zi, image, mimetype)
                return initialize_word(new_word)

            else:
                return check_the_problem(word_is_unique, english, image)

        except KeyError:
            return insert_word(form)


@application.route("/words", methods=["GET"])
def get_words():

    if request.method == "GET":

        words = Word.query.all()
        words_list = []

        for word in words:

            word_id = word.word_identification
            english = word.english
            pinyin = word.pinyin
            plain_pinyin = word.plain_pinyin
            han_zi = word.han_zi
            image = word.image
            mimetype = word.mimetype

            word_dict = {
                "wordIdentification": word_id, "english": english, "pinyin": pinyin,
                "plainPinyin": plain_pinyin, "hanZi": han_zi, "image": image, "mimetype": mimetype
            }

            words_list.append(word_dict)

        return {"dictionary": words_list}, 200


@application.route("/words/<word_id>", methods=["PUT"])
def update_word(word_id):

    if request.method == "PUT":

        body = request.get_json()

        english = body["english"]
        pinyin = body["pinyin"]
        plain_pinyin = body["plain_pinyin"]
        han_zi = body["hanzi"]

        queried_word = database.session.query(Word).filter(Word.word_identification == word_id).first()

        queried_word.english = english
        queried_word.pinyin = pinyin
        queried_word.plain_pinyin = plain_pinyin
        queried_word.han_zi = han_zi

        database.session.commit()

        data = {"english": english, "pinyin": pinyin, "plainPinyin": plain_pinyin,
                "hanzi": han_zi, "image": queried_word.image, "mimetype": queried_word.mimetype}

        return data, 200


@application.route("/words", methods=["DELETE"])
def delete_word():

    if request.method == "DELETE":

        body = request.get_json()

        english = body["english"]
        pinyin = body["pinyin"]
        plain_pinyin = body["plain_pinyin"]
        han_zi = body["hanzi"]

        requested_word = Word(english, pinyin, plain_pinyin, han_zi)

        queried_word = database.session.query(Word).filter(Word.english == requested_word.english).first()

        if queried_word is not None:

            database.session.delete(queried_word)
            database.session.commit()

            word_id = queried_word.word_identification
            english = queried_word.english
            pinyin = queried_word.pinyin
            plain_pinyin = queried_word.plain_pinyin
            han_zi = queried_word.han_zi
            existing_word = {
                "wordIdentification": word_id, "english": english, "pinyin": pinyin,
                "plainPinyin": plain_pinyin, "hanZi": han_zi
            }

            return existing_word, 200
        else:
            return {"message": f"The word '{english}' was not found in the database"}, 404


if __name__ == "__main__":
    application.run(port=7777)
