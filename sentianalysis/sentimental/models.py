from __future__ import unicode_literals


# Create your models here.
from mongoengine import *

connect('medicinereview')

from django.db import models

class brandnameReviews(Document):
    name = StringField(max_length=50)
    genericname = StringField(max_length=50)
    review = StringField(max_length=5000)
    date = StringField(max_length=50)
    condition = StringField(max_length=50)

class genericnameReviews(Document):
    name = StringField(max_length=50)
    brandname = StringField(max_length=50)
    review = StringField(max_length=5000)
    date = StringField(max_length=50)
    condition = StringField(max_length=50)

class Employee(Document):
    name = StringField(max_length=50)