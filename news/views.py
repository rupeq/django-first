from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from hypernews.settings import NEWS_JSON_PATH
from datetime import datetime
from random import randint
import json


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")


class NewsView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(NEWS_JSON_PATH, "r") as news_json:
            self.news = json.load(news_json)
            self.dates = {}
            for item in self.news:
                date = datetime.strptime(item["created"], "%Y-%m-%d %H:%M:%S").date()
                if date in self.dates:
                    self.dates[date].append(item)
                else:
                    self.dates[date] = [item]
            self.sorted_dates = sorted(self.dates.items(), reverse=True)

    def get(self, request, item_id=1, *args, **kwargs):
        return render(request, "news/item.html", context={"item": self.get_item(item_id)})

    def get_item(self, item_id):
        for item in self.news:
            if item["link"] == item_id:
                return item
        return {"title": "Empty"}


class MainView(NewsView):
    def get(self, request, item_id=1, *args, **kwargs):
        pages = self.sorted_dates
        q = request.GET.get('q')
        spot = request.GET.get('spot')
        if not spot:
            spot = "title"
        if q:
            query_result = {}
            for day in pages:
                for item in day[1]:
                    if q in item[spot]:
                        if day[0] in query_result:
                            query_result[day[0]].append(item)
                        else:
                            query_result[day[0]] = [item]
            pages = sorted(query_result.items(), reverse=True)
        return render(request, "main/main.html", context={"dates": pages})


class CreateView(NewsView):
    def get(self, request, *args, **kwargs):
        return render(request, "create/create.html")

    def post(self, request, *args, **kwargs):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = request.POST.get('title')
        text = request.POST.get('text')
        link = randint(1000, 9999)
        new_item = {"created": date, "text": text, "title": title, "link": link}
        self.news.append(new_item)
        with open(NEWS_JSON_PATH, "w") as news_json:
            json.dump(self.news, news_json)
        return redirect('../')
