from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [

    url(r'ajax_calls/search/$', views.autocompleteModel),
    path('',views.BookSearch.as_view(),name='booksearch'),
    path('issued/',views.MyIssuedBook.as_view(),name='myissuedbook'),

]