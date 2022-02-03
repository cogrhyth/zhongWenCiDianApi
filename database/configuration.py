from flask import Flask


UPLOAD_FOLDER = "../resources"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

application = Flask(__name__)
environment = "production"

application.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
