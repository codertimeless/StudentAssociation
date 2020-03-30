from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


def main_view(request):
    context = {}
    if request.user.is_authenticated:
        user = "logan"

    return render(request, "index_v1.html", context=context)


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            return render(request, "login_v1.html")

    context = {}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["Password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "login_v1.html", context=context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        # TODO user is not login
        return HttpResponseRedirect("/")

    return HttpResponseRedirect("/")
