import collections
import dateutil.parser as parser

from sentimental.src import *
from sentimental.src.home import *
from sentimental.src.searchdatabase import *

from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt


from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, Context
from numpy import mean
from sentimental.database import CSVtoMongoDB
from sentimental.models import brandnameReviews, genericnameReviews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def keywordslist(request):
    d = path.dirname("/Users/Nil/GradFinalProject/sentianalysis/")
    # / Users / Nil / GradFinalProject / sentianalysis / data.txt
    text = open(path.join(d, 'data.txt')).read()
    wordcloud = WordCloud().generate(text)

    wordcloud = WordCloud(max_font_size=40).generate(text)
    # plt.figure()
    # plt.imsave("words.png",wordcloud)
    # plt.axis("off")
    image = wordcloud.to_image()

    wordcloud.to_file("data.png")

    # image.show()
    return render_to_response('sentimental/keywords.html')
