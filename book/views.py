from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Book, IssuedBook
# Create your views here.
from django.views import View
import json
from datetime import datetime


def autocompleteModel(request):
    """searchbar autocomplete"""
    if request.is_ajax():
        q = request.GET.get('term')
        search_qs = Book.objects.filter(name__istartswith=q)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class BookSearch(View):
    """provides list of all book for search """

    def get(self, request):
        return render(request, 'book/book_search.html')

    def post(self, request):
        bookinput = request.POST.get('bookinput').strip()
        searchresult = Book.objects.all().filter(name__iexact=bookinput)
        return render(request, 'book/book_search.html', {'searchresult': searchresult})


class MyIssuedBook(View):
    """book issue request and user's book list"""

    def get(self, request):
        booklist = IssuedBook.objects.filter(user=request.user, status='booked')
        return render(request, 'accounts/index.html', {'booklist': booklist})

    def post(self, request):
        data = request.POST.copy()
        bookinput = Book.objects.get(id=data.get('book'))
        print(IssuedBook.objects.filter(user=request.user, status='booked').count())
        if IssuedBook.objects.filter(user=request.user,
                                     status='booked').count() < 3:  # User can not issue more than 3 books
            if bookinput.avail_stock > 0:
                new_issue = IssuedBook.objects.create(book=bookinput, user=request.user,
                                                      issued_date=datetime.now().date(),
                                                      return_date=request.POST.get('date'))
                messages.info(request,"Waiting for Librarian's Confirmation..You will be notified by email when its been approved")
        else:
            messages.error(request, 'You have already issued 3 books, return any book in order to issue another..')
            booklist = IssuedBook.objects.filter(user=request.user, status='booked')
            return render(request, 'accounts/index.html', {'booklist': booklist})
        return render(request, 'accounts/index.html')


class ApproveReq(View):
    """for Librarian to accept req """

    def get(self, request):
        pending_req = IssuedBook.objects.filter(status='pending')
        return render(request, 'accounts/index.html', {'pending_req': pending_req})

    def post(self, request):
        print(request.POST.get('book'))
        req = IssuedBook.objects.get(book__id=request.POST.get('book'), user__id=request.POST.get('user_id'))

        req.status = 'booked'
        req.save()
        print('updated')
        pending_req = IssuedBook.objects.filter(status='pending')
        messages.info(request, 'Approved book ' + str(req.book.name) + ' for user ' + str(req.user.name))
        return render(request, 'accounts/index.html', {'pending_req': pending_req})


class ReturnBook(View):

    def post(self, request):
        print(request.POST.get('entry_id'))
        obj_del = IssuedBook.objects.filter(id=request.POST.get('entry_id'))
        print(obj_del)
        obj_del[0].delete()
        book = Book.objects.get(id=request.POST.get('book'))
        book.avail_stock += 1
        book.save()
        print('deleted')
        messages.info(request, 'Book is returned')
        booklist = IssuedBook.objects.filter(user=request.user, status='booked')
        return render(request, 'accounts/index.html', {'booklist': booklist})
