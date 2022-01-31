from flask_sqlalchemy import SQLAlchemy


database = SQLAlchemy()


def initialize_database(application):
    # Initializes the database
    database.init_app(application)

    with application.app_context():
        # Creates the tables if the database doesn't already exist
        database.create_all()
