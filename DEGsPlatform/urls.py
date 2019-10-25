"""DEGsPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path
from django.contrib import admin
from django.conf.urls import url
from . import view

urlpatterns = [
    path("home/",view.home),
    url(r'^$',view.home),
    path('admin/', admin.site.urls),
    url(r'^upload$',view.upload_csv),
    url(r'^check_column$',view.check_column),
    url(r'^cal_degs$',view.cal_degs),
    url(r'^download$',view.download_file)
]
