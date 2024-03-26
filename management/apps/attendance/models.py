from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.username} - {self.date}"

class AttendanceEntry(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.attendance.employee.username} - {self.attendance.date} - Entry {self.pk}"

    class Meta:
        unique_together = ('attendance', 'check_in')
