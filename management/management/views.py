from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.utils.common import Common
from .utils import get_user_attendance_context
from apps.assets.utils import ManagementAssets
from apps.leave.utils import LeaveViewTemplate
from apps.utils.filter import GlobalFilter

common = Common() 

lvt = LeaveViewTemplate()
ma = ManagementAssets()
global_filter = GlobalFilter()

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                "status": 200,
                'message': "Login Successful",
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
        else:
            return JsonResponse({
                "status": 400,
                'message': 'Invalid credentials'
            })

@login_required(login_url='login')
def home(request):
    return render(request, 'main/home.html')

@login_required(login_url='login')
def employee(request):
    employee = request.user
    get_user_attendance = get_user_attendance_context(employee)
    leave_summary = lvt.leave_summary(employee)
    user_groups = global_filter.check_access(request)
    other_staff_leave_list = lvt.other_staff_leave_list(employee)
    get_employee_assets= ma.get_employee_assets(request)
    merged_context = get_employee_assets.copy()
    merged_context.update(get_user_attendance)
    merged_context.update(leave_summary)
    merged_context.update(other_staff_leave_list)
    merged_context.update(user_groups)

    return render(request, 'main/employee.html', merged_context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'main/profile.html')

@method_decorator(csrf_exempt, name='dispatch')
class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'main/forgot-password.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            message = 'Invalid username or email'
            messages.error(request, message)

        user.password = make_password(new_password)
        user.save()

        message = 'Password Updated successfully'
        messages.success(request, message)
        return redirect('login')