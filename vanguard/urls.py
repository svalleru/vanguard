"""vanguard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from vanguard import users

urlpatterns = [
    url(r'^/?$', users.user_signup),
    url(r'^/signup/?$', users.user_signup),
    url(r'^/login/?$', users.user_login),
    url(r'^/forgotpassword/?$', users.forgot_password),
    url(r'^/logout/?$', users.user_logout),
]
