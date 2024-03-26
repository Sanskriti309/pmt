from django.contrib import admin
from .models import Profile, Bank, EmergencyContact, FamilyInfo, Education, Experience, JobSkill, JobProfile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'dob', 'nationality', 'marital_status', 'no_of_children')
    list_filter = ('gender', 'marital_status')
    search_fields = ('user__username', 'user__email', 'nationality', 'religion')

class BankAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'account', 'ifsc', 'pan')
    search_fields = ('user__username', 'name', 'account', 'ifsc', 'pan')

class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('get_user_username', 'name', 'relation', 'phone', 'contact_type', 'is_active')
    list_filter = ('contact_type', 'is_active')
    search_fields = ('user__username', 'name', 'relation', 'phone')

    def get_user_username(self, obj):
        return obj.profile.username

    get_user_username.short_description = 'User'

class FamilyInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'relation', 'dob', 'phone', 'is_active', 'created_at')
    list_filter = ('relation', 'is_active', 'created_at')
    search_fields = ('user__username', 'name', 'relation', 'phone')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'stream', 'from_year', 'to_year', 'created_at', 'is_active')
    list_filter = ('stream', 'created_at', 'is_active')
    search_fields = ('user__username', 'college', 'stream')

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'from_date', 'to_date', 'created_at', 'is_active')
    list_filter = ('from_date', 'created_at', 'is_active')
    search_fields = ('user__username', 'company')


class JobSkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class JobProfileAdmin(admin.ModelAdmin):
    list_display = ('title', 'experience_required', 'created_at', 'updated_at')
    list_filter = ('experience_required', 'created_at')
    search_fields = ('title', 'description', 'responsibilities', 'qualifications', 'skills_required__name')
    filter_horizontal = ('skills_required',)

admin.site.register(JobProfile, JobProfileAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(EmergencyContact, EmergencyContactAdmin)
admin.site.register(FamilyInfo, FamilyInfoAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(JobSkill, JobSkillAdmin)