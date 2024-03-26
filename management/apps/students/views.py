from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Enquiry,Course,Admission,FeeManagement
from django.db.models import Sum, Max
from apps.utils.filter import GlobalFilter
from .utils import FeeManagementUtils, EnquiryUtils, AdmissionUtils

global_filter = GlobalFilter()

# Create your views here.

# Admission
class AdmissionView(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not global_filter.check_access_filter(request, ['isAdmin', 'isManager', 'isMarketing']):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    template_name = 'web/students/admission.html'

    def get(self, request, *args, **kwargs):
        page_type = request.GET.get('type', 'admission')

        enquiry = Enquiry.objects.all()

        enquiry_admission = Enquiry.objects.filter(admission__isnull=False).distinct()

        admissions = AdmissionUtils.get_filtered_admissions(request)

        admissions = AdmissionUtils.paginate_admissions(request, admissions)

        context = AdmissionUtils.get_admission_context(enquiry, enquiry_admission, admissions, page_type, request.GET.get('date_range'), request.GET.get('select_student'))

        if page_type == 'admission-list':
            self.template_name = 'web/students/admission-list.html'

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return AdmissionUtils.handle_admission_post_request(request)


# Enquiry View 
class EnquiryView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not global_filter.check_access_filter(request, ['isAdmin', 'isManager', 'isMarketing']):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    template_name = 'web/students/enquiry.html'

    def get(self, request, *args, **kwargs):
        page_type = request.GET.get('type', 'enquiry')

        enquiry = EnquiryUtils.get_filtered_enquiries(request)
        all_enquiry = Enquiry.objects.all()
        courses = Course.objects.all()

        enquiry = EnquiryUtils.paginate_enquiries(request, enquiry)

        context = EnquiryUtils.get_enquiry_context(enquiry, all_enquiry, courses, page_type, request.GET.get('select_course'))

        if page_type == 'enquiry-list':
            self.template_name = 'web/students/enquiry-list.html'

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return EnquiryUtils.handle_enquiry_post_request(request)

   
# Fee Management
class FeeManagementView(View):

    fee_management_utils = FeeManagementUtils()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not global_filter.check_access_filter(request, ['isAdmin', 'isManager', 'isMarketing']):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        

        admissions = Admission.objects.all()

        fee_management_aggregated = (
            FeeManagement.objects.values('admission')
            .annotate(
                latest_fee_paid_date=Max('fee_paid_date'),
                total_paid_fee=Sum('paid_fee'),
                latest_created_date=Max('created_date'),
            )
        )

        admissions_with_fee = []
        for item in fee_management_aggregated:
            admission_id = item['admission']
            admission = Admission.objects.get(pk=admission_id)
            total_due = admission.fee_entries.last().total_due

            fee_entries = FeeManagement.objects.filter(admission=admission).values('paid_fee', 'fee_paid_date')

            fee_entries_list = [
                {
                    'paid_fee': str(entry['paid_fee']),
                    'fee_paid_date': entry['fee_paid_date'].strftime('%Y-%m-%d'),
                } for entry in fee_entries
            ]

            admissions_with_fee.append({
                'admission': admission,
                'latest_fee_paid_date': item['latest_fee_paid_date'],
                'total_paid_fee': item['total_paid_fee'],
                'latest_created_date': item['latest_created_date'],
                'total_due': total_due,
                'fee_entries': fee_entries_list,
            })

        filter_option = request.GET.get('filter_option', 'active')
        admissions_with_fee_filtered = self.fee_management_utils.get_filtered_admissions(filter_option, admissions_with_fee)

        if filter_option in ['active', 'inactive']:
            total_users_count = admissions.count()
            active_users, inactive_users = self.fee_management_utils.get_active_inactive_counts(filter_option, admissions)
        else:
            active_users = sum(1 for entry in admissions_with_fee_filtered if entry['admission'].is_active)
            inactive_users = total_users_count - active_users

        if filter_option in ['active', 'inactive']:
            admissions_with_fee_filtered = self.fee_management_utils.get_filtered_admissions(filter_option,admissions_with_fee_filtered)

        selected_admission_id = request.GET.get('admission_filter')

        if selected_admission_id:
            admissions_with_fee_filtered = [entry for entry in admissions_with_fee_filtered if entry['admission'].id == int(selected_admission_id)]
            admission = Admission.objects.get(pk=selected_admission_id)
            total_due = admission.fee_entries.last().total_due

            fee_entries = FeeManagement.objects.filter(admission=admission).values('paid_fee', 'fee_paid_date')

            fee_entries_list = [
                {
                    'paid_fee': str(entry['paid_fee']),
                    'fee_paid_date': entry['fee_paid_date'].strftime('%Y-%m-%d'),
                } for entry in fee_entries
            ]

            admissions_with_fee = [{
                'admission': admission,
                'latest_fee_paid_date': admission.fee_entries.last().fee_paid_date,
                'total_paid_fee': sum(entry['paid_fee'] for entry in fee_entries),
                'latest_created_date': admission.fee_entries.last().created_date,
                'total_due': total_due,
                'fee_entries': fee_entries_list,
            }]

            active_users = 1 if admission.is_active else 0
            inactive_users = 0 if admission.is_active else 1

        page = request.GET.get('page', 1)
        admissions_with_fee_paginated = self.fee_management_utils.get_paginated_admissions(admissions_with_fee_filtered,page)

        context = self.fee_management_utils.get_admission_context(admissions, admissions_with_fee_paginated,filter_option, selected_admission_id)
        return render(request, 'web/students/fee-management.html', context)

    def post(self, request, *args, **kwargs):
        return FeeManagementUtils.post_fee_management_context(request)
