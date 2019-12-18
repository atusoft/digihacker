import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from stock.data.models import *

s = Stock(name='test')
s.save()

first = Stock.objects.all()[0]

print(first.name)
