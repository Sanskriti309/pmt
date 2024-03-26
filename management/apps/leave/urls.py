from django.urls import path
from .views import LeaveBalanceView, LeaveView

app_name = 'leave' 

urlpatterns = [
    path('leave-balances/', LeaveBalanceView.as_view(), name='leave_balance'),
    path('leaves/', LeaveView.as_view(), name='leave'),
]
