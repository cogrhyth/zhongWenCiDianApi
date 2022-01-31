from database.database import database


class Word(database.Model):

    __table_name__ = "word"
    word_identification = database.Column(database.Integer, primary_key=True)
    english = database.Column(database.String(64), unique=True)
    pinyin = database.Column(database.String(64), unique=True)
    plain_pinyin = database.Column(database.String(64), unique=False)
    han_zi = database.Column(database.String(64), unique=True)
    image = database.Column(database.Text, unique=True)
    mimetype = database.Column(database.Text)

    def __init__(self, english, pinyin, plain_pinyin, han_zi, image=None, mimetype=None):

        self.english = english
        self.pinyin = pinyin
        self.plain_pinyin = plain_pinyin
        self.han_zi = han_zi

        if image is not None and mimetype is not None:

            self.image = image
            self.mimetype = mimetype
