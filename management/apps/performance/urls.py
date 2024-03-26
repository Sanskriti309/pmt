from django.urls import path
from .views import PerformanceView

app_name = 'performance' 

urlpatterns = [
    path('performance/', PerformanceView.as_view(), name='performance'),   
]
