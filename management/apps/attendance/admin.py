from django.contrib import admin
from .models import Attendance, AttendanceEntry

class AttendanceEntryInline(admin.StackedInline):
    model = AttendanceEntry
    extra = 1

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'is_present')
    inlines = [AttendanceEntryInline]

class AttendanceEntryAdmin(admin.ModelAdmin):
    list_display = ('attendance', 'check_in', 'check_out')
    list_filter = ('attendance__employee', 'attendance__date')

admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(AttendanceEntry, AttendanceEntryAdmin)