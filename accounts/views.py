from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import *
from django.views import View
from django.contrib.messages.views import messages


def index(request):
    return render(request, 'accounts/base.html')


class Login(View):
    def get(self, request):
        form = LoginForm()
        messages.warning(request, 'Please Login in order to continue!')
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            print('isvalid')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                print('login successfull')
                return redirect('book:booksearch')
            else:
                messages.error(request, 'User Not Found please Enter Valid data' + str(form.errors))
        return render(request, 'accounts/login.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        print('logged out')
        return redirect("accounts:index")

class Registration(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'accounts/registrations.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Registration fail..')
            return render(request, 'accounts/registrations.html', {'form': form})

        return redirect('accounts:login')
