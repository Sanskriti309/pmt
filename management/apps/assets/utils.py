from .models import ManageAsset
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class ManagementAssets:
    def __init__(self):
        pass
    def get_all_assets(self, request):

            employees = User.objects.all()

            selected_employee_id = request.GET.get('employee_id')

            if selected_employee_id:
                assets = ManageAsset.objects.filter(assigned_to=selected_employee_id)
            else:
                assets = ManageAsset.objects.all()

            total_cost = assets.aggregate(Sum('cost'))['cost__sum'] or 0

            paginator = Paginator(assets, 10)
            page = request.GET.get('page', 1)

            try:
                assets = paginator.page(page)
            except PageNotAnInteger:
                assets = paginator.page(1)
            except EmptyPage:
                assets = paginator.page(paginator.num_pages)
            context={
                "assets": assets,
                "total_cost": total_cost,
                "isAccess": True,
                "employees": employees,
                "selected_employee_id": int(selected_employee_id) if selected_employee_id else None,
            }
            return context

    def get_employee_assets(self, request):
        user = request.user

        assets = ManageAsset.objects.filter(assigned_to=user)

        total_cost = assets.aggregate(Sum('cost'))['cost__sum'] or 0

        paginator = Paginator(assets, 10)
        page = request.GET.get('page', 1)

        try:
            assets = paginator.page(page)
        except PageNotAnInteger:
            assets = paginator.page(1)
        except EmptyPage:
            assets = paginator.page(paginator.num_pages)

        context={
            "assets": assets,
            "total_cost": total_cost,
            "isAccess": False,
            "employees": [],
            "selected_employee_id": None,
        }
        return context