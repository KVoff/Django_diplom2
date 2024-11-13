from django.urls import path

from .views import profile

app_name = 'profile'

urlpatterns = [
    path('', profile, name='profile'),


]
