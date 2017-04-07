from __future__ import unicode_literals

from django.db import models

# Create your models here.
from mongoengine import *

connect('medicinereview')


class Employee(Document):
    name = StringField(max_length=50)
    age = IntField(required=False)


class brandnameReviews(Document):
    name = StringField(max_length=50)
    genericname = StringField(max_length=50)
    review = StringField(max_length=5000)
    date = StringField(max_length=50)


class genericnameReviews(Document):
    name = StringField(max_length=50)
    brandname = StringField(max_length=50)
    review = StringField(max_length=5000)
    date = StringField(max_length=50)