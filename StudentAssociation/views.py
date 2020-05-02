from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .utils import send_message


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


@login_required
def logout_view(request):
    logout(request)
    # TODO user is not login
    return HttpResponseRedirect(reverse("index"))


def register_view(request):

    return render(request, "register_v1.html")


def forget_view(request):

    return render(request, "forget.html")


def join_club_view(request):

    return render(request, "join_club_v1.html")


def send_msg(request):
    send_message("18570748208", "123969")
    return HttpResponseRedirect(reverse("index"))
