"""django_project URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from registration.backends.simple.views import RegistrationView

from rango import views


# 定义类,用户成功注册后重定向到首页
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/rango/'


class MyChangePwdView(RegistrationView):
    def change_password(self, user):
        return 'accounts/password/change/'


class MyChangePwdDoneView(RegistrationView):
    def change_password_done(self, user):
        return 'accounts/password/change/done/'


urlpatterns = [
      url(r'^admin/', admin.site.urls),
      url(r'^$', views.index, name='index'),
      url(r'^rango/', include('rango.urls')),
      url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
      url(r'^accounts/change/$', MyChangePwdView.as_view(), name='registration_change'),
      url(r'^accounts/change/done$', MyChangePwdDoneView.as_view(), name='registration_change_done'),
      url(r'^accounts/', include('registration.backends.simple.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
