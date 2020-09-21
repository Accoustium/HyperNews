from django.views import View
from django.contrib.auth import PermissionDenied
from django.shortcuts import render, redirect
from hypernews.settings import NEWS_JSON_PATH
from .forms import NewsForm
import random
import json
import datetime


# Global News Data in JSON
NEWS_JSON_DATA = json.load(open(NEWS_JSON_PATH, 'r'))


# Creation of News Articles by date
def articles_by_date(articles=NEWS_JSON_DATA):
    news_dict = {}
    for article in articles:
        date_ = datetime.datetime.strptime(article["created"], "%Y-%m-%d %H:%M:%S")
        if date_.strftime("%Y-%m-%d") not in news_dict.keys():
            news_dict[date_.strftime("%Y-%m-%d")] = []
        news_dict[date_.strftime("%Y-%m-%d")].append(article)

    news_dict = dict(
        sorted(
            news_dict.items(),
            key=lambda item: datetime.datetime.strptime(item[0], "%Y-%m-%d"),
            reverse=True
        )
    )
    for key, val in news_dict.items():
        val = sorted(
            val,
            key=lambda item: datetime.datetime.strptime(item['created'], "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )
        news_dict[key] = val

    return news_dict


# Create your views here.
class NewsHomeView(View):
    template_page = "news_home.html"

    def get(self, request, q=None, *args, **kwargs):
        if len(request.GET) > 0:
            return render(
                request,
                self.template_page,
                context={'news_articles': articles_by_date(
                    list(
                        filter(
                            lambda item: request.GET['q'] in item['title'],
                            NEWS_JSON_DATA
                        )
                    )
                )}
            )
        else:
            return render(request, self.template_page, context={'news_articles': articles_by_date()})


class NewsArticleView(View):
    template_page = "news_article.html"

    def get(self, request, link_, *args, **kwargs):
        news_data = None
        for article in NEWS_JSON_DATA:
            if article['link'] == link_:
                news_data = article
                break

        return render(request, self.template_page, context={'article': news_data})


class CreateNewsArticleView(View):
    template_page = "create_news.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_page, context={'form': NewsForm})

    def post(self, request, *args, **kwargs):
        form_class = NewsForm(request.POST)
        link = None
        if form_class.is_valid():
            while True:
                link = int(random.random() * 100000)
                if not list(filter(lambda item: item['link'] == link, NEWS_JSON_DATA)):
                    break

            created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            NEWS_JSON_DATA.append(
                {
                    "created": created,
                    "link": link,
                    "text": form_class.cleaned_data['text'],
                    "title": form_class.cleaned_data['title']
                }
            )

        return redirect('index')
