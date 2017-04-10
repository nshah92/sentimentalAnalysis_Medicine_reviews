from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext


from database import CSVtoMongoDB
from .models import brandnameReviews

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def index(request):
    context = {'all_albums': ''}
   # CSVtoMongoDB();
    return render(request, 'sentimental/index.html', context)


def search(request):
    if 'medicinename' in request.GET:
        message = request.GET['medicinename']
    else:
        message = 'You submitted nothing!'

    posts = brandnameReviews.objects(name=message)

    sentences = "great"
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(sentences)
    return render_to_response('sentimental/search.html', {'Posts': posts})

def searchData(medicine):
    result = list()
    for e in brandnameReviews.objects().all():
        if medicine.__eq__(e["name"]):
            result.append(e.name)
            brandnameReviews(e.name, e.genericname, e.review, e.date)
    return result