"""mediation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from feedback.SMS_соntrol import SMS_valid, Sms_mediation
from feedback.views import home
from django.urls import path, re_path


urlpatterns = [
    path('', home, name='home'),
    # re_path('^smscont/(?P<pk>[0-9]+)/$', SMS_valid.as_view(), name="sms_control")
    path('smscont', SMS_valid.as_view(), name="sms_control"),
    path('smsmediation', Sms_mediation.as_view(), name="sms_media"),
    #path('smsmess', SMS_valid.as_view(), name="sms_control"),

]
