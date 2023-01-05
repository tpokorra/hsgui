"""hsgui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from apps.dashboard import views as dashboard_views
from apps.domains import views as domains_views
from apps.wordpress import views as wordpress_views
from apps.nextcloud import views as nextcloud_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard_views.home),
    path('search', dashboard_views.search_command),
    path('wordpress/list', wordpress_views.wordpress_list),
    #path('nextcloud/list', nextcloud_views.nextcloud_list),
]
