from django.contrib import admin
from .models import (LeadSource, Service, LeadStatus, CommunicationChannel, Lead, LeadFollowUp)

@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    list_per_page = 10


@admin.register(LeadStatus)
class LeadStatusAdmin(admin.ModelAdmin):
    list_display = ['status']
    search_fields = ['status']
    list_per_page = 10


@admin.register(CommunicationChannel)
class CommunicationChannelAdmin(admin.ModelAdmin):
    list_display = ['channel_name', 'description']
    search_fields = ['channel_name']
    list_per_page = 10


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'company', 'service_interested', 'source', 'status', 'created_date']
    list_filter = ['service_interested', 'source', 'status', 'created_date']
    search_fields = ['first_name', 'last_name', 'email', 'company']
    filter_horizontal = ('preferred_communication_channels',)
    date_hierarchy = 'created_date'
    ordering = ['-created_date']
    list_per_page = 10


@admin.register(LeadFollowUp)
class LeadFollowUpAdmin(admin.ModelAdmin):
    list_display = ['lead', 'date_followed_up']
    list_filter = ['lead', 'date_followed_up']
    search_fields = ['lead__first_name', 'lead__last_name']
    date_hierarchy = 'date_followed_up'
    list_per_page = 10

