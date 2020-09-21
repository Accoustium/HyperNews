from django import forms
import datetime


class NewsForm(forms.Form):
    title = forms.CharField(max_length=150)
    text = forms.CharField(max_length=1024)
