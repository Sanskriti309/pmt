from django.contrib import admin

from .models import Course, Enquiry, Admission, FeeManagement

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = ("name", "duration")
    list_per_page = 10

    def get_list_display(self, request):
        user = request.user

        if user.groups.filter(name='Instructors').exists():
            return ('name', 'duration')
        return ('name', 'duration', 'fee')
    
    def get_fieldsets(self, request, obj=None):
        user = request.user
        if user.groups.filter(name='Instructors').exists():
            return (
                (None, {
                    'fields': ('name', 'duration', 'description', 'instructor', 'is_active', 'created_date'),
                }),
            )
        return super().get_fieldsets(request, obj=obj)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display=('name', 'contact_no', 'course_interested', 'discounted_fee', 'enquiry_date')
    list_per_page = 10
    list_filter = ("name", "enquiry_date")


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    
    def enquiry_name(self, obj):
        return obj.enquiry.name
    enquiry_name.short_description = "Name"

    def enquiry_contact_no(self, obj):
        return obj.enquiry.contact_no
    enquiry_contact_no.short_description = "Contact No."

    list_display = ('enquiry_name', 'enquiry_contact_no', 'admission_fee', 'admission_date')
    list_filter = ('enquiry__name', 'admission_date')
    list_per_page = 10

class AdmissionFilter(admin.SimpleListFilter):
    title = 'Admission'
    parameter_name = 'admission'

    def lookups(self, request, model_admin):
        return [(a.id, str(a)) for a in Admission.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(admission__id=self.value())
        return queryset


@admin.register(FeeManagement)
class FeeManagementAdmin(admin.ModelAdmin):
    list_display = ('admission', 'paid_fee', 'fee_paid_date', 'total_due_display', 'created_date')
    list_filter = ('fee_paid_date', AdmissionFilter)
    readonly_fields = ('total_due_display',)
    list_per_page = 10
    
    def total_due_display(self, obj):
        return obj.total_due
    total_due_display.short_description = 'Total Due'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []




