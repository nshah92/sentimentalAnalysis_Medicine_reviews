from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from database import CSVtoMongoDB
from .models import brandnameReviews, genericnameReviews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def index(request):
    context = {'all_albums': ''}
    # CSVtoMongoDB();
    return render(request, 'sentimental/index.html', context)

def graph(request):
    xdata = ["Positve", "Negetive", "Netural"]
    ydata = [52, 48, 160]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('sentimental/graph.html', data)


def search(request):
    if 'medicinename' in request.GET:
        message = request.GET['medicinename']
    else:
        message = 'You submitted nothing!'

    posts = brandnameReviews.objects(name=message)
    data = posts.explain()

    count = data.get("executionStats").get("nReturned")

    if count == 0:
        print "Data Not Avaliable"
        posts = genericnameReviews.objects(name=message)
        posts1 = brandnameReviews.objects(genericname=message)
        return render_to_response('sentimental/results.html', {'Posts': posts, 'Posts1': posts1})
    else:
        print "Data is Avaliable"
        posts1=genericnameReviews.objects(brandname=message)
        return render_to_response('sentimental/results.html', {'Posts': posts, 'Posts1': posts1})
    # sentences = "great"
    # analyzer = SentimentIntensityAnalyzer()
    # vs = analyzer.polarity_scores(sentences)
    # return render_to_response('sentimental/results.html', {'Posts': posts}, {'Posts1': posts1})

def searchData(medicine):
    result = list()
    for e in brandnameReviews.objects().all():
        if medicine.__eq__(e["name"]):
            result.append(e.name)
            brandnameReviews(e.name, e.genericname, e.review, e.date)
    return result
