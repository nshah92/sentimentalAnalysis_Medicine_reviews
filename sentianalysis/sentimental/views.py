'''
For Line chart
    x-axis -> date
    y-axis -> score

'''

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, Context
from numpy import mean
import collections


from database import CSVtoMongoDB
from .models import brandnameReviews, genericnameReviews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import dateutil.parser as parser

def index(request):
    context = {'all_albums': ''}
    # CSVtoMongoDB();
    return render(request, 'sentimental/index.html', context)

def getAverage(num, date):
    data = sorted(zip(date, num), key=lambda x: x[0])
    d = {}
    p1 = list()
    d1 = list()
    for tuple in data:
        key, val = tuple
        d.setdefault(key, []).append(val)

    od = collections.OrderedDict(sorted(d.items()))

    for key in od:
        p1.append(key)
        d1.append(mean(d[key]))
    return p1,d1

def graph(request):

    print "Generating charts....."
    extra_serie = {}

    if 'medicinename' in request.GET:
        message = request.GET['medicinename']
    else:
        message = 'You submitted nothing!'

    context = {
        'medicine': message
    }
    pos, neg, neu, Allscore, date, condition = search(message.lower())

    count = len(pos)
    if len(set(condition)) == 1:
        med_condition = set(condition).pop()

    print med_condition

    brandPos, brandNeg, brandNeu, brandDate = conditionScoreforBrands(med_condition)
    brand_count = len(brandPos)

    genericPos, genericNeg, genericNeu, genericDate = conditionScoreforGeneric(med_condition)
    generic_count = len(genericPos)

    #for postive graph
    d1, p1 = getAverage(pos,date)

    #for Negetive graph
    d2, p2 = getAverage(neg, date)

    # for netural graph
    d3, p3 = getAverage(neu, date)

    #for Brand drugs multiple line chart
    brandD1, brandP1 = getAverage(brandPos, brandDate)
    brandD2, brandP2 = getAverage(brandNeg, brandDate)
    brandD3, brandP3 = getAverage(brandNeu, brandDate)

    #for Generic drugs multiple line chart
    genericD1, genericP1 = getAverage(genericPos, genericDate)
    genericD2, genericP2 = getAverage(genericNeg, genericDate)
    genericD3, genericP3 = getAverage(genericNeu, genericDate)

    xdata = d1
    ydata = p1

    # xdata = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016,2017]
    # ydata =[0.095194029850746251, 0.087108695652173884, 0.069086092715231751, 0.082803370786516853, 0.11149504950495051, 0.10211428571428573, 0.093208955223880618, 0.12076315789473681, 0.057068965517241374,0.075627450980392141, 0.24700000000000003,]
    xdata1 = d2
    ydata1 = p2

    xdata2 = d3
    ydata2 = p3

    #med_positive
    chartdata = {
        'x': xdata,
        'name1': 'Positive', 'y1': ydata, 'extra1': extra_serie,
    }
    #med_negetive
    chartdata1 = {
        'x': xdata1,
        'name1': 'Negetive', 'y1': ydata1, 'extra1': extra_serie,
    }
    #med_netural
    chartdata2 = {
        'x': xdata2,
        'name1': 'Netural', 'y1': ydata2, 'extra1': extra_serie,
    }

    #condition_brand
    chartdata3 = {
        'x': brandD1,
        'name1': 'Positive', 'y1': brandP1, 'extra1': extra_serie,
        'name2': 'Negetive', 'y2': brandP2, 'extra2': extra_serie,
        'name3': 'Netural', 'y3': brandP3, 'extra3': extra_serie,
    }

    #condition_generic
    chartdata4 = {
        'x': genericD1,
        'name1': 'Positive', 'y1': genericP1, 'extra1': extra_serie,
        'name2': 'Negetive', 'y2': genericP2, 'extra2': extra_serie,
        'name3': 'Netural', 'y3': genericP3, 'extra3': extra_serie,
    }

    charttype = "lineChart"
    charttype1 = "lineChart"
    charttype2 = "lineChart"
    charttype3 = "lineChart"
    charttype4 = "lineChart"

    chartcontainer = 'linechart_container'
    chartcontainer1 = 'linechart_container1'
    chartcontainer2 = 'linechart_container2'
    chartcontainer3 = 'linechart_container3'
    chartcontainer4 = 'linechart_container4'

    data = {
        'condition': med_condition,
        'medicine': message.title(),
        'count': count,
        'brandCount': brand_count,
        'genericCount': generic_count,

        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,

        'charttype1': charttype1,
        'chartdata1': chartdata1,
        'chartcontainer1': chartcontainer1,

        'charttype2': charttype2,
        'chartdata2': chartdata2,
        'chartcontainer2': chartcontainer2,

        'charttype3': charttype3,
        'chartdata3': chartdata3,
        'chartcontainer3': chartcontainer3,

        'charttype4': charttype4,
        'chartdata4': chartdata4,
        'chartcontainer4': chartcontainer4,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
        'extra1': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
        'extra2': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
        'extra3': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
        'extra4': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('sentimental/graphs.html',data)

def search(message):
    # if 'medicinename' in request.GET:
    #     message = request.GET['medicinename']
    # else:
    #     message = 'You submitted nothing!'

    posts = brandnameReviews.objects(name=message)
    data = posts.explain()

    brandnameScore = list()
    bPos = list()
    bNeg = list()
    bNeu = list()
    bDate = list()
    bCondition = list()

    count = data.get("executionStats").get("nReturned")

    if count == 0:
        print "Data Not Avaliable"
        posts = genericnameReviews.objects(name=message)
        # posts1 = brandnameReviews.objects(genericname=message)
        # return render_to_response('sentimental/results.html', {'Posts': posts, 'Posts1': posts1})
        print len(posts)
        analyzer = SentimentIntensityAnalyzer()
        for post in posts:
            score = analyzer.polarity_scores(post.review)
            bDate.append(parser.parse(post.date).year)
            bCondition.append(post.condition)
            for keys, values in score.items():
                if keys == 'pos':
                    brandnameScore.append(values)
                    bPos.append(values)
                if keys == 'neg':
                    bNeg.append(values)
                    brandnameScore.append(values)
                if keys == 'neu':
                    bNeu.append(values)
                    brandnameScore.append(values)
        return bPos, bNeg, bNeu, brandnameScore, bDate, bCondition
    else:
        print "Data is Avaliable"
        posts1 = brandnameReviews.objects(name=message)
        # return render_to_response('sentimental/results.html', {'Posts': posts, 'Posts1': posts1})
        analyzer = SentimentIntensityAnalyzer()
        for post in posts1:
            score = analyzer.polarity_scores(post.review)
            bDate.append(parser.parse(post.date).year)
            bCondition.append(post.condition)
            for keys, values in score.items():
                if keys == 'pos':
                    brandnameScore.append(values)
                    bPos.append(values)
                if keys == 'neg':
                    bNeg.append(values)
                    brandnameScore.append(values)
                if keys == 'neu':
                    bNeu.append(values)
                    brandnameScore.append(values)
        return bPos, bNeg, bNeu, brandnameScore, bDate, bCondition
        # return render_to_response('sentimental/results.html', {'Posts': posts}, score)

def searchData(medicine):
    result = list()
    for e in brandnameReviews.objects().all():
        if medicine.__eq__(e["name"]):
            result.append(e.name)
            brandnameReviews(e.name, e.genericname, e.review, e.date)
    return result

def conditionScoreforBrands(condition_name):

    brandPos = list()
    brandNeg = list()
    brandNeu = list()
    brandDate = list()

    brands_data = brandnameReviews.objects(condition=condition_name)
    analyzer = SentimentIntensityAnalyzer()

    for data in brands_data:
        score = analyzer.polarity_scores(data.review)
        brandDate.append(parser.parse(data.date).year)
        for keys, values in score.items():
            if keys == 'pos':
                brandPos.append(values)
            if keys == 'neg':
                brandNeg.append(values)
            if keys == 'neu':
                brandNeu.append(values)
    return brandPos, brandNeg, brandNeu, brandDate

def conditionScoreforGeneric(condition_name):

    genericPos = list()
    genericNeg = list()
    genericNeu = list()
    genericDate = list()

    generic_data = genericnameReviews.objects(condition=condition_name)
    analyzer = SentimentIntensityAnalyzer()

    for data in generic_data:
        score = analyzer.polarity_scores(data.review)
        genericDate.append(parser.parse(data.date).year)
        for keys, values in score.items():
            if keys == 'pos':
                genericPos.append(values)
            if keys == 'neg':
                genericNeg.append(values)
            if keys == 'neu':
                genericNeu.append(values)
    return genericPos, genericNeg, genericNeu, genericDate

def drugdrtail(request):
    return render_to_response('sentimental/drugdetail.html')