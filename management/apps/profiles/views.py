from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages 
from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from .models import Profile, Bank, EmergencyContact, FamilyInfo, Education, Experience
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.assets.utils import ManagementAssets

ma = ManagementAssets()

# Get Profile View
@method_decorator(login_required, name='dispatch')
class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        user = request.user
        profile = Profile.objects.filter(user=user).first()
        bank_account = Bank.objects.filter(user=user).first()
        emergency_contacts = EmergencyContact.objects.filter(profile=user)
        family_info = FamilyInfo.objects.filter(user=user)
        education = Education.objects.filter(user=user)
        experiences = Experience.objects.filter(user=user)
        get_employee_assets= ma.get_employee_assets(request)
        merged_context = get_employee_assets.copy()

        user_fields = ['id', 'email', 'first_name', 'last_name', 'date_joined']
        user_data = {field: getattr(user, field) for field in user_fields}

        context = {
            'profile': profile,
            'bank_account': bank_account,
            'emergency_contacts': emergency_contacts,
            'family_info': family_info,
            'education': education,
            'experiences': experiences,
            'user_data': user_data,
            'profile_assets': merged_context,
        }

        return render(request, 'main/profile.html', context)


# Update Profile View 
@method_decorator(login_required, name='dispatch')
class UpdateProfileView(View):

    def post(self, request, *args, **kwargs):
        user = request.user

        try:
            profile, created = Profile.objects.get_or_create(user=user)

            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()

            profile.dob = datetime.strptime(request.POST.get('dob'), '%d-%m-%Y').date() if request.POST.get('dob') else None
            gender = request.POST.get('gender')
            if not gender:
                raise ValueError('Gender cannot be blank.')

            profile.gender = gender
            profile.address = request.POST.get('address')
            profile.phone = request.POST.get('phone')

            new_photo = request.FILES.get('photo')
            if new_photo:
                profile.photo = new_photo
                profile.existing_photo = ''

            profile.save()
            message="Profile Updated Successfully"
            
            messages.success(request, message)
        except Exception as e:
            messages.error(request, str(e))
        return redirect('profile')


# Update Personal Information View 
@method_decorator(login_required, name='dispatch')
class UpdatePersonalInfoView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        user = request.user

        try:
            profile, created = Profile.objects.get_or_create(user=user)

            profile.nationality = request.POST.get('nationality')
            profile.religion = request.POST.get('religion')
            profile.marital_status = request.POST.get('marital_status')
            profile.no_of_children = request.POST.get('no_of_children')

            profile.save()
            message="Personal Information Updated Successfully"
            
            messages.success(request, message)
        except Exception as e:
            messages.error(request, str(e))
        return redirect('profile')


# Update Bank View 
@method_decorator(login_required, name='dispatch')
class UpdateBankView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        user = request.user

        try:
            bank, created = Bank.objects.get_or_create(user=user)

            bank.name = request.POST.get('bank_name')
            bank.account = request.POST.get('bank_account')
            bank.ifsc = request.POST.get('ifsc_code')
            bank.pan = request.POST.get('pan_card')

            bank.save()
            message="Bank Information Updated Successfully"

            messages.success(request, message)
        except Exception as e:
            messages.error(request, str(e))
        return redirect('profile')


# Update Family View 
@method_decorator(login_required, name='dispatch')
class UpdateFamilyView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        user = request.user
        family_id = request.POST.get('family_info_id')

        try:

            if family_id:
                family = FamilyInfo.objects.get(id=family_id, user=user)
            else:
                family = FamilyInfo(user=user)

            family.name = request.POST.get('name')
            family.relation = request.POST.get('relation')
            family.dob = datetime.strptime(request.POST.get('dob'), '%d-%m-%Y').date() if request.POST.get('dob') else None
            family.phone = request.POST.get('phone')

            family.save()
            message="Family Information updated successfully"
            messages.success(request, message)
        except Exception as e:
            messages.error(request, str(e))
        return redirect('profile')


# Update Education View
@method_decorator(login_required, name='dispatch')
class UpdateEducationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        try:
            education_detail_ids = set()
            for key in request.POST:
                if key.startswith('education_detail_id_'):
                    education_detail_ids.add(int(request.POST[key]))

            for education_detail_id in education_detail_ids:
                college = request.POST.get(f'college_{education_detail_id}', '')
                stream = request.POST.get(f'stream_{education_detail_id}', '')
                from_year = request.POST.get(f'from_year_{education_detail_id}', '')
                to_year = request.POST.get(f'to_year_{education_detail_id}', '')

                to_year = to_year if to_year != '' else None
                
                if education_detail_id == 0:
                    education = Education.objects.create(
                        user=request.user,
                        college=college,
                        stream=stream,
                        from_year=from_year,
                        to_year=to_year,
                        is_active=True
                    )
                else:
                    education = get_object_or_404(Education, pk=education_detail_id)
                    education.college = college
                    education.stream = stream
                    education.from_year = from_year
                    education.to_year = to_year
                    education.save()

            if education_detail_id == 0:
                message = 'Education added successfully'
            else:
                message = 'Education updated successfully'

            messages.success(request, message)

        except Exception as e:
            messages.error(request, str(e))
        return redirect('profile')
        

# Update Experience View 
@method_decorator(login_required, name='dispatch')
class UpdateExperienceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            experience_detail_ids = set()
            for key in request.POST:
                if key.startswith('experience_detail_id_'):
                    experience_detail_ids.add(int(request.POST[key]))

            for experience_detail_id in experience_detail_ids:
                company = request.POST.get(f'company_{experience_detail_id}', '')
                from_date = request.POST.get(f'from_date_{experience_detail_id}', '')
                to_date = request.POST.get(f'to_date_{experience_detail_id}', '')
                
                to_date = to_date if to_date != '' else None

                if experience_detail_id == 0:
                    experience = Experience.objects.create(
                        user=request.user,
                        company=company,
                        from_date=datetime.strptime(from_date, '%d-%m-%Y').date(),
                        to_date=datetime.strptime(to_date, '%d-%m-%Y').date() if to_date else None,
                        is_active=True
                    )
                else:
                    experience = get_object_or_404(Experience, pk=experience_detail_id)
                    experience.company = company
                    experience.from_date = datetime.strptime(from_date, '%d-%m-%Y').date()
                    experience.to_date = datetime.strptime(to_date, '%d-%m-%Y').date() if to_date else None
                    experience.save()
            if experience_detail_id == 0:
                message = 'Experience added successfully'
            else:
                message = 'Experience updated successfully'

            messages.success(request, message)

        except Exception as e:
            messages.error(request, str(e))
        return redirect('profile')
    

# Update Emergency Contact View
@method_decorator(login_required, name='dispatch')
class UpdateEmergencyContactView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            emergency_contact_ids = set()
            for key in request.POST:
                if key.startswith('emergency_contact_id_'):
                    emergency_contact_ids.add(int(request.POST[key]))

            for emergency_contact_id in emergency_contact_ids:
                name = request.POST.get(f'name_{emergency_contact_id}', '')
                relation = request.POST.get(f'relation_{emergency_contact_id}', '')
                phone = request.POST.get(f'phone_{emergency_contact_id}', '')
                contact_type = request.POST.get(f'contact_type_{emergency_contact_id}', '')
                
                if emergency_contact_id == 0:
                    emergency_contact = EmergencyContact.objects.create(
                        profile=request.user,
                        name=name,
                        relation=relation,
                        phone=phone,
                        contact_type=contact_type,
                        is_active=True
                    )
                else:
                    emergency_contact = get_object_or_404(EmergencyContact, pk=emergency_contact_id)
                    emergency_contact.name = name
                    emergency_contact.relation = relation
                    emergency_contact.phone = phone
                    emergency_contact.contact_type = contact_type
                    emergency_contact.save()

            if emergency_contact_id == 0:
                message = 'Emergency Contact added successfully'
            else:
                message = 'Emergency Contact(s) updated successfully'

            messages.success(request, message)

        except Exception as e:
            messages.error(request, str(e))
        return redirect('profile')

