from django.views import View
from django.shortcuts import render,redirect
from datetime import datetime
from .models import Lead, LeadFollowUp, Service, LeadStatus, LeadSource
from .utils import LeadUtils 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.utils.filter import GlobalFilter

global_filter = GlobalFilter()

# Lead Follow Up View 
class LeadFollowUpView(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not global_filter.check_access_filter(request, ['isAdmin', 'isManager', 'isMarketing']):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        lead_follow_ups = LeadFollowUp.objects.all()
        page = request.GET.get('page')
        lead_follow_ups = LeadUtils.paginate_query(lead_follow_ups, page)
        leads= Lead.objects.all()

        context = {
            'lead_follow_ups': lead_follow_ups,
            "leads": leads
        }
        return render(request, 'web/leads/Lead-follow-ups.html', context)

    def post(self, request, *args, **kwargs):
        try:
            follow_up = LeadUtils.get_or_create_lead_follow_up(request.POST)
            message = 'Lead follow-up added successfully'
            messages.success(request, message)
            return redirect('leads:lead_follow_up')
        except Exception as e:
            messages.error(request, str(e))


# Lead View 
class LeadView(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not global_filter.check_access_filter(request, ['isAdmin', 'isManager', 'isMarketing']):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        leads = Lead.objects.all()
        services = Service.objects.all()
        lead_statuses = LeadStatus.objects.all()
        lead_sources = LeadSource.objects.all()

        filter_service = request.GET.get('select_Service', None)
        filter_source = request.GET.get('select_Source', None)
        filter_status = request.GET.get('select_Status', None)
        filter_created_date = request.GET.get('select_date_created', None)
        filter_first_name = request.GET.get('select_FirstName', '')

        if filter_service:
            leads = leads.filter(service_interested__pk=filter_service)
        if filter_source:
            leads = leads.filter(source__pk=filter_source)
        if filter_status:
            leads = leads.filter(status__pk=filter_status)
        if filter_created_date:
            filter_created_date = datetime.strptime(filter_created_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            leads = leads.filter(created_date=filter_created_date)
        if filter_first_name:
            leads = leads.filter(first_name__icontains=filter_first_name)

        page = request.GET.get('page')
        leads = LeadUtils.paginate_query(leads, page)

        context = {
            'leads': leads,
            'services': services,
            'lead_statuses': lead_statuses,
            'lead_sources': lead_sources,
            'filter_service': filter_service,
            'filter_source': filter_source,
            'filter_status': filter_status,
            'filter_created_date': filter_created_date,
            'filter_first_name': filter_first_name,
        }
        return render(request, 'web/leads/leads.html', context)

    def post(self, request, *args, **kwargs):
        try:
            lead = LeadUtils.get_or_create_lead(request.POST)
            message = 'Lead added successfully'
            messages.success(request, message)
            return redirect('leads:lead')
        except Exception as e:
            messages.error(request, str(e))
