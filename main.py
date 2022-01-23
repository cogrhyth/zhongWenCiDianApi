from flask import Flask, render_template, request
import json
import time

application = Flask(__name__)


@application.route("/words", methods=["POST"])
def add_word():

    if request.method == "POST":

        word = request.get_json()

        english = word["english"]
        pinyin = word["pinyin"]
        han_zi = word["hanzi"]

        dictionary = {"english": english, "pinyin": pinyin, "hanzi": han_zi}
        json_data = json.dumps(dictionary)

        return json_data


@application.route("/words", methods=["GET"])
def get_words():
    if request.method == "GET":
        data_set1 = {"Page": "Home", "Message": "Successfully loaded the Home page", "Timestamp": time.time()}
        data_set2 = {"Page": "Home", "Message": "Successfully loaded the Home page", "Timestamp": time.time()}
        data_set3 = {"Page": "Home", "Message": "Successfully loaded the Home page", "Timestamp": time.time()}
        data_sets = {"first": data_set1, "second": data_set2, "third": data_set3}
        json_data = json.dumps(data_sets)

        return json_data


if __name__ == "__main__":
    application.debug = True
    application.run(port=7777)
