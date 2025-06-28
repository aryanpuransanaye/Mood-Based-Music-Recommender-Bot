from django.urls import path
from .views import RecommendationAPIView


app_name = 'Moodfusion'


urlpatterns = [
    path('recommendation/', RecommendationAPIView.as_view(), name='recommendation'),
    
]