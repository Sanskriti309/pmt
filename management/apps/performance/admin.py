from django.contrib import admin
from .models import PerformanceCategory, Performance, PerformanceKeys, PerformanceAppraisal

# Register your models here.

class PerformanceCategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    search_fields = ('category',)



class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_productive', 'rating', 'progress', 'performance_date', 'created_at')
    list_filter = ('is_productive',)
    search_fields = ('user__username', 'comment', 'performance_date')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


class PerformanceKeysAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_value', 'max_value', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

class AppraisalPerformanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'performance_keys', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

admin.site.register(PerformanceAppraisal, AppraisalPerformanceAdmin)
admin.site.register(PerformanceCategory, PerformanceCategoryAdmin)
admin.site.register(PerformanceKeys, PerformanceKeysAdmin)
admin.site.register(Performance, PerformanceAdmin)