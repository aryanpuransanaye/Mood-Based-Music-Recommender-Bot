from django.urls import path
from .views import UserMoodView

app_name = 'Users'

urlpatterns = [
    path('users-mood/', UserMoodView.as_view(), name='usermood')
]