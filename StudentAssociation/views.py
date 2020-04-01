from django.shortcuts import render, reverse
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login_v1.html")

    context = {}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["Password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login_v1.html", context=context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        # TODO user is not login
        return HttpResponseRedirect(reverse("login"))

    return HttpResponseRedirect(reverse("index"))


def register_view(request):

    return render(request, "register_v1.html")


def forget_view(request):

    return render(request, "forget.html")


def join_club_view(request):

    return render(request, "join_club_v1.html")
