from django.shortcuts import render,redirect
from django.views import View
from .models import Performance,PerformanceCategory
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from django import template
from apps.utils.filter import GlobalFilter
from django.contrib.auth.models import User, Group
from .utils import performanceUtils
from django.contrib import messages

global_filter = GlobalFilter()

register = template.Library()
@register.filter
def get_value(obj, attr_name):
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None


# Perfonmance View
class PerformanceView(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if global_filter.check_access_filter(request, ['isStudent']):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        
        today = timezone.now().date()

        date_ranges = {
            'last7days': today - timedelta(days=7),
            'last15days': today - timedelta(days=15),
            'last1month': today - timedelta(days=30),
            'last2months': today - timedelta(days=60),
            'lastyear': today - timedelta(days=365),
        }

        filter_option = request.GET.get('filter', None)

        performances = Performance.objects.all()
        employees = User.objects.filter(groups__name='Employee')
        performance_category = PerformanceCategory.objects.all()
        column_names = []
        
        if filter_option in date_ranges:
            performances = performances.filter(performance_date__gte=date_ranges[filter_option])

        isAdmin = global_filter.check_access_filter(request, ["isAdmin","isManager"])
        isMarketing = global_filter.check_access_filter(request, ["isMarketing"])
        is_employee = global_filter.check_access_filter(request, ["isEmployee"])

        if isAdmin or isMarketing:
            pass
        elif is_employee:
            performances = performances.filter(user=request.user)
            column_names = [field for field in Performance._meta.get_fields() if field.name != 'user']
        else:
            raise PermissionDenied()

        if not column_names:
            column_names = Performance._meta.get_fields()

        return render(request, 'web/performance/performance.html', {
            'performances': performances,
            'performance_category': performance_category,
            'column_names': column_names,
            'current_filter': filter_option,
            'is_manager': isAdmin,
            'is_marketing': isMarketing,
            'employees': employees,
        })

    def post(self, request, *args, **kwargs):
        try:
            performance = performanceUtils.get_or_create_performance(request.POST)
            message = 'Performance added successfully'
            messages.success(request, message)
            return redirect('performance:performance')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('performance:performance')