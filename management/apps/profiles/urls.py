from django.urls import path
from .views import ProfileView,UpdateProfileView,UpdatePersonalInfoView,UpdateBankView,UpdateFamilyView,UpdateEducationView,UpdateExperienceView,UpdateEmergencyContactView


urlpatterns = [
    path('', ProfileView.as_view(),name='profile'),
    path('update-profile/', UpdateProfileView.as_view(),name='update_profile'),
    path('update-personal-info/', UpdatePersonalInfoView.as_view(),name='update_personal_info'),
    path('update-bank-info/', UpdateBankView.as_view(),name='update_bank'),
    path('update-family-info/', UpdateFamilyView.as_view(),name='update_family_info'),
    path('update-education-info/', UpdateEducationView.as_view(),name='update_education_info'),
    path('update-experience-info/', UpdateExperienceView.as_view(),name='update_experience_info'),
    path('update-emergency-contact/', UpdateEmergencyContactView.as_view(),name='update_emergency_contact'),
]

