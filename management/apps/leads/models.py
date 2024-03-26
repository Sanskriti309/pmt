from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User

class LeadSource(models.Model):
    """
    Model to track the source of the leads (e.g. Referral, Website, Social Media)
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Service(models.Model):
    """
    Different services provided by the IT company (e.g. Web Development, Mobile App, SEO)
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class LeadStatus(models.Model):
    """
    Model to represent different statuses a lead can have.
    """
    status = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.status

class CommunicationChannel(models.Model):
    channel_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.channel_name
    
class Lead(models.Model):
    """
    Main model to manage leads
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    preferred_communication_channels = models.ManyToManyField(CommunicationChannel, blank=True, related_name="leads")
    website = models.URLField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    service_interested = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name="leads")
    source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, related_name="leads")
    status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True, related_name="leads")
    notes = RichTextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email} -{self.phone}"

class LeadFollowUp(models.Model):
    """
    Model to track follow-ups with leads
    """
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="followups")
    date_followed_up = models.DateTimeField(default=timezone.now)
    notes = RichTextField(blank=True, null=True)

    def __str__(self):
        return f"Follow-up for {self.lead} on {self.date_followed_up}"