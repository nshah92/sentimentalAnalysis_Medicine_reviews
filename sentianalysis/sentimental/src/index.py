from django.shortcuts import render, render_to_response

from django.template import RequestContext, Context
from numpy import mean
import collections

from sentimental.database import CSVtoMongoDB
from sentimental.models import brandnameReviews, genericnameReviews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import dateutil.parser as parser

from django.http import HttpResponse

def index(request):
    context = {'all_data': ''}
    return render(request, 'sentimental/index.html', context)