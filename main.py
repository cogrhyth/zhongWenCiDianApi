from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json
import time

application = Flask(__name__)
environment = "production"

if environment == "development":
    application.debug = True
    application.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:7770/words"
elif environment == "production":
    application.debug = False
    user = "gqdfcvzoebasyw"
    password = "dc05314f8526ebf29d5974070e85dad77e1745651a6b9473f84f16dd74e324f3"
    dns = "ec2-54-216-17-9.eu-west-1.compute.amazonaws.com:5432"
    database = "d6kr4k8ud0v7c7"
    application.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{user}:{password}@{dns}/{database}"

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
def manipulate_dictionary():

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

        word = Word.query.filter_by(english="Hello").first()

        word = json.dumps({"word": word})

        return word, 200


if __name__ == "__main__":
    application.run(port=7777)
