from django.contrib import admin
from .models import ManageAsset

@admin.register(ManageAsset)
class ManageAssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'condition_type', 'cost', 'assigned_to', 'assigned_Id', 'assigned_by')
    list_filter = ('assigned_to','assigned_Id','assigned_by')
    actions = ['assign_to_user']
    list_per_page = 10

    def assign_to_user(self, request, queryset):
        selected_user = request.user
        for asset in queryset:
            asset.assign_to(selected_user)

    assign_to_user.short_description = "Assign selected assets to user"


