from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import NewsHomeView, NewsArticleView, CreateNewsArticleView


urlpatterns = [
    path('', NewsHomeView.as_view(), name="news_splash"),
    path('<int:link_>/', NewsArticleView.as_view(), name="single_article"),
    path('create/', CreateNewsArticleView.as_view(), name="create_news"),
]

urlpatterns += static(settings.STATIC_URL)
