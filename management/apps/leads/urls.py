from django.urls import path
from .views import LeadFollowUpView, LeadView

app_name = 'leads' 

urlpatterns = [
    path('lead-followup/', LeadFollowUpView.as_view(), name='lead_follow_up'),
    path('leads/', LeadView.as_view(), name='lead'),
 
]
