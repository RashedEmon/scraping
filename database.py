from peewee import *

# db = MySQLDatabase('scraping', user='Rashedul', password='R@shedu1',
#                    host='localhost', port=3306)

db = MySQLDatabase('mysql', user='mysql', password='mysql',
                         host='127.0.0.1', port=3306)

class BaseModel(Model):
    class Meta:
        database = db


class Hotel(BaseModel):
    hotel_id = CharField(primary_key=True, max_length=50)
    name = CharField(max_length=200)


class Label(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, unique=True)


class Images(BaseModel):
    hotel = ForeignKeyField(Hotel)
    image = CharField(max_length=200, unique=True)
    label = ForeignKeyField(Label)



