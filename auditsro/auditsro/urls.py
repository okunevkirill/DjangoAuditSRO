"""auditsro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from authapp.views import CustomUserViewSet
from mainapp.views import CompanyViewSet, OrganizationViewSet, WatchlistViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'watchlists', WatchlistViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('rest_framework.urls')),
    re_path('^api/', include(router.urls)),
]
