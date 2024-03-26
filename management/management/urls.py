from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView,employee,login_view,logout_view,ForgotPasswordView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',employee,name='dashboard'),
    path('login/',login_view,name='login'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('students/', include('apps.students.urls')),
    path('leave/', include('apps.leave.urls')),
    path('leads/', include('apps.leads.urls')),
    path('performance/', include('apps.performance.urls')),
    path('profile/', include('apps.profiles.urls')),
    path('assets/', include('apps.assets.urls')),
    path('user/logout/', logout_view, name='logout'),
    path('forgot-password/',ForgotPasswordView.as_view(),name='forgot_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)