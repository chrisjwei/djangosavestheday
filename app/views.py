"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import *
from django.contrib.auth.models import User
from HTMLParser import HTMLParser
import unicodedata
import htmlentitydefs
import sqlite3
import re
import requests

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        codepoint = htmlentitydefs.name2codepoint[name]
        self.result.append(unichr(codepoint))

    def get_text(self):
        return u''.join(self.result)

def html_to_text(html):
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()

def cleanQuery(sql):
    return re.sub(r'\W+', '', sql)

def unicodeToASCII(uni):
    return unicodedata.normalize('NFKD', uni).encode('ascii','ignore')


def webscrape(name):
    codewords=[name+" is a ", "it is used for " " side effects ", " side-effects ", " abuse ", " overdose "," usage ", " therapy ", " helps "]
    text=""
    '''
    
    googleurl = "https://www.google.com/#q="+name
    for n in xrange(3):
        url = getNthGoogleLink(n,googleurl)
        text+= scrape(url)
    '''
    url2=""
    url1="https://en.wikipedia.org/w/index.php?search="+name
    url ="http://www.drugs.com/"+name+".html"
    xpath='''//*[@id="firstHeading"]'''
    page = requests.get(url)
    if (page == None): page = requests.get(url1)
    if (page == None): page = requests.get(url2)
    temp=unicodeToASCII(html_to_text(page.text))
    temp= re.sub("([\(\[]).*?([\)\]])", "", temp)
    temp=[x for x in map(str.strip, temp.split('.')) if x]
    
    
    for sentence in temp:
        for codeword in codewords:
            if (codeword in sentence):
                s = sentence.strip()
                if codeword == name+" is a ":
                    s = s[s.index(codeword):]
                text+=(s+". ")
    return text

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