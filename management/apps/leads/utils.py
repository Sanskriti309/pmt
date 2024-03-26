# utils.py
from .models import Lead, LeadFollowUp, Service, LeadSource, LeadStatus
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from datetime import datetime

class LeadUtils:
    @staticmethod
    def paginate_query(queryset, page, per_page=10):
        paginator = Paginator(queryset, per_page)
        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)

    @staticmethod
    def get_or_create_lead(data):
        lead_id = data.get('lead_id')
        service_interested = get_object_or_404(Service, pk=data.get('service_interested'))
        source = get_object_or_404(LeadSource, pk=data.get('source'))
        status = get_object_or_404(LeadStatus, pk=data.get('status'))

        created_date_str = data.get('created_date')
        created_date = datetime.strptime(created_date_str, '%d-%m-%Y')

        lead, created = Lead.objects.update_or_create(
            id=lead_id,
            defaults={
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'company': data.get('company'),
                'website': data.get('website'),
                'position': data.get('position'),
                'created_date': created_date,
                'service_interested': service_interested,
                'source': source,
                'status': status,
                'notes': data.get('notes')
            }
        )
        return lead

    @staticmethod
    def get_or_create_lead_follow_up(data):
        follow_up_id = data.get('follow_up_id')
        lead = get_object_or_404(Lead, pk=data.get('lead_id'))

        date_followed_up_str =data.get('date_followed_up')
        date_followed_up = datetime.strptime(date_followed_up_str, '%d-%m-%Y')

        follow_up, created = LeadFollowUp.objects.update_or_create(
            id=follow_up_id,
            defaults={
                'lead': lead,
                'date_followed_up': date_followed_up,
                'notes': data.get('notes')
            }
        )
        return follow_up
