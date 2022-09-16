from enum import unique
from unicodedata import name
from webbrowser import BaseBrowser
from peewee import *

db = MySQLDatabase('mysql', user='mysql', password='mysql',
                         host='127.0.0.1', port=3306)

db.connect()
print(db)
class BaseModel(Model):
    class Meta:
        database = db

class Hotel(BaseModel):
    id=AutoField(primary_key = True)
    name=CharField(max_length=200)

class Label(BaseModel):
    id=AutoField(primary_key = True)
    name=CharField(max_length=50,unique=True)

class Images(BaseModel):
    hotel= ForeignKeyField(Hotel)
    image=CharField(max_length=200,unique=True)
    label=ForeignKeyField(Label)

db.create_tables([Hotel, Label,Images])

res=Label.create(name="Bedroom")

print(res)