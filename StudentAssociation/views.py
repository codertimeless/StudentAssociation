import random

from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.db.models import Q

from .utils import message_service, get_info_from_cache
from accounts.models.studentclub_user import StudentClubUser
from accounts.models.messages import Messages
from accounts.models.user_profile import ClubUserProfile
from management.models.club import Club
from management.models.unit import Unit
from management.models.activity import Activity
from .tasks import celery_send_email
from management.models.student_class import StudentClass

UNIT = {
    "jx": "计算机与信息工程学院",
    "kj": "会计学院",
    "gs": "工商管理学院",
    "cj": "财政与金融学院 ",
    "lg": "旅管学院 ",
    "fg": "法学与公共管理学院 ",
    "sy": "设计与艺术学院 ",
}

ERROR_MESSAGES = {
    "PASSWORD_ERROR": "您输入的账号或密码错误，请确认大小写",
    "USER_NOT_EXIST": "该账号不存在，请先注册，请访问: ",
    "USER_PROFILE_ALREADY": "您已是社团会员，请使用您在社团报名时预留的手机号进行注册",
    "USER_ALREADY": "该账号已存在，请登录。 如需重置密码，请访问: ",
    "CONFIRM_PASSWORD_ERROR": "两次密码不相等，请重新输入",
    "VALIDATION_ERROR": "验证码错误，请检查手机号码是否输入正确",
    "CLUB_NOT_EXIST": "抱歉，该社团暂时无法加入",
    'ALREADY_IN_CLUB': "您已加入了该社团，请勿重复提交",
    "SUCCESS": "",
}


def main_view(request):
    # celery_send_email.delay("subject", "xfhc9495@163.com", "nihaoma")

    return render(request, "index_v1.html")


def login_code_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("main"))
        else:
            return render(request, "login_code_v1.html")

    context = {}
    if request.method == "POST":
        phone_number = request.POST.get("phone_number", "")
        validate_code = request.POST.get("validate_code", "")

        if not phone_number:
            context['error'] = True
            context['error_type'] = "错误"
            context['error_message'] = "请先输入手机号码"

        try:
            user = StudentClubUser.objects.get(phone_number=phone_number)
            code = get_info_from_cache(phone_number, "login")
            if code == validate_code:
                login(request, user)
                return HttpResponseRedirect(reverse("main"))
            else:
                context['error'] = True
                context['error_type'] = "错误"
                context['error_message'] = "验证码错误，请重试"
                context['phone_number'] = phone_number
        except StudentClubUser.DoesNotExist:
            context['error'] = True
            context['error_type'] = "错误"
            context['error_message'] = "该账号不存在，请先注册"

    return render(request, "login_code_v1.html", context=context)


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("main"))
        else:
            return render(request, "login_v1.html")

    context = {"error": False, "error_message": "", "next_url": "", "phone_number": ""}
    error_message = ""
    if request.method == "POST":
        phone_number = request.POST["phone"]
        password = request.POST["Password"]
        user = authenticate(request, username=phone_number, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("main"))
        else:
            try:
                StudentClubUser.objects.get(phone_number=phone_number, is_active=True)
                error_message = 'PASSWORD_ERROR'
                context["phone_number"] = phone_number
            except StudentClubUser.DoesNotExist:
                error_message = 'USER_NOT_EXIST'
                user_profile = ClubUserProfile.objects.filter(phone_number=phone_number, is_active=True)
                if user_profile:
                    error_message = "USER_PROFILE_ALREADY"
                    context['next_url'] = "register"

            context['error'] = True
            context['error_message'] = ERROR_MESSAGES[error_message]

            return render(request, "login_v1.html", context=context)


@login_required
def logout_view(request):
    logout(request)
    # TODO user is not login
    return HttpResponseRedirect(reverse("main"))


def register_view(request):
    if request.user.is_authenticated:
        return render(request, "index_v1.html")

    if request.method == "GET":
        return render(request, "register_v1.html")

    elif request.method == "POST":
        context = {"error": False, "error_message": "", "phone": ""}
        phone_number = request.POST['phone_number']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        validate_code = request.POST["validate_code"]

        try:
            StudentClubUser.objects.get(phone_number=phone_number)
            context["error"] = True
            context["error_message"] = ERROR_MESSAGES["USER_ALREADY"]
            context['phone'] = phone_number
            return render(request, "login_v1.html", context=context)

        except StudentClubUser.DoesNotExist:
            cache_code = get_info_from_cache(phone_number, "register")
            if not cache_code:
                context["error"] = True

            if cache_code != validate_code:
                context["error"] = True
                context["error_message"] = ERROR_MESSAGES["VALIDATION_ERROR"]

            if password1 and password2 and password1 != password2:
                context["error"] = True
                context["error_message"] = ERROR_MESSAGES["CONFIRM_PASSWORD_ERROR"]
                context["phone_number"] = phone_number
                return render(request, "register_v1.html", context=context)
            else:
                user = StudentClubUser.objects.create(phone_number=phone_number)
                user.set_password(password1)
                user.username = username
                user.save()
                try:
                    ClubUserProfile.objects.get(phone_number=phone_number)
                except ClubUserProfile.DoesNotExist:
                    user_profile = ClubUserProfile.objects.create(phone_number=phone_number,
                                                                  real_name="匿名",
                                                                  gender="unknown",
                                                                  joined_date=timezone.now().date(),
                                                                  modify_date=timezone.now().date(),
                                                                  job="anonymous")
                    user_profile.save()

                user = authenticate(request, username=phone_number, password=password1)
                login(request, user)
                return HttpResponseRedirect(reverse("main"))


def forget_view(request):
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        validate_code = request.POST['validate_code']
        password1 = request.POST["password1"]
        password2 = request.POST['password2']
        context = {"error": False, "error_message": "", "phone_number": phone_number}

        try:
            user = StudentClubUser.objects.get(phone_number=phone_number, is_active=True)
            cache_code = cache.get(phone_number)

            if validate_code != cache_code:
                context['error'] = True
                context['error_message'] = ERROR_MESSAGES["VALIDATION_ERROR"]

            context["validate_code"] = validate_code

            if password1 and password2 and password1 != password2:
                context["error"] = True
                context["error_message"] = ERROR_MESSAGES["PASSWORD_ERROR"]
                context["phone_number"] = phone_number
                return render(request, "register_v1.html", context=context)

            user.set_password(password1)
            user.save()
            context['error'] = True
            context['error_message'] = "请使用修改后的密码重新登陆"
            context['phone_number'] = phone_number
            return render(request, 'login_v1.html', context=context)

        except StudentClubUser.DoesNotExist:
            context["error"] = True
            context['error_message'] = ERROR_MESSAGES["USER_NOT_EXIST"]
            return render(request, "forget_password.html", context=context)
    else:
        return render(request, "forget_password.html")


def join_club_view(request, club_abbr="null"):
    context = {}
    if request.method == "GET":
        if club_abbr == "null":
            return render(request, "join_club_v1.html")
        else:
            try:
                club = Club.objects.get(club_abbreviation=club_abbr, is_active=True)
                club_name = club.name
                club_type = club.club_category
                context = {"club_name": club_name, "club_type": club_type}
            except Club.DoesNotExist:
                pass

        return render(request, "join_club_v1.html", context=context)

    elif request.method == "POST":
        try:
            name = request.POST["username"]
            student_number = request.POST['student_number']
            phone_number = request.POST['phone_number']
            class_name = request.POST['class_name']
            unit = request.POST['unit']
            gender = request.POST['gender']
            club_name = request.POST["club_name"]
            validate_code = request.POST.get("verification_code", "")
        except Exception:
            context['error'] = True
            context['error_type'] = "错误："
            context['error_message'] = "请填写好所有信息后提交"
            return render(request, "join_club_v1.html", context=context)

        unit = UNIT[unit]
        unit = Unit.objects.get(name=unit)

        try:
            club = Club.objects.get(name=club_name, is_active=True)
        except Club.DoesNotExist:
            context['error'] = True
            context['error_message'] = ERROR_MESSAGES['CLUB_NOT_EXIST']
            context['error_type'] = "错误："
            context['name'] = name
            context['student_number'] = student_number
            context['phone_number'] = phone_number
            context['class_name'] = class_name
            return render(request, "join_club_v1.html", context=context)

        try:
            ClubUserProfile.objects.get(phone_number=phone_number, club=club, is_active=True)
            context['error'] = True
            context['error_message'] = "您已加入" + club.name + ", 请勿重复报名"
            context['name'] = name
            context['student_number'] = student_number
            context['phone_number'] = phone_number
            context['class_name'] = class_name
            context['validate_code'] = validate_code
            context['error_type'] = "错误："
            return render(request, "join_club_v1.html", context=context)
        except ClubUserProfile.DoesNotExist:
            if get_info_from_cache(phone_number, "join_club") != validate_code:
                context['error'] = True
                context['error_type'] = "错误："
                context['error_message'] = "验证码错误，请重试"
                context['name'] = name
                context['student_number'] = student_number
                context['phone_number'] = phone_number
                context['class_name'] = class_name
                return render(request, "join_club_v1.html", context=context)

            class_name = StudentClass.objects.get(classname=class_name)
            user = ClubUserProfile.objects.create(real_name=name, phone_number=phone_number, gender=gender,
                                                  job="成员", student_class=class_name,
                                                  student_number=student_number, joined_date=timezone.now())
            user.club = club
            user.unit = unit
            user.save()
            StudentClubUser.objects.get_or_create(phone_number=phone_number)

        context['error'] = True
        context['error_message'] = "恭喜您，成功报名" + user.club.name + "，使用手机号登录后可以查看更多社团讯息哦！"
        context['error_type'] = '提示：'

        return render(request, "join_club_v1.html", context=context)


@csrf_exempt
def send_msg(request):
    random_code = random.randint(100000, 999999)
    phone_number = request.POST.get("phone_number", "")
    base_url = request.POST.get("base_url", "")
    usage = ""

    if base_url.endswith("register/"):
        usage = "register"
    elif base_url.endswith("forget_password/"):
        usage = "forget_pw"
    elif base_url.endswith("activity_apply/"):
        usage = "act_apply"
    elif base_url.endswith("login_code/"):
        usage = "login"
    elif base_url.endswith("join_club/"):
        usage = "join_club"

    if phone_number == "" and usage == "act_apply":
        if request.user.is_authenticated:
            phone_number = request.user.phone_number
        else:
            return HttpResponse("error")

    print("手机号：" + phone_number + "，请求验证码：" + str(random_code) + "，用作：" + usage)

    flag, msg_status = message_service(phone_number, random_code)

    if flag:
        cache_message = usage + phone_number
        cache.set(cache_message, random_code, 300)
    else:
        return HttpResponse("send message failed")

    return HttpResponse("send message success")


@login_required(login_url="/login/")
def message_view(request):
    context = {}
    message_list = Messages.objects.filter(to_user=request.profile)
    q = request.GET.get("q", "")
    if q and "所有" not in q:
        message_list = message_list.filter(type__contains=q)

    paginator = Paginator(message_list, 6)

    current_num = int(request.GET.get('page', 1))
    messages = paginator.page(current_num)
    context["messages"] = messages
    context['num_pages'] = paginator.num_pages
    return render(request, "message_v1.html", context=context)


def files_view(request):
    return render(request, "files_v1.html")


def activity(request, activity_id):
    return render(request, "activity_v1.html")


def all_activities_view(request):
    act = Activity.objects.filter(is_over=False)
    act_type = request.GET.get("type", "")
    club_type = request.GET.get("club_type", "")

    if act_type:
        act = act.filter(activity_application__activity_type=act_type)

    if club_type:
        act = act.filter(activity_application__main_club__club_category=club_type)

    context = {"act": act, 'cghd_num': Activity.objects.filter(activity_application__activity_type="常规活动").count(),
               'dxhd_num': Activity.objects.filter(activity_application__activity_type="大型活动").count(),
               'sthd_num': Activity.objects.filter(activity_application__activity_type="素拓活动").count(),
               'wyty_num': Activity.objects.filter(activity_application__main_club__club_category="文娱体育").count(),
               'gysj_num': Activity.objects.filter(activity_application__main_club__club_category="公益实践").count(),
               'xslu_num': Activity.objects.filter(activity_application__main_club__club_category="学术理论").count(),
               'whzh_num': Activity.objects.filter(activity_application__main_club__club_category="文化综合").count()}

    return render(request, "all_activities_v1.html", context=context)


def search_act_view(request):
    q = request.GET.get("q", "")
    if q:
        act = Activity.objects.filter(Q(activity_application__name__icontains=q)
                                      | Q(activity_application__description__icontains=q)
                                      | Q(activity_application__main_club__name__icontains=q)
                                      | Q(activity_application__activity_type__icontains=q))
    act.filter(is_over=False)
    context = {"act": act, 'search': True}
    return render(request, "all_activities_v1.html", context=context)


@login_required(login_url="/login/")
def profile_view(request):
    context = {'user': request.user, "profile": request.profile}

    return render(request, "profile_v1.html", context=context)


@login_required(login_url="/login/")
def change_profile_view(request):
    context = {}
    if request.method == "POST":
        password_1 = request.POST.get("password1", "")
        password_2 = request.POST.get("password2", "")
        username = request.POST.get("username", "")
        if password_1 != password_2:
            context['error_type'] = True
            context['error_message'] = "两次密码不相等，请重新输入！"
            context['message_type'] = "错误："
        else:
            if username:
                request.user.username = username
                user = StudentClubUser.objects.get(phone_number=request.user.phone_number)
                user.set_password(password_1)
                user.save()
            else:
                context['error_type'] = True
                context['error_message'] = "用户名不能为空"
                context['message_type'] = "错误："

        return render(request, "profile_v1.html", context=context)


@login_required(login_url="/login/")
@csrf_exempt
def read_message(request):
    if request.method == "POST":
        message_id = request.POST.get("message_id", "")
        msg = Messages.objects.get(pk=message_id)
        msg.is_read = True
        msg.save()
        return HttpResponse("Read Successful")
