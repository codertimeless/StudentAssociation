from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from accounts.models.user_profile import ClubUserProfile
from management.models.club import Club
from management.models.activity_apply import ActivityApplication
from management.models.activity import Activity
from StudentAssociation.utils import get_info_from_cache
from StudentAssociation.utils import send_inner_message
from accounts.models.studentclub_user import StudentClubUser
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
        club_users = ClubUserProfile.objects.filter(club__name=club_name, is_active=True, job="成员")
        context['club_name'] = club_name
        context['club_users'] = club_users
    else:
        error_message = "抱歉，您不能访问这个网站"

    return render(request, "manage_user_v1.html", context=context)


@login_required(login_url='/login/')
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


@login_required(login_url="/login/")
def manager_user(request):
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
def activity_apply(request):
    """
    if request.method == "GET" and activity_id is not none,
    then check special application.
    if request.method == "POST", the request is a apply.
    """
    if request.profile.job == "成员" or request.profile.job == "匿名":
        return redirect("all_activities")

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
        act_date = request.POST.get("act_date", "")
        act_date = timezone.datetime.strptime(act_date, "%Y-%m-%d %H-%M")

        # if Club.objects.filter(name=coo_club).exists():
        #     coo_club = Club.objects.filter(name=coo_club)
        # if get_info_from_cache(request.user.phone_number, "act_apply") == validation_code:
        ap = ActivityApplication.objects.create(name=act_name, venue=act_place, activity_type=act_type,
                                                description=description, main_club=request.profile.club,
                                                apply_people=request.profile, date=act_date, ap_status="审核中")
        context['error'] = True
        context['message_type'] = "提示"
        context['error_message'] = "活动创建成功"
        content = request.profile.club.name + "发起了一个新的活动申请，请点击下方查看详情按钮进行审核。"
        to_users = ClubUserProfile.objects.filter(job="活动管理")
        next_url = "/manage/activity_check/" + str(ap.pk)
        for to_user in to_users:
            send_inner_message(content, to_user, next_url, "活动消息")

        return render(request, "activity_apply_v1.html", context)


@login_required(login_url='/login/')
def activity_check(request, activity_id):
    context = {'apply': False}
    if request.profile.job == "成员" or request.profile.job == "匿名":
        return redirect("all_activities")

    if request.method == "GET" and activity_id:
        try:
            ap = ActivityApplication.objects.get(pk=activity_id)
        except ActivityApplication.DoesNotExist:
            context["error"] = True
            context["error_message"] = "活动申请不存在，请先创建"
            context['error_type'] = "错误："
            return redirect("apply")

        context = ap.get_act_apply_info()
        context['activity_id'] = activity_id
        context['review1'] = ap.adjust_suggest_ass
        context['review2'] = ap.adjust_suggest_tea

        if request.profile.job == "活动管理":
            if ap.ap_status == "审核中":
                context['check_ass'] = True
            else:
                context['check_ass'] = False
        if request.profile.job == "指导老师":
            if ap.ap_status == "等待指导老师审核":
                context['check_tea'] = True
            else:
                context['check_tea'] = False
        if request.profile.job == "会长":
            if "修改" in ap.ap_status:
                context['apply'] = True
                context['request_change'] = True
        return render(request, "activity_apply_v1.html", context)

    if request.method == "POST" and activity_id:
        try:
            ap = ActivityApplication.objects.get(pk=activity_id)
            context = ap.get_act_apply_info()

            if request.profile.job == "活动管理":
                sug = request.POST.get("review1", "")
                status = request.POST.get("optionsRadios", "")
                ap.adjust_suggest_ass = sug
                if status == "agree":
                    ap.ap_status = "等待指导老师审核"
                    content = "您的活动申请" + ap.name + "已经获得了社联管理人员的同意，请点击下方查看详情按钮获取更多信息。"
                    content2 = ap.main_club.name + "有一个活动等待您的审核，请点击下方按钮查看详情按钮扭曲更多信息"
                    next_url = "/manage/activity_check/" + str(ap.pk) + "/"
                    to_user2 = ClubUserProfile.objects.get(job="指导老师", club=ap.main_club)
                    send_inner_message(content, to_user2, next_url, message_type="活动消息")

                elif status == "no":
                    ap.ap_status = "学社联拒绝"
                    ap.is_check_over = True
                    content = "您的活动申请" + ap.name + "已被社联管理人员拒绝，请点击下方查看详情按钮获取更多信息。"

                elif status == "request_change":
                    ap.ap_status = "学社联要求修改"
                    content = "您的活动申请" + ap.name + "，社联管理人员要求对活动信息进行更改，请点击下方查看详情按钮获取更多信息。"

                ap.save()
                next_url = "/manage/activity_check/" + str(ap.pk) + "/"
                to_user = ClubUserProfile.objects.get(phone_number=ap.apply_people.phone_number)
                send_inner_message(content, to_user, next_url, message_type="活动消息")
            elif request.profile.job == "指导老师":
                sug = request.POST.get("review2", "")
                status = request.POST.get("optionsRadios", "")
                ap.adjust_suggest_tea = sug
                if status == "agree":
                    ap.ap_status = "待举办"
                    # todo activity_info

                    content = "您的活动申请" + ap.name + "已经获得了指导老师的同意，请点击下方查看详情按钮获取更多信息。"
                    ap.is_check_over = True
                    Activity.objects.create(activity_application=ap)

                elif status == "no":
                    ap.ap_status = "指导老师已拒绝"
                    ap.is_check_over = True
                    content = "您的活动申请" + ap.name + "已被老师拒绝，请点击下方查看详情按钮获取更多信息。"

                elif status == "request_change":
                    ap.ap_status = "指导老师要求修改"
                    content = "您的活动申请" + ap.name + "，老师要求对活动信息进行更改，请点击下方查看详情按钮获取更多信息。"

                ap.save()
                next_url = "/manage/activity_check/" + str(ap.pk) + "/"
                to_user = ClubUserProfile.objects.get(phone_number=ap.apply_people.phone_number)
                send_inner_message(content, to_user, next_url, message_type="活动消息")

            context['error'] = True
            context['error_message'] = "活动审核成功"
            context['message_type'] = '提示：'
            context['activity_id'] = activity_id

        except ActivityApplication.DoesNotExist:
            context["error"] = True
            context["error_message"] = "活动申请不存在，请先创建"
            context['error_type'] = "错误："
            return redirect("apply")
            context = ap.get_act_apply_info()
            context['activity_id'] = activity_id

        return render(request, "activity_apply_v1.html", context)


def manage_activity(request):
    activities = ActivityApplication.objects.filter(main_club=request.profile.club).order_by("-apply_time")
    act_type = request.GET.get("type", "")
    q = request.GET.get("q", "")

    if act_type == "素拓活动":
        activities = activities.filter(activity_type="素拓活动")
    elif act_type == "大型活动":
        activities = activities.filter(activity_type="大型活动")
    elif act_type == "常规活动":
        activities = activities.filter(activity_type="常规活动")

    if q == "审核中":
        activities = activities.filter(ap_status__contains="审核")
    elif q == "待举办":
        activities = activities.filter(ap_status="待举办")
    elif q == "已完成":
        activities = activities.filter(ap_status="已完成")
    elif q == "待修改":
        activities = activities.filter(Q(ap_status__contains="修改"))
    elif q == "已拒绝":
        activities = activities.filter(Q(ap_status__contains="拒绝"))

    context = {"activities": activities}

    return render(request, "manage_activity_1.html", context)


def activity_info(request, activity_id):
    context = {}

    if request.method == "GET" and activity_id:
        try:
            activity_info = Activity.objects.get(pk=activity_id)
        except ActivityApplication.DoesNotExist:
            context["error"] = True
            context["error_message"] = "活动申请不存在，请先查看其他活动"
            return redirect("all_activities")
        ap = activity_info.activity_application

        context = ap.get_act_apply_info()
        return render(request, "activity_info_v1.html", context)

    if request.method == "POST" and activity_id:
        try:
            activity_info = Activity.objects.get(pk=activity_id)
        except ActivityApplication.DoesNotExist:
            context["error"] = True
            context["error_message"] = "活动申请不存在，请先查看其他活动"
            return redirect("all_activities")

        ap = activity_info.activity_application
        context = ap.get_act_apply_info()
        if request.user.is_authenticated:
            if request.profile != ap.apply_people:
                context['error'] = True
                context['error_message'] = "您已经成功报名参加该活动！"
                context['message_type'] = "提示"
                return render(request, "activity_info_v1.html", context)
            else:
                context['error'] = True
                context['error_message'] = "您是活动的发起人，您无法报名参加该活动"
                context['message_type'] = "错误："
                return render(request, "activity_info_v1.html", context)
        else:
            context['error'] = True
            context['error_message'] = "请您先登录"
            return redirect("login")
