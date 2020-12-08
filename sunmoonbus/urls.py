"""sunmoonbus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# 2015244044 이준희
# 전체페이지 경로
from django.contrib import admin
from django.urls import path,include
import main.views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.index,name="index"),
    path('index/',include('main.urls')),
    path('board/',include('board.urls')),
    path('accounts/',include('accounts.urls')),
    path('<str:user_id>/reservation/', main.views.busSelect, name="busSelect"),
    path('<str:user_id>/reservation/<int:bus_id>/', main.views.startselect, name='startTime'),
    path('<str:user_id>/reservation/<int:bus_id>/<str:start_id>/', main.views.seatSelect, name='seat'),
    path('<str:user_id>/reservation/<int:bus_id>/<str:start_id>/<int:seat_id>/', main.views.confirm, name='confirm'),
    path('<str:user_id>/myhistory/', main.views.myhistory),
    path('<str:user_id>/cancel/<str:reservation_id>', main.views.cancel),
    path('initial/', main.views.initial),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)