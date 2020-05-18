from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models.user_profile import ClubUserProfile
from management.models.club import Club
from management.models.activity_apply import ActivityApplication


@login_required(login_url='/login/')
def club_manager(request):
    context = {}
    if request.profile.is_manager:
        club_name = request.profile.club.name
        club_users = ClubUserProfile.objects.filter(club__name=club_name, is_active=True, job="manager")


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

    return render(request, "manage_user_v1.html", context=context)


@login_required(login_url='/login/')
# @require_manager
def manage_club(request):
    error_message = ""
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
def activity_apply(request, activity_id=None):
    context = {"apply": True}

    if request.profile.is_manager:
        club_name = request.profile.club.name

    if request.method == "GET" and activity_id is None:
        return render(request, "apply_activity_v1.html", context)

    elif request.method == "GET" and activity_id:
        try:
            ap = ActivityApplication.objects.get(activity_id)
        except ActivityApplication.DoesNotExist:
            context["error"] = True
            context["error_message"] = "活动申请不存在，请先创建"
            return render(request, "apply_activity_v1.html", context)
        context = ap.get_act_apply_info()

        return render(request, "apply_activity_v1.html", context)

    else:
        if activity_id is None:
            print(request.POST)

            return render(request, "apply_activity_v1.html", context)

        else:
            try:
                ap = ActivityApplication.objects.get(activity_id)
            except ActivityApplication.DoesNotExist:
                context["error"] = True
                context["error_message"] = "活动申请不存在，请先创建"
                return render(request, "apply_activity_v1.html", context)
            context = ap.get_act_apply_info()


def manage_activity(request):
    return render(request, "manage_activity_1.html")
