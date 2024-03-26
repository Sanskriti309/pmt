from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Manage Assets Model

class ManageAsset(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('regular', 'Regular')
    ]
    ASSETS_TYPE_CHOICES = [
        ('accessories', 'Accessories'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='assets/', max_length=255, null=True)
    condition_type = models.CharField(max_length=100, choices=CONDITION_CHOICES, default=None, null=True)
    assets_type = models.CharField(max_length=100, choices=ASSETS_TYPE_CHOICES, default=None, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    assigned_Id = models.CharField(max_length=10, null=True, blank=True)
    serial_number = models.CharField(max_length=32, null=True, blank=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assets_assigned_to')
    assigned_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assets_assigned_by')
    assigned_date = models.DateField(default=timezone.now,  null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name


