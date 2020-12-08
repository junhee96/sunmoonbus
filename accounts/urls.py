# 2015244044 이준희
# url 경로지정
from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.login,name="login"),
    path('signup/', views.signup,name="signup"),
    path('signout/', views.signout,name="signout"),
    path('confirm/', views.confirm_email, name="confirm_email"),
    path('email_sent/', views.email_sent, name="email_sent"),
]