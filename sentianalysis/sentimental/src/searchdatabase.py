import collections
import itertools
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

    wordlist = list()

    allwords_pos = list()
    allwords_neg = list()
    allwords_neu = list()


    count = data.get("executionStats").get("nReturned")

    if count == 0:
        print "Generic Drug"
        posts = genericnameReviews.objects(name=message)
        # posts1 = brandnameReviews.objects(genericname=message)
        # return render_to_response('sentimental/results.html', {'Posts': posts, 'Posts1': posts1})
        print len(posts)
        analyzer = SentimentIntensityAnalyzer()
        for post in posts:
            score, wordlist = analyzer.polarity_scores(post.review)
            bDate.append(parser.parse(post.date).year)
            bCondition.append(post.condition)
            print score
            for keys, values in score.items():
                if keys == 'pos':
                    allwords_pos.append(wordlist[0])
                    brandnameScore.append(values)
                    bPos.append(values)
                if keys == 'neg':
                    allwords_neg.append(wordlist[0])
                    bNeg.append(values)
                    brandnameScore.append(values)
                if keys == 'neu':
                    allwords_neu.append(wordlist[0])
                    bNeu.append(values)
                    brandnameScore.append(values)
        return bPos, bNeg, bNeu, brandnameScore, bDate, bCondition, allwords_pos, allwords_neg, allwords_neu
    else:
        print "Brand Drug"
        posts1 = brandnameReviews.objects(name=message)
        # return render_to_response('sentimental/results.html', {'Posts': posts, 'Posts1': posts1})
        print len(posts1)
        analyzer = SentimentIntensityAnalyzer()
        for post in posts1:
            score, wordlist = analyzer.polarity_scores(post.review)
            bDate.append(parser.parse(post.date).year)
            bCondition.append(post.condition)
            # print map(max,zip(*score.items()))
            for keys, values in score.items():
                if keys == 'pos':
                    allwords_pos.append(wordlist[0])
                    brandnameScore.append(values)
                    bPos.append(values)
                if keys == 'neg':
                    allwords_neg.append(wordlist[0])
                    bNeg.append(values)
                    brandnameScore.append(values)
                if keys == 'neu':
                    allwords_neu.append(wordlist[0])
                    bNeu.append(values)
                    brandnameScore.append(values)
        return bPos, bNeg, bNeu, brandnameScore, bDate, bCondition, allwords_pos, allwords_neg, allwords_neu
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

    wordlist = list()

    brands_data = brandnameReviews.objects(condition=condition_name)
    analyzer = SentimentIntensityAnalyzer()

    for data in brands_data:
        brandDrugName.append(data.name)
        score, wordlist = analyzer.polarity_scores(data.review)
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

def conditionScoreforGeneric(condition_name, flag):

    genericPos = list()
    genericNeg = list()
    genericNeu = list()
    genericDate = list()
    genericDrugName = list()
    wordlist = list()


    generic_data = genericnameReviews.objects(condition=condition_name)
    analyzer = SentimentIntensityAnalyzer()

    for data in generic_data:
        genericDrugName.append(data.name)
        score, wordlist = analyzer.polarity_scores(data.review)
        genericDate.append(parser.parse(data.date).year)
        for keys, values in score.items():
            if keys == 'pos':
                genericPos.append(values)
            if keys == 'neg':
                genericNeg.append(values)
            if keys == 'neu':
                genericNeu.append(values)
    if flag == 'true':
        return genericPos, genericNeg, genericNeu, genericDate, genericDrugName
    else:
        return genericPos, genericNeg, genericNeu, genericDate

def countWords(pos, neg, neu):
    alldata_pos = list()
    alldata_neg = list()
    alldata_neu = list()

    alldata_pos = list(itertools.chain.from_iterable(pos[0]))
    # alldata_neg = list(itertools.chain.from_iterable(neg[0]))
    # alldata_neu = list(itertools.chain.from_iterable(neu[0]))
    # print alldata_pos
    # counter_pos = collections.Counter(alldata_pos).clear()
    counter_pos = collections.Counter(alldata_pos)

    # counter_pos = [[x, alldata_pos.count(x)] for x in set(alldata_pos)]
    # counter_neg = collections.Counter(alldata_neg)
    # counter_neu = collections.Counter(alldata_neu)
    # print counter_pos.most_common()

    f = open("data.txt", "w")
    f.write(str(counter_pos.most_common(50)))  # str() converts to string
    f.close()

    return counter_pos.most_common(50)
