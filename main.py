from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import time

application = Flask(__name__)
environment = "development"

if environment == "development":
    application.debug = True
    application.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:7770/words"
else:
    application.debug = False
    application.config["SQLALCHEMY_DATABASE_URI"] = ""

application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database = SQLAlchemy(application)


class Word(database.Model):
    __table_name__ = "word"
    word_identification = database.Column(database.Integer, primary_key=True)
    english = database.Column(database.String(64), unique=True)
    pinyin = database.Column(database.String(64), unique=True)
    han_zi = database.Column(database.String(64), unique=True)

    def __init__(self, english, pinyin, han_zi):
        self.english = english
        self.pinyin = pinyin
        self.han_zi = han_zi


@application.route("/words", methods=["POST", "GET"])
def word():

    if request.method == "POST":

        body = request.get_json()

        english = body["english"]
        pinyin = body["pinyin"]
        han_zi = body["hanzi"]

        if database.session.query(Word).filter(Word.english == english).count() == 0:
            new_word = Word(english, pinyin, han_zi)
            database.session.add(new_word)
            database.session.commit()

            json_data = json.dumps({"english": english, "pinyin": pinyin, "hanzi": han_zi})
            return json_data, 200
        else:
            return {"message": f"The word '{english}' already exists in the database"}, 409

    elif request.method == "GET":
        data_set1 = {"Page": "Home", "Message": "Successfully loaded the Home page", "Timestamp": time.time()}
        data_set2 = {"Page": "Home", "Message": "Successfully loaded the Home page", "Timestamp": time.time()}
        data_set3 = {"Page": "Home", "Message": "Successfully loaded the Home page", "Timestamp": time.time()}
        data_sets = {"first": data_set1, "second": data_set2, "third": data_set3}
        json_data = json.dumps(data_sets)

        return json_data, 200


if __name__ == "__main__":
    application.run(port=7777)
