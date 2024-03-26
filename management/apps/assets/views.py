from django.shortcuts import render,redirect
from django.views import View
from .utils import ManagementAssets
from apps.utils.filter import GlobalFilter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

ma = ManagementAssets()

global_filter = GlobalFilter()

class ManageAssetView(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if global_filter.check_access_filter(request, ['isStudent']):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request):
        if global_filter.check_access_filter(request, ["isAdmin", "isManager"]):
            context = ma.get_all_assets(request)
        else:
            context = ma.get_employee_assets(request)

        return render(request, 'web/assets/Manage-Assets.html', context)
