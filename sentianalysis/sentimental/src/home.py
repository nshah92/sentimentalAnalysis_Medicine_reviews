'''
For Line chart
    x-axis -> date
    y-axis -> score

'''

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

    brandPos, brandNeg, brandNeu, brandDate = conditionScoreforBrands(med_condition, 'false')
    brand_count = len(brandPos)

    genericPos, genericNeg, genericNeu, genericDate = conditionScoreforGeneric(med_condition, 'false')
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
    return render_to_response('sentimental/graphs.html', data)
