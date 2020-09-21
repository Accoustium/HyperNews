from django.views import View
from django.shortcuts import render, redirect


# Create your views here.
class LandingPageView(View):
    template_page = "landing_page.html"

    def get(self, request, *args, **kwargs):
        return redirect('news_splash')
