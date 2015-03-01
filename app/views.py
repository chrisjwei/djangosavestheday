"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import *
from django.contrib.auth.models import User
import sqlite3
import re

def cleanQuery(sql):
    return re.sub(r'\W+', '', sql)

def webscrape(name):
    return "LOL"

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def results(request):
    """Renders the search page."""
    assert isinstance(request, HttpRequest)
    context = {}
    if 'query' in request.POST:
        query = cleanQuery(request.POST['query'])
        context['query'] = request.POST['query']
        context['result'] = []
        context['valid'] = False
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        sql = '''SELECT * FROM product WHERE SponsorApplicant LIKE \'%''' + query + '''%\' OR drugname LIKE \'%''' + query + "%\' OR activeingred LIKE \'%" + query + "%\';"
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        if (len(result) > 0):
            context['result'] = result
            context['valid'] = True

    return render(
        request,
        'app/results.html',context
        )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

def dashboard(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/dashboard.html')

def fact(request,drugname):
    assert isinstance(request, HttpRequest)
    context={}
    text = ""
    text = text+webscrape(drugname)
    context['text'] = text
    context['name'] = drugname
    return render(
        request,
        'app/fact.html',context)