import os
import sqlite3
from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from .models import User
from django.views.decorators.csrf import csrf_exempt
from xml.dom import pulldom
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges


def index(request):
    context = {}
    return render(request, 'index.html', context)

# FLAW 1: Broken Access Control
def flaw1(request):
    file = request.GET.get('file')
    if file is not None:
        context = { 
            'content':  open('files/' + file, 'r').read()
        }
    else:
        context = {}
        

    return render(request, 'flaw1.html', context)

def fix1(request):
    file = request.GET.get('file')
    if file is not None:
        safe = is_directory_traversal(file)
        if safe is True:
            return HttpResponseForbidden()

        context = { 
            'content':  open(file, 'r').read()
        }
    else:
        context = {}
        
    return render(request, 'fix1.html', context)


# FLAW 2: Cross-Site Scripting (XSS)
def flaw2(request):
    context = { "comment": request.POST.get("comment") }
    return render(request, 'flaw2.html', context)

def fix2(request):
    context = { "comment": request.POST.get("comment") }
    return render(request, 'fix2.html', context)

# FLAW 3: Injection
def flaw3(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username is not None and password is not None:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        user = cursor.execute("SELECT * FROM myapp_User WHERE username LIKE '" + username + "' AND password LIKE '" + password + "'").fetchall()    
        context = { "user": user }
        return render(request, 'flaw3.html', context)
    else:
        context = { }
        return render(request, 'flaw3.html', context)

def fix3(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username is not None and password is not None:
        user = User.objects.get(username = username, password = password)
        context = { "user": user }
        return render(request, 'flaw3.html', context)
    else:
        context = { }
        return render(request, 'fix3.html', context)

# FLAW 4: XML External Entities (XXE)
def flaw4(request):
    payload = request.POST.get("xml")
    if payload is not None:
        parser = make_parser()
        parser.setFeature(feature_external_ges, True)
        doc = pulldom.parseString(payload, parser=parser)
        out = ""
        for event, node in doc:
            out += node.toxml()
            
        context = { "xml": out }
        return render(request, 'flaw4.html', context)
    else:
        return render(request, 'flaw4.html', {})

def fix4(request):
    payload = request.POST.get("xml")
    if payload is not None:
        doc = pulldom.parseString(payload)
        out = ""
        for event, node in doc:
            out += node.toxml()
            
        context = { "xml": out }
        return render(request, 'fix4.html', context)
    else:
        return render(request, 'fix4.html', {})

# FLAW 5: Security Misconfiguration
def flaw5(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username is not None and password is not None:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        user = cursor.execute("SELECT * FROM myapp_User WHERE username LIKE '" + username + "' AND password LIKE '" + password + "'").fetchall()    
        context = { "user": user }
        return render(request, 'flaw5.html', context)
    else:
        context = { }
        return render(request, 'flaw5.html', context)

def fix5(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username is not None and password is not None:
        user = User.objects.get(username = username, password = password)
        context = { "user": user }
        return render(request, 'flaw3.html', context)
    else:
        context = { }
        return render(request, 'fix3.html', context)


# Source: https://stackoverflow.com/questions/6803505/does-my-code-prevent-directory-traversal
def is_directory_traversal(file_name):
    current_directory = os.path.abspath(os.curdir)
    requested_path = os.path.relpath(file_name, start=current_directory)
    requested_path = os.path.abspath(requested_path)
    common_prefix = os.path.commonprefix([requested_path, current_directory])
    return common_prefix != current_directory