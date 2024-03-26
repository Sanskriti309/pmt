from .models import FeeManagement, Admission, Enquiry,Course
from django.db.models import Sum
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404,redirect
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
 

# Fee Management Utils
class FeeManagementUtils:
    def get_filtered_admissions(self, filter_option, admissions_with_fee):
        if filter_option == 'active':
            return [entry for entry in admissions_with_fee if entry['admission'].is_active]
        elif filter_option == 'inactive':
            return [entry for entry in admissions_with_fee if not entry['admission'].is_active]
        else:
            return admissions_with_fee

    def get_paginated_admissions(self, admissions_with_fee_filtered, page):
        paginator = Paginator(admissions_with_fee_filtered, 10)
        try:
            admissions_with_fee_paginated = paginator.page(page)
        except PageNotAnInteger:
            admissions_with_fee_paginated = paginator.page(1)
        except EmptyPage:
            admissions_with_fee_paginated = paginator.page(paginator.num_pages)
        return admissions_with_fee_paginated

    def calculate_summary_statistics(self, admissions_with_fee):
        total_users_count = len(admissions_with_fee)
        total_user = len(Admission.objects.all())
        total_amount_paid = sum(entry['total_paid_fee'] for entry in admissions_with_fee)
        total_due_amount = sum(entry['total_due'] for entry in admissions_with_fee)
        active_users = sum(1 for entry in admissions_with_fee if entry['admission'].is_active)
        inactive_users = total_users_count - active_users
        total_fee = total_amount_paid + total_due_amount
        total_active_percentage = (active_users / total_user) * 100 if total_user > 0 else 0
        total_inactive_percentage = (inactive_users / total_user) * 100 if total_user > 0 else 0

        try:
            paid_percentage = int((total_amount_paid / total_fee) * 100)
            due_percentage = int((total_due_amount / total_fee) * 100)
        except ZeroDivisionError:
            paid_percentage = 0
            due_percentage = 0

        return {
            'total_amount_paid': total_amount_paid,
            'total_due_amount': total_due_amount,
            'active_users_count': active_users,
            'inactive_users_count': inactive_users,
            'total_active_percentage': total_active_percentage,
            'total_inactive_percentage': total_inactive_percentage,
            'paid_percentage': paid_percentage,
            'due_percentage': due_percentage,
        }

    def get_admission_context(self, admissions, admissions_with_fee_paginated, filter_option, selected_admission_id):
        return {
            'admissions': admissions,
            'admissions_with_fee': admissions_with_fee_paginated,
            'filter_option': filter_option,
            'selected_admission': selected_admission_id,
            **self.calculate_summary_statistics(admissions_with_fee_paginated.object_list),
        }

    def get_active_inactive_counts(self, filter_option, admissions):
        total_users = admissions.count()
        active_users = admissions.filter(is_active=True).count()
        inactive_users = total_users - active_users

        if filter_option == 'active':
            return active_users, inactive_users
        elif filter_option == 'inactive':
            return inactive_users, active_users
        else:
            return active_users, inactive_users

    def post_fee_management_context(request):
        try:
            admission_id = request.POST.get('admission')
            data = {field: request.POST.get(field) for field in ['paid_fee', 'fee_paid_date']}
            data['fee_paid_date'] = datetime.strptime(data['fee_paid_date'], '%d-%m-%Y').date()

            admission_obj = get_object_or_404(Admission, pk=admission_id)
            total_due = admission_obj.fee_entries.last().total_due

            if float(data['paid_fee']) > float(total_due):
                raise ValidationError("Paid amount exceeds the due amount " + str(total_due) + ".")

            FeeManagement.objects.create(admission=admission_obj, **data)
            message = 'Fee Added Successfully'

            messages.success(request, message)
            return redirect('students:fee_management')

        except ValidationError as ve:
            messages.error(request, str(ve))
        except Exception as e:
            messages.error(request, str(e))


# Enquiry Utils 
class EnquiryUtils:
    def get_filtered_enquiries(request):
        select_student = request.GET.get('select_student')
        select_course = request.GET.get('select_course')

        enquiry = Enquiry.objects.all()

        if select_student:
            enquiry = enquiry.filter(id=select_student)

        if select_course:
            enquiry = enquiry.filter(course_interested__id=select_course)

        return enquiry

    def paginate_enquiries(request, enquiry):
        from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

        paginator = Paginator(enquiry, 12)
        page = request.GET.get('page', 1)

        try:
            enquiry = paginator.page(page)
        except PageNotAnInteger:
            enquiry = paginator.page(1)
        except EmptyPage:
            enquiry = paginator.page(paginator.num_pages)

        return enquiry

    def get_enquiry_context(enquiry, all_enquiry, courses, page_type, select_course):
        context = {
            'enquiry': enquiry,
            'all_enquiry': all_enquiry,
            'courses': courses,
            'enquiry_list_path': reverse('students:enquiry') + '?type=enquiry-list',
            'page_type': page_type,
            'select_course': select_course,
        }

        return context

    def handle_enquiry_post_request(request):
        try:
            enquiry_id = request.POST.get('enquiry_id')
            data = {field: request.POST.get(field) for field in [
                'name', 'father_name', 'mother_name', 'email', 'contact_no', 'dob', 'gender', 'address',
                'pincode', 'whatsapp_no', 'course_interested', 'discounted_fee', 'education', 'enquiry_date'
            ]}

            data['discounted_fee'] = int(data['discounted_fee']) if data['discounted_fee'] and data['discounted_fee'] != 'None' else None
            data['dob'] = datetime.strptime(data['dob'], '%d-%m-%Y').strftime('%Y-%m-%d')
            data['enquiry_date'] = datetime.strptime(data['enquiry_date'], '%d-%m-%Y').strftime('%Y-%m-%d')

            course_obj = get_object_or_404(Course, pk=data['course_interested'])
            enquiry_data = {**data, 'course_interested': course_obj}

            if enquiry_id:
                enquiry = get_object_or_404(Enquiry, pk=enquiry_id)
                for key, value in enquiry_data.items():
                    setattr(enquiry, key, value)
                enquiry.save()
                message = 'Enquiry Updated Successfully'
            else:
                enquiry = Enquiry.objects.create(**enquiry_data)
                message = 'Enquiry Added Successfully'

            messages.success(request, message)
            return redirect('students:enquiry')

        except Exception as e:
            messages.error(request, str(e))


# Admission Utils 
class AdmissionUtils:
    def get_filtered_admissions(request):
        date_range = request.GET.get('date_range')
        select_student = request.GET.get('select_student')

        admissions = Admission.objects.all()

        if date_range:
            filter_range = timezone.now() - timedelta(days=int(date_range))
            admissions = Admission.objects.filter(admission_date__range=[filter_range, timezone.now()])

        if select_student:
            admissions = admissions.filter(enquiry__id__exact=select_student)

        return admissions

    def paginate_admissions(request, admissions):
        paginator = Paginator(admissions, 12)
        page = request.GET.get('page', 1)

        try:
            admissions = paginator.page(page)
        except PageNotAnInteger:
            admissions = paginator.page(1)
        except EmptyPage:
            admissions = paginator.page(paginator.num_pages)

        return admissions

    def get_admission_context(enquiry, enquiry_admission, admissions, page_type, date_range, select_student):
        context = {
            'enquiry': enquiry,
            'enquiry_admission': enquiry_admission,
            'admissions': admissions,
            'admission_list_path': reverse('students:admission') + '?type=admission-list',
            'page_type': page_type,
            'date_range': date_range,
            'select_student': select_student,
        }

        return context

    def handle_admission_post_request(request):
        try:
            admission_id = request.POST.get('student_id')
            data = {field: request.POST.get(field) for field in ['enquiry', 'admission_fee', 'admission_date', 'address_doc_type']}
            files = {field: request.FILES.get(field) or request.POST.get(f'existing_{field}') for field in ['student_photo', 'qualification_docs', 'address_docs']}
            data['admission_date'] = datetime.strptime(data['admission_date'], '%d-%m-%Y').date()

            enquiry_obj = get_object_or_404(Enquiry, pk=data['enquiry'])
            admission_data = {**data, 'enquiry': enquiry_obj, **files}

            existing_admission = Admission.objects.filter(enquiry=enquiry_obj).first()

            if admission_id:
                admission = get_object_or_404(Admission, pk=admission_id)
                admission_data['student_photo'] = admission_data['student_photo'] or admission.student_photo
                admission_data['qualification_docs'] = admission_data['qualification_docs'] or admission.qualification_docs
                admission_data['address_docs'] = admission_data['address_docs'] or admission.address_docs

                admission.__dict__.update(admission_data)
                admission.save()
                message = 'Admission Updated Successfully'
            elif existing_admission:
                raise Exception('Admission for this enquiry already exists')
            else:
                Admission.objects.create(**admission_data)
                message = 'Admission Added Successfully'
            
            messages.success(request, message)

        except Exception as e:
            messages.error(request, str(e))
        return redirect('students:admission')