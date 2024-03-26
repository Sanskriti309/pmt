from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.conf import settings

class Course(models.Model):
    DURATION_CHOICES = [
        ('3m', '3 months'),
        ('6m', '6 months'),
        ('9m', '9 months'),
        ('12m', '12 months')
    ]

    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=4, choices=DURATION_CHOICES)
    description = RichTextField(blank=True, null=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fee = models.IntegerField(default=None)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Enquiry(models.Model):
    def clean(self):
        if self.dob >= date.today():
            raise ValidationError({
                'dob': 'Date of Birth cannot be today or in the future.'
            })
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    contact_no = models.CharField(max_length=10)
    whatsapp_no = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    course_interested = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="enquiries")
    discounted_fee = models.IntegerField(default=None, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    enquiry_date = models.DateField(default=None)
    coming_date = models.DateField(default=None, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Admission(models.Model):
    enquiry = models.OneToOneField(Enquiry, on_delete=models.CASCADE, related_name="admission")
    admission_date = models.DateField(auto_now_add=True)
    admission_fee = models.IntegerField()
    student_photo = models.FileField(upload_to='students_photos/', null=True, blank=True)
    qualification_docs = models.FileField(upload_to='qualification_docs/', null=True, blank=True)
    ADDRESS_DOC_CHOICES = [
        ('aadhaar', 'Aadhaar Card'),
        ('voter', 'Voter ID Card'),
        ('others', 'Others')
    ]
    address_doc_type = models.CharField(max_length=32, choices=ADDRESS_DOC_CHOICES, default='aadhaar')
    address_docs = models.FileField(upload_to='address_docs/', null=True, blank=True)
    admission_date = models.DateField(default=None)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.enquiry.name} - {self.enquiry.course_interested.name}"


class FeeManagement(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name="fee_entries")
    paid_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee_paid_date = models.DateField(default=timezone.now)
    created_date = models.DateField(auto_now_add=True)

    @property
    def total_due(self):
        admission_fee = self.admission.admission_fee if (self.admission and self.admission.admission_fee is not None) else 0
        Course_Fee = self.admission.enquiry.discounted_fee if (self.admission and self.admission.enquiry and self.admission.enquiry.discounted_fee is not None) else self.admission.enquiry.course_interested.fee
        total_paid = sum(entry.paid_fee for entry in self.admission.fee_entries.all())
        return (admission_fee + Course_Fee) - total_paid 

    def clean(self, *args, **kwargs):
        if self.paid_fee > self.total_due:
            raise ValidationError("Paid amount exceeds the due amount "+ str(self.total_due) +" .")
        super(FeeManagement, self).save(*args, **kwargs)

    def __str__(self):
        return f"Fee Entry for {self.admission.enquiry.name} on {self.fee_paid_date}"
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



