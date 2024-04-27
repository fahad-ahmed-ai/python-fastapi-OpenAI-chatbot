from mongoengine import Document, StringField


class Chat(Document):
    session_id = StringField(required=True, unique=False)
    question = StringField()
    answer = StringField()
    refined_query = StringField()