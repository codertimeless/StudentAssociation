from django.http import request, response
from django.shortcuts import render
from django.http import HttpResponse


def my_view(x, y):
    return x+y
