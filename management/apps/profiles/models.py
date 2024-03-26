from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class JobSkill(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Skill Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Job Skill'
        verbose_name_plural = 'Job Skills'


class JobProfile(models.Model):
    title = models.CharField(max_length=255, verbose_name='Job Title')
    description = RichTextField(blank=True, null=True, verbose_name='Job Description')
    responsibilities = RichTextField(blank=True, null=True, verbose_name='Responsibilities')
    qualifications = RichTextField(blank=True, null=True, verbose_name='Qualifications')
    experience_required = models.PositiveIntegerField(verbose_name='Experience Required (in years)')
    skills_required = models.ManyToManyField(JobSkill, related_name='job_profiles', verbose_name='Skills Required')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated At')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Job Profile'
        verbose_name_plural = 'Job Profiles'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    report_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_to')
    dob = models.DateField(null=True, blank=True)
    doj = models.DateField(null=True, blank=True)
    job_profile = models.OneToOneField(JobProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    address = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], blank=True, null=True)
    no_of_children = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class Bank(models.Model):
    """
    Bank Model: Represents the bank account details of a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    """
    The User model instance associated with the bank account.
    """
    name = models.CharField(max_length=100)
    """
    The name of the bank.
    """
    account = models.CharField(max_length=20)
    """
    The bank account number.
    """
    ifsc = models.CharField(max_length=20)
    """
    The IFSC code of the bank.
    """
    pan = models.CharField(max_length=10, null=True, blank=True)
    """
    The PAN number of the user.
    """
    def __str__(self):
        """
        Return a string representation of the Bank instance.
        """
        return f"{self.user.username}'s Bank Account"
    
class EmergencyContact(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    contact_type = models.CharField(max_length=20, choices=[('Primary', 'Primary'), ('Secondary', 'Secondary')])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.profile.username}'s {self.contact_type} Emergency Contact"

class FamilyInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}'s {self.relation}"
    
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=100)
    stream = models.CharField(max_length=50)
    job_position = models.CharField(max_length=120, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    from_year = models.PositiveIntegerField()
    to_year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Education at {self.college}, {self.stream}"
    
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Experience at {self.company}"