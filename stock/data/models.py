from django.db.models import Model, TextField, CharField


class Stock(Model):
    name = CharField(max_length=20,default='')
    stockid = CharField(max_length=20,default='')
