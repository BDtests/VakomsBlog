from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import CustomUser
from utils.responsehelper import (RESPONSE_400_INVALID_DATA,
                                  RESPONSE_400_INVALID_HTTP_METHOD)
from django.shortcuts import render
from django.urls import reverse
from utils.send_email import send_email
from vacomsBlog import settings


def register(request):
    if request.method == 'POST':
        data = request.POST
        user = CustomUser.create(first_name=data.get('first_name'),
                                 last_name=data.get('last_name'),
                                 email=data.get('email'),
                                 phone=data.get('phone'),
                                 password=data.get('password')
                                 )
        if user:
            email_data = {'domain': settings.FRONT_HOST,
                          'token': user.email}
            subject = 'VakomsBlog Activation'
            message = 'registration'
            template = 'registration.html'
            send_email(subject,
                       message,
                       [user.email,],
                       template,
                       email_data)
            return render(request, 'authentication/index.html')
    else:
        return render(request, 'authentication/register.html')


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(email=data.get('email'),
                            password=data.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("home:index"))
        else:
            return RESPONSE_400_INVALID_DATA
    elif request.method == 'GET':
        return render(request, 'authentication/login.html')
    else:
        return RESPONSE_400_INVALID_HTTP_METHOD


def logout_user(request):
    if request.method == "GET":
        logout(request)
        return HttpResponseRedirect(reverse("home:index"))
    return RESPONSE_400_INVALID_HTTP_METHOD


def activate(request, token):
    if request.method == "GET":
        user = CustomUser.get_by_email(token)
        if user:
            user.activate()
            return HttpResponseRedirect(reverse("home:index"))