from database.configuration import ALLOWED_EXTENSIONS, application
from database.database import initialize_database, database
from models.word import Word
from flask import request, send_from_directory
from werkzeug.utils import secure_filename
import json
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
            image.save(os.path.join(application.config["UPLOAD_FOLDER"], image_name))
            return "The file was uploaded", 200


@application.route("/get_image/<path:image_name>", methods=["GET"])
def get_image(image_name):

    upload_folder = os.path.join(application.root_path, application.config["UPLOAD_FOLDER"])

    return send_from_directory(directory=upload_folder, path=image_name)


def initialize_word(new_word):

    database.session.add(new_word)
    database.session.commit()

    data = {"english": new_word.english, "pinyin": new_word.pinyin, "plainPinyin": new_word.plain_pinyin,
            "hanzi": new_word.han_zi, "image": new_word.image, "mimetype": new_word.mimetype}

    json_data = json.dumps(data)
    return json_data, 200


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


@application.route("/words", methods=["POST", "GET", "DELETE"])
def manipulate_dictionary():

    if request.method == "POST":

        form = request.form

        try:

            english = form["english"]
            pinyin = form["pinyin"]
            plain_pinyin = form["plain_pinyin"]
            han_zi = form["hanzi"]
            image = request.files["image"].read()
            mimetype = request.files["image"].mimetype

            if not_exist(english):

                new_word = Word(english, pinyin, plain_pinyin, han_zi, image, mimetype)
                return initialize_word(new_word)

            else:

                return {"message": f"the word '{english}' already exists in the database"}, 409

        except KeyError:

            return insert_word(form)

    elif request.method == "GET":

        words = Word.query.all()
        words_list = []

        for word in words:

            word_id = word.word_identification
            english = word.english
            pinyin = word.pinyin
            plain_pinyin = word.plain_pinyin
            han_zi = word.han_zi

            word_dict = {
                "wordIdentification": word_id, "english": english, "pinyin": pinyin,
                "plainPinyin": plain_pinyin, "hanZi": han_zi
            }
            json_word = json.dumps(word_dict)

            words_list.append(json_word)

        return str(words_list), 200

    elif request.method == "DELETE":

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
