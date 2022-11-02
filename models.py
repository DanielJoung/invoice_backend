from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase("Company.sqlite")

class Company(Model):
  companyName: CharField(unique=True)
  email: CharField(unique=True)
  password: CharField()
  address: CharField(unique=True)
  companyPhone: CharField(unique=True)

  class Meta:
    database=DATABASE


class User(Model):
  userName: CharField(unique=True)
  email: CharField(unique=True)
  password: CharField()
  company: ForeignKeyField(Company, backref="user")

  class Meta:
    database=DATABASE


class Store(Model):
  storeName: CharField(unique=True)
  address: CharField()
  storePhone: CharField(unique=True)
  company: ForeignKeyField(Company, backref="stores")

  class Meta:
    database=DATABASE


class Product(Model):
  productName: CharField()
  price: DecimalField()
  quantity: CharField()
  discount: CharField()
  company: ForeignKeyField(Company,backref="products")

  class Meta:
    database=DATABASE


def initialize():
  DATABASE.connect()
  DATABASE.create_tables([Company,Product,User,Store], safe=True)
  print("Connected to the DB")
  DATABASE.close()