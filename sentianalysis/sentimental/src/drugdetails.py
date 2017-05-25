import collections
import dateutil.parser as parser

from sentimental.src.searchdatabase import *

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, Context
from numpy import mean
from sentimental.database import CSVtoMongoDB
from sentimental.models import brandnameReviews, genericnameReviews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def drugdetail(request):
    brandPos = list()
    brandNeg = list()
    brandNeu = list()
    brandDate = list()
    brandDrugName = list()


    if 'condition' in request.GET:
        message = request.GET['condition']
    else:
        message = 'You submitted nothing!'

    context = {
        'condition': message
    }

    brandPos, brandNeg, brandNeu, brandDate, brandDrugName = conditionScoreforBrands(message, 'true')


    print set(brandDrugName)

    return render_to_response('sentimental/drugdetail.html', context)