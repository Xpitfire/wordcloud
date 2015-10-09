"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app import models

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'WordCloud',
            'year':datetime.now().year,
        })
    )

def search(request):
    """Renders the search result page."""
    searchbox = request.GET.get('searchbox')
    for char in "'\";":
        searchbox = searchbox.replace(char, "")
    if searchbox is None or searchbox == "":
        return render(request, 'app/index.html',
                      {'title':'WordCloud',
                       'infotxt':'Type in your idea',
                       'year':datetime.now().year,
                       'error': True})
    else:
        return render(request, 'app/search.html',
                      {'title':'WordCloud',
                       'infotxt':'Results',
                       'year':datetime.now().year,
                       'linklist':models.getLinksForKeyword(searchbox)})
    
