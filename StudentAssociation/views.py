import random

from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache

from .utils import message_service
from accounts.models.studentclub_user import StudentClubUser
from accounts.models.user_profile import ClubUserProfile


def main_view(request):

    return render(request, "index_v1.html")


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login_v1.html")

    context = {"error": False, "error_message": "", "phone_number": ""}

    if request.method == "POST":
        phone = request.POST["phone"]
        password = request.POST["Password"]
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            context["error"] = True
            try:
                StudentClubUser.objects.get(phone_number=phone, is_active=True)
                context["error_message"] = "你输入的账号或密码错误，请确认大小写"
                context["phone_number"] = phone
            except StudentClubUser.DoesNotExist:
                context["error_message"] = "改账号不存在，请先注册"
                user_profile = ClubUserProfile.objects.filter(phone_number=phone, is_active=True)
                if user_profile:
                    context["error_message"] = "您已是社团会员，请绑定您在社团报名时预留的手机号"

            return render(request, "login_v1.html", context=context)


@login_required
def logout_view(request):
    logout(request)
    # TODO user is not login
    return HttpResponseRedirect(reverse("index"))


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
            context["error_message"] = "该账号已存在，请登录"
            context['phone'] = phone_number
            return render(request, "login_v1.html", context=context)

        except StudentClubUser.DoesNotExist:
            cache_code = cache.get("phone_number")
            if cache_code != validate_code:
                context["error"] = True
                context["error_message"] = "验证码错误，请重新尝试"

            if password1 and password2 and password1 != password2:
                context["error"] = True
                context["error_message"] = "两次密码不相等，请重新输入"
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
                return HttpResponseRedirect(reverse("index"))


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
                context['error_message'] = "验证码错误"

            context["validate_code"] = validate_code

            if password1 and password2 and password1 != password2:
                context["error"] = True
                context["error_message"] = "两次密码不相等，请重新输入"
                context["phone_number"] = phone_number
                return render(request, "register_v1.html", context=context)

            user.set_password(password1)
            user.save()
            context['error_message'] = "请重新登陆"
            return HttpResponseRedirect(reverse("login"))

        except StudentClubUser.DoesNotExist:
            context["error"] = True
            context['error_message'] = "该手机号尚未注册，请先注册"
            return render(request, "forget_password.html", context=context)
    else:
        return render(request, "forget_password.html")


def join_club_view(request):
    return render(request, "join_club_v1.html")


@csrf_exempt
def send_msg(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    random_code = random.randint(100000, 999999)
    phone_number = request.POST['phone_number']
    print("The random_code is: " + str(random_code))

    msg_status = message_service(phone_number, random_code)
    if not msg_status:
        message_service(phone_number, random_code)
    else:
        cache.set(phone_number, random_code, 300)

    return HttpResponse("message success")
