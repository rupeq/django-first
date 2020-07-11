from django.db import models
from hypernews.settings import NEWS_JSON_PATH
from collections import OrderedDict
import json
# Create your models here.


# class News(models.Model):
#     created = models.DateField()
#     text = models.CharField(max_length=50)
#     title = models.CharField(max_length=50)
#     link = models.IntegerField(max_length=7, prim

with open(NEWS_JSON_PATH, 'r') as news_json:
    news = json.load(news_json)

sorted_by_date = OrderedDict()
for element in sorted(news, key=lambda k: k['created'], reverse=True):
    if not sorted_by_date.get(element["created"].split()[0]):
        sorted_by_date[element["created"].split()[0]] = []
    sorted_by_date[element["created"].split()[0]].append(element)
