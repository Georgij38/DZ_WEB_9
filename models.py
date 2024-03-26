from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

from pymongo.mongo_client import MongoClient

connect(
    db='DZ_8',
    host="mongodb+srv://user:567234@cluster0.qpllrc8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",  # наприклад, 'mongodb+srv://<username>:<password>@your_cluster_url/your_database_name?retryWrites=true&w=majority'
    username='user',
    password='567234',
    authentication_source='admin'  # аутентифікація в адміністративній базі даних
)

uri = "mongodb+srv://user:567234@cluster0.qpllrc8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)




class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=40))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)