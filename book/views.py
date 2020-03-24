from django.http import HttpResponse
from django.shortcuts import render
from .models import Book
# Create your views here.
from django.views import View
import json


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term')
        search_qs = Book.objects.filter(name__istartswith=q)
        results = []
        print('q:')
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class BookSearch(View):
    def get(self, request):
        return render(request, 'book/book_search.html')
