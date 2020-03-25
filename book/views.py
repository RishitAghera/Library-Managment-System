from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Book, IssuedBook, LibrarianTemp
# Create your views here.
from django.views import View
import json
from datetime import datetime


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

    def post(self, request):
        bookinput = request.POST.get('bookinput').strip()
        print(bookinput)
        # if(Book)

        searchresult = Book.objects.all().filter(name__iexact=bookinput)
        return render(request, 'book/book_search.html', {'searchresult': searchresult})


class MyIssuedBook(View):

    def post(self, request):
        data=request.POST.copy()
        bookinput = Book.objects.get(id=data.get('book'))
        print(request.POST.get('date'))
        print(bookinput.avail_stock)

        if bookinput.avail_stock > 0:
            new_issue=LibrarianTemp.objects.create(book=bookinput,user=request.user,issued_date=datetime.now().date(),return_date=request.POST.get('date'))
            messages.info(request,"Waiting for Librarian's Confirmation..You will be notified when its been approved")

        return render(request, 'accounts:index')
