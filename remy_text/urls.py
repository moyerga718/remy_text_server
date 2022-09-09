"""remy_text URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from remy_text_api.views import login_user, register_user
from remy_text_api.views import GameFlagView
from remy_text_api.views import GameView
from remy_text_api.views import ItemView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'game_flags', GameFlagView, 'game_flag')
router.register(r'games', GameView, 'game')
router.register(r'items', ItemView, 'item')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls))
]
