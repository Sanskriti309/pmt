from django.urls import path
from .views import AdmissionView,EnquiryView,FeeManagementView

app_name = 'students' 

urlpatterns = [
    path('admissions/', AdmissionView.as_view(), name='admission'),
    path('enquiry/', EnquiryView.as_view(), name='enquiry'),
    path('fee-management/', FeeManagementView.as_view(), name='fee_management'),
]
