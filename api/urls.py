from django.urls import path

from api.apps import ApiConfig
from api.views import login, check_login, messages, wild

app_name = ApiConfig.name

urlpatterns = [
    path('login/', login, name='login'),
    path('check/login/', check_login, name='check_login'),
    path('messages/', messages, name='messages'),
    path('wild/', wild, name='wild'),
]
