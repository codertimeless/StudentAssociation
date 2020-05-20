from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models.user_profile import ClubUserProfile
from management.models.club import Club
from management.models.activity_apply import ActivityApplication
from management.models.activity import Activity
from StudentAssociation.utils import get_info_from_cache
from django.utils import timezone


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
        context['teacher'] = ClubUserProfile.objects.get(job="指导老师", club=club)
        context['master'] = ClubUserProfile.objects.get(job="会长", club=club)
        context['club'] = club

    return render(request, 'manage_club.html', context=context)


@login_required(login_url='/login/')
def activity_apply(request):
    """
    if request.method == "GET" and activity_id is not none,
    then check special application.
    if request.method == "POST", the request is a apply.
    """

    context = {"apply": True}

    if request.method == "GET":
        return render(request, "activity_apply_v1.html", context)

    if request.method == "POST":
        act_name = request.POST.get("act_name", "")
        act_place = request.POST.get("act_place", "")
        act_type = request.POST.get("act_type", "")
        coo_club = request.POST.get("coo_club", "")
        description = request.POST.get("description", "")
        validation_code = request.POST.get("validation_code", "")

        # if Club.objects.filter(name=coo_club).exists():
        #     coo_club = Club.objects.filter(name=coo_club)
        # if get_info_from_cache(request.user.phone_number, "act_apply") == validation_code:
        ap = ActivityApplication.objects.create(name=act_name, venue=act_place, activity_type=act_type,
                                                description=description, main_club=request.profile.club,
                                                apply_people=request.profile, date=timezone.now())
        context['error'] = True
        context['message_type'] = "提示"
        context['error_message'] = "活动创建成功"

        return render(request, "activity_apply_v1.html", context)

        # else:
        #     context['error'] = True
        #     context['error_message'] = "验证码错误，请重试"
        #     return render(request, "activity_apply_v1.html", context)

     # else:
     #    try:
     #        ap = ActivityApplication.objects.get(activity_id)
     #    except ActivityApplication.DoesNotExist:
     #        context["error"] = True
     #        context["error_message"] = "活动申请不存在，请先创建"
     #        return render(request, "apply_activity_v1.html", context)
     #    context = ap.get_act_apply_info()


def activity_check(request, activity_id):
    context = {'apply': False}

    if request.method == "GET" and activity_id:
        try:
            ap = ActivityApplication.objects.get(pk=activity_id)
        except ActivityApplication.DoesNotExist:
            context["error"] = True
            context["error_message"] = "活动申请不存在，请先创建"
            return render(request, "activity_apply_v1.html", context)
        context = ap.get_act_apply_info()
        context['activity_id'] = activity_id
        return render(request, "activity_apply_v1.html", context)


def manage_activity(request):
    activities = ActivityApplication.objects.filter(main_club=request.profile.club).order_by("-apply_time")
    context = {"activities": activities}

    return render(request, "manage_activity_1.html", context)


def activity_info(request, activity_id):
    context = {}

    if request.method == "GET" and activity_id:
        try:
            activity_info = Activity.objects.get(active_id=activity_id)
        except ActivityApplication.DoesNotExist:
            context["error"] = True
            context["error_message"] = "活动申请不存在，请先创建"
            return render(request, "activity_apply_v1.html", context)
        ap = activity_info.activity_application

        context = ap.get_act_apply_info()
        return render(request, "activity_info_v1.html", context)
