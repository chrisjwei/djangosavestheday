"""
Definition of views.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib import auth
from app.models import *
from django.contrib.auth.models import User
import sqlite3
import re

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)      

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(reverse("app/index.html"))
    else:
        return HttpResponseRedirect("app/index.html")

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("app/index.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/dashboard/")
    else:
        form = UserCreationForm()
    return render(request, "app/register.html", {
        'form': form,
    })

def signin(request):
    return render(request, "app/signin.html")

def cleanQuery(sql):
    return re.sub(r'\W+', '', sql)

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
    context['text'] = text
    context['name'] = drugname
    return render(
        request,
        'app/fact.html',context)