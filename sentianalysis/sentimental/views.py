from django.shortcuts import render
from django.http import HttpResponse

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

        for e in brandnameReviews.objects().all():
            if message.__eq__(e["name"]):
                print e["name"];

        sentences = "great"
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(sentences)
    else:
        message = 'You submitted nothing!'

    return HttpResponse("{:-<65} {}".format("hello", str(message)))

def searchData(medicine):


    return medicine
