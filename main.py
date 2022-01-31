from database.configuration import application
from database.database import initialize_database
from routes.image import post_image, get_image
from routes.word import manipulate_dictionary

initialize_database(application)


if __name__ == "__main__":
    application.run(port=7777)
