from django.contrib import admin
from .models import LeaveBalence, Leave, LeaveCategory, Type, LeaveStatus

@admin.register(LeaveCategory)
class LeaveCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_leaves')
    search_fields = ('name',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('name',)

@admin.register(LeaveBalence)
class LeaveBalenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_balance', 'leave_category')
    search_fields = ('user__username',)
    list_filter = ('leave_category',) 

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    search_fields = ('employee__user__username', 'leave_type__name', 'status')
    list_filter = ('leave_type', 'status')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if request.user.groups.filter(name='Instructors').exists():
            readonly_fields += ('status',)
        return readonly_fields

@admin.register(LeaveStatus)
class LeaveStatusAdmin(admin.ModelAdmin):
    list_display = ['status']
    search_fields = ['status']
    list_per_page = 10