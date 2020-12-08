# 2015244044 이준희

from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .email_confirmation import generate_random_string



# 로그인
def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    elif request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    return redirect('index')

#회원가입
def signup(request):
    sun = "@sunmoon.ac.kr"
    if request.method=="GET":
        return render(request, "signup.html")
    elif request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        pwcheck = request.POST["pwcheck"]
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = username + sun
        if password != pwcheck:
            return render(request, "signup.html",{"pw_msg":"비밀번호가 일치하지 않습니다"})
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"email_overlap":"이미 가입된 이메일 입니다"})
        user = User.objects.create_user(username=username, password=password, name=name, phone=phone, email=email)
        user.save()        
        auth.login(request, user)
        # return login_next(request, user)
    return redirect('index')

#로그아웃
def signout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')

#이메일 인증이되면 로그인
def login_next(request, user):
    if EmailConfirm.objects.filter(user=user, is_confirmed=True).exists():
        auth.login(request, user)
        return redirect('index')
    else:
        send_confirm_mail(user)
        return redirect('email_sent')

#해당 이메일에 인증 보내기
def send_confirm_mail(user):
    try:
        email_confirm = EmailConfirm.objects.get(user=user)
    except EmailConfirm.DoesNotExist:
        email_confirm = EmailConfirm.objects.create(
            user = user,
            key = generate_random_string(length=30),
        )
    url = '{0}{1}?key={2}'.format(
        'http://localhost:8000',
        reverse('confirm_email'),
        email_confirm.key,
    )
    html = '<p>선문대학교 셔틀버스 이메일인증입니다 계속하시려면 아래 링크를 눌러주세요.</p><a href="{0}">인증하기</a>'.format(url)
    send_mail(
        '인증 메일입니다.',
        '',
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=html,
    )

#인증 이메일을 클릭하면 가입할 수 있다.
def confirm_email(request):
    key = request.GET.get('key')
    try:
        email_confirm = get_object_or_404(EmailConfirm, key=key, is_confirmed=False)
        email_confirm.is_confirmed = True
        email_confirm.save()
        return redirect('login')
    except:
        return render(request, 'login.html')

#이메일 보내지고 난 화면
def email_sent(request):
    return render(request, "email_sent.html")