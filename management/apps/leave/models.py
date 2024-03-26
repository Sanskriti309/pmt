from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField

# Create your models here.

class LeaveCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_leaves = models.FloatField()

    def __str__(self):
        return self.name

class Type(models.Model):
    type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type


class LeaveBalence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Employee'})
    leave_category = models.ForeignKey(LeaveCategory, on_delete=models.SET_NULL, null=True, blank=True)
    leave_balance = models.FloatField(default=0)

    class Meta:
        unique_together = ['user', 'leave_category']

    def __str__(self):
        return f"{self.user.username}"

    
class LeaveStatus(models.Model):
    """
    Model to represent different statuses a Leave can have.
    """
    status = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.status

class Leave(models.Model):
    employee = models.ForeignKey(LeaveBalence, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveCategory, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT, null=True)
    start_date = models.DateField()
    is_start_date_half_day = models.BooleanField(default=False)
    end_date = models.DateField()
    is_end_date_half_day = models.BooleanField(default=False)
    reason = models.TextField()
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    requested_date= models.DateTimeField(default=timezone.now, null=True)
    status = models.ForeignKey(LeaveStatus, on_delete=models.CASCADE)
    notes= RichTextField(blank=True, null=True)

    @property
    def total_days(self):

        if self.start_date == self.end_date:

            if self.is_start_date_half_day or self.is_end_date_half_day:
                total_days = 0.5
            else:
                total_days = (self.end_date - self.start_date).days + 1

        elif self.start_date != self.end_date:
            
            if self.is_start_date_half_day and self.is_end_date_half_day:
                total_days = (self.end_date - self.start_date).days
            elif self.is_start_date_half_day or self.is_end_date_half_day:
                total_days = (self.end_date - self.start_date).days + 0.5
            else:
                total_days = (self.end_date - self.start_date).days + 1
    
        return total_days

    def clean(self, *args, **kwargs):
        if self.total_days > self.employee.leave_balance:
                raise ValidationError("Leave request exceeds available leave balance.")
        else:
            if self.status.status=="Approved":
                self.employee.leave_balance -= self.total_days
                self.employee.save()           

        super(Leave, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.user.username} - {self.leave_type}"