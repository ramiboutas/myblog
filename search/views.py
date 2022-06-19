from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse

from wagtail.core.models import Page, Locale
from wagtail.search.models import Query


def open_search_modal(request):
    context = {}
    return render(request, 'search/modal.html', context)

def close_search_modal(request):
    return HttpResponse(status=200)

def search(request):
    search_query = request.GET.get('query', None)

    if search_query:
        search_results = Page.objects.live().filter(locale=Locale.get_active()).search(search_query)[:10]
        query = Query.get(search_query)
        query.add_hit() # Record hit
    else:
        search_results = Page.objects.none()

    return TemplateResponse(request, 'search/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
