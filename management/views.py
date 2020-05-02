from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models.user_profile import ClubUserProfile
from management.models.club import Club
from management.models.activity import Activity


@login_required(login_url='/login/')
def club_user(request):
    context = {}
    if request.profile.is_manager:
        club_name = request.profile.club.name
        club_users = ClubUserProfile.objects.filter(club__name=club_name, is_active=True)

        context['club_name'] = club_name
        context['club_users'] = club_users
    else:
        error_message = "抱歉，您不能访问这个网站"

    return render(request, "manage_v1.html", context=context)


@login_required(login_url='/login/')
# @require_manager
def manage_club(request):
    context = {}
    if request.profile.is_manager:
        club_name = request.profile.club.name
        try:
            club = Club.objects.get(name=club_name, is_active=True)

        except Club.DoesNotExist:
            club = None
            error_message = "改社团正在整改中"

        context['error'] = error_message
        context['club'] = club
    return render(request, 'manage_club.html', context=context)


@login_required(login_url='/login/')
def activity_apply(request):
    context = {}
    if request.profile.is_manager:
        club_name = request.profile.club.name
