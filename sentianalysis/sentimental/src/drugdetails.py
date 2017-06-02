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
    '''
        graphdata_brand and graphdata_generic
        0 = drug_name
        1 = pos
        2 = neg
        3 = neu
        4 = date
    '''
    extra_serie = {}

    Pos = list()
    Neg = list()
    Neu = list()
    Date = list()
    DrugName = list()
    drugs = list()

    if 'condition' in request.GET:
        message = request.GET['condition']
    else:
        message = 'You submitted nothing!'

    if request.GET['flag'] == 'true':
        Pos, Neg, Neu, Date, DrugName = conditionScoreforBrands(message, 'true')
    else:
        Pos, Neg, Neu, Date, DrugName = conditionScoreforGeneric(message, 'true')

    data = sorted(zip(Date, DrugName, Pos, Neg, Neu), key = lambda x: x[1])

    graphdata = filterRecords(DrugName, data)
    chartaxis = list()
    i = 0
    charttype = "lineChart"
    finaldata = {}
    for item in graphdata:
        chartdata = {
            'x': item[4],
            'name1': 'Positive', 'y1': item[1], 'extra1': extra_serie,
            'name2': 'Negetive', 'y2': item[2], 'extra2': extra_serie,
            'name3': 'Netural', 'y3': item[3], 'extra3': extra_serie,
        }
        chartaxis.append(chartdata)

        data = {
            'record':len(graphdata),
            'medicine'+str(i): str(item[0]).title(),
            'charttype'+str(i): charttype,
            'chartdata'+str(i): chartaxis[i],
            'chartcontainer'+str(i): 'linechart_container'+str(i),

            'extra'+str(i): {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            }
        }
        i = i+1
        finaldata.update(data)
    return render_to_response('sentimental/drugdetail.html', finaldata)

def filterRecords(drugName, data):
    '''i[0] = date, i1= Name, i2,i3,i4= pos, neg, neu'''
    p = list()
    d = list()
    n = list()
    ne = list()
    l_drug = ""
    drugs = set(drugName)
    graphdata = list()
    print drugs
    print len(drugs)
    for i in range(0, len(drugs)):
        currentdrug = drugs.pop()
        p = list()
        d = list()
        n = list()
        ne = list()
        l_drug = ""
        for item in data:
            if item[1] == currentdrug:
                d.append(item[0])
                l_drug = item[1]
                p.append(item[2])
                n.append(item[3])
                ne.append(item[4])
            avg_d, avg_p = getAverage(p, d)
            avg_d1, avg_n = getAverage(n, d)
            avg_d2, avg_ne = getAverage(ne, d)

        result = (l_drug, avg_p, avg_n, avg_ne, avg_d)
        graphdata.append(result)
    return graphdata