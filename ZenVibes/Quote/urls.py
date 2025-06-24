from django.urls import path
from .views import QuoteViewSet

app_name = 'Quote'

urlpatterns = [
    path('random-quote/', QuoteViewSet.as_view(), name='random-quote')
]