from peewee import *
# import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase("company.sqlite")

class Company(UserMixin,Model):
  companyname= CharField(unique=True)
  email= CharField(unique=True)
  password= CharField()
  address= CharField(unique=True)
  companyphone= CharField(unique=True)

  class Meta:
    database=DATABASE

class User(UserMixin,Model):
  username= CharField(unique=True)
  email= CharField(unique=True)
  password= CharField()
  company= ForeignKeyField(Company, backref="user")

  class Meta:
    database=DATABASE


class Store(Model):
  storename= CharField(unique=True)
  address= CharField()
  storePhone= CharField(unique=True)
  company= ForeignKeyField(Company, backref="stores")

  class Meta:
    database=DATABASE


class Product(Model):
  productname= CharField()
  price= IntegerField(default=0)
  quantity= IntegerField(default=0)
  discount= IntegerField(default=0)
  company= ForeignKeyField(Company,backref="products")

  class Meta:
    database=DATABASE


def initialize():
  DATABASE.connect()
  DATABASE.create_tables([Company,Product,User,Store], safe=True)
  print("Connected to the DB")
  DATABASE.close()