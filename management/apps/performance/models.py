from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


class Performance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Employee'})
    is_productive = models.BooleanField(default=True)
    performance_categories = models.ManyToManyField('PerformanceCategory', related_name='performances')
    rating = models.FloatField()
    progress = models.FloatField()
    comment = RichTextField(blank=True, null=True)
    performance_date = models.DateField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Performance"

    def save(self, *args, **kwargs):
        if not self.pk:
            existing_entry = Performance.objects.filter(user=self.user, performance_date=self.performance_date).first()

            if existing_entry:
                raise ValidationError("On the same day, duplicate user entries are not allowed.")

        super(Performance, self).save(*args, **kwargs)

class PerformanceCategory(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

class PerformanceKeys(models.Model):
    name = models.CharField(max_length=255)
    min_value = models.FloatField()
    max_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PerformanceAppraisal(models.Model):
    name = models.CharField(max_length=255)
    performance_keys = models.ForeignKey(PerformanceKeys, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
