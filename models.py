from peewee import *
import datetime
from flask_login import UserMixin
import os
from playhouse.db_url import connect

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///company.sqlite')


class Company(UserMixin, Model):
    companyname = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    address = CharField(unique=True)
    companyphone = CharField(unique=True)

    class Meta:
        database = DATABASE


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    company = ForeignKeyField(Company, backref="user")

    class Meta:
        database = DATABASE


class Store(Model):
    storename = CharField()
    address = CharField()
    storephone = CharField(unique=True)
    company = ForeignKeyField(Company, backref="stores")
    class Meta:
        database = DATABASE


class Product(Model):
    productname = CharField(unique=True)
    price = IntegerField(default=0)
    quantity = IntegerField(default=0)
    discount = IntegerField(default=0)
    company = ForeignKeyField(Company, backref="products")

    class Meta:
        database = DATABASE

class Invoice(Model):
    user: ForeignKeyField(User, backref="invoices")
    balance = IntegerField()
    case = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database =DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Company, Product, User, Store, Invoice], safe=True)
    print("Connected to the DB")
    DATABASE.close()
