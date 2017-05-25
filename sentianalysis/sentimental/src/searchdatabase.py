import collections
import dateutil.parser as parser

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, Context
from numpy import mean
from sentimental.database import CSVtoMongoDB
from sentimental.models import brandnameReviews, genericnameReviews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


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

def conditionScoreforBrands(condition_name, flag):

    brandPos = list()
    brandNeg = list()
    brandNeu = list()
    brandDate = list()
    brandDrugName = list()

    brands_data = brandnameReviews.objects(condition=condition_name)
    analyzer = SentimentIntensityAnalyzer()

    for data in brands_data:
        brandDrugName.append(data.name)
        score = analyzer.polarity_scores(data.review)
        brandDate.append(parser.parse(data.date).year)
        for keys, values in score.items():
            if keys == 'pos':
                brandPos.append(values)
            if keys == 'neg':
                brandNeg.append(values)
            if keys == 'neu':
                brandNeu.append(values)
    if flag == 'true':
        return brandPos, brandNeg, brandNeu, brandDate, brandDrugName
    else:
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
