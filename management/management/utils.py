from django.conf import settings
from django.utils import timezone
from apps.attendance.models import AttendanceEntry
from apps.utils.common import Common

common = Common() 

def get_user_attendance_context(user):
    current_date = timezone.now().date()

    attendance_entries = AttendanceEntry.objects.filter(
        attendance__employee=user,
        attendance__date=current_date
    ).order_by('check_in')
    activity_list = []
    for entry in attendance_entries:
        activity_list.append("Punch In Time: " + common.format_time(entry.check_in))
        if entry.check_out:
            activity_list.append("Punch Out Time: " + common.format_time(entry.check_out))

    context = {
        'activity_list': activity_list,
    }

    return context
