from flask import Flask, request
import json, time


application = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# database = SQLAlchemy(app)


# class Word(database.Model):
#     id = database.Column(database.Integer, primary_key=True)
#     english = database.Column(database.String(80), unique=False, nullable=False)
#     pinyin = database.Column(database.String(80), unique=False, nullable=False)
#     han_zi = database.Column(database.String(80), unique=False, nullable=False)


@application.route("/", methods=["GET"])
def home_page():
    data_set = {"Page": "Home", "Message": "Successfully loaded the Home page", "Timestamp": time.time()}
    json_dump = json.dumps(data_set)

    return json_dump


@application.route("/user/", methods=["GET"])
def request_page():
    user_query = str(request.args.get("user"))

    data_set = {"Page": "Request", "Message": f"Successfully got the request for {user_query}", "Timestamp": time.time()}
    json_dump = json.dumps(data_set)

    return json_dump


if __name__ == "__main__":
    # database.create_all()
    application.run(port=7770)
