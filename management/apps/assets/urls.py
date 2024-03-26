from django.urls import path
from .views import ManageAssetView

app_name = 'assets' 

urlpatterns = [
    path('manage-assets/', ManageAssetView.as_view(), name='manage_assets'),
]
