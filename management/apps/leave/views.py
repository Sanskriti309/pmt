from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User, Group
from .models import Leave,LeaveBalence,LeaveCategory,LeaveStatus,Type
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from .utils import LeaveViewTemplate
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.utils.filter import GlobalFilter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

global_filter = GlobalFilter()

leaveViewTemplate = LeaveViewTemplate()

# Create your views here.

# Leave Balance View
class LeaveBalanceView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if global_filter.check_access_filter(request, ['isStudent']):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    template_name = 'web/leaves/Leave-balance.html'

    def get(self, request, *args, **kwargs):
        leave_categories = leaveViewTemplate.get_leave_categories()

        isAdmin = global_filter.check_access_filter(request, ["isAdmin", "isManager","isMarketing"])

        is_superuser = isAdmin
        leave_data = []

        if is_superuser:
            column_names = ['Employee']
            column_names.extend(category.name for category in leave_categories)
            employees = leaveViewTemplate.get_employees()
            selected_employee_id = request.GET.get('employee_id')
            filtered_employees = employees if not selected_employee_id else employees.filter(id=selected_employee_id)

            for employee in filtered_employees:
                employee_leave_data = leaveViewTemplate.get_leave_data_for_employee(employee)
                leave_data.append(employee_leave_data)
        else:
            employee_leave_data = leaveViewTemplate.get_leave_data_for_employee(request.user)
            leave_data.append(employee_leave_data)
            column_names = [category.name for category in leave_categories]

        paginated_leave_data = leaveViewTemplate.paginate_data(leave_data, request.GET.get('page', 1))
        context = {'column_names': column_names, 'leave_data': paginated_leave_data, 'is_superuser': is_superuser, 'employees': employees if is_superuser else None}
        return render(request, self.template_name, context)


# Leave View
class LeaveView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if global_filter.check_access_filter(request, ['isStudent']):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
        
    template_name = 'web/leaves/leaves.html'

    def get(self, request, *args, **kwargs):

        isAdmin = global_filter.check_access_filter(request, ["isAdmin", "isManager","isMarketing"])
        isMarket = global_filter.check_access_filter(request, ["isMarketing"])

        employee_name = request.GET.get('employee_name', '')
        leave_type = request.GET.get('leave_type', '')
        leave_status = request.GET.get('leave_status', '')
        start_date_str = request.GET.get('start_date', '')
        end_date_str = request.GET.get('end_date', '')

        start_date =leaveViewTemplate.safe_parse_date(start_date_str)
        end_date = leaveViewTemplate.safe_parse_date(end_date_str)

        employees = User.objects.filter(groups__name='Employee')
        
        selected_employee_id = request.GET.get('employee_id')

        leave_statuses = LeaveStatus.objects.all()
        categories = LeaveCategory.objects.all()
        types = Type.objects.all()
        
        filtered_employees = employees
        leave_data = None

        leave_categories = {}

        if selected_employee_id:
            filtered_employees = employees.filter(id=selected_employee_id)
            userdata = User.objects.filter(id=selected_employee_id).first()
            leave_data, column_names = leaveViewTemplate.filterEmployeeLeave(userdata)

            for category in leave_data[0]:
                rejected_count = Leave.objects.filter(
                    employee__user__in=filtered_employees,
                    leave_type__name=category,
                    status__status='Rejected'
                ).count()
                pending_count = Leave.objects.filter(
                    employee__user__in=filtered_employees,
                    leave_type__name=category,
                    status__status='Pending'
                ).count()
                approved_count = Leave.objects.filter(
                    employee__user__in=filtered_employees,
                    leave_type__name=category,
                    status__status='Approved'
                ).count()

                remaining_balance = leave_data[0][category]

                leave_categories[category] = {
                    'rejected_count': rejected_count,
                    'pending_count': pending_count,
                    'approved_count': approved_count,
                    'remaining_balance': remaining_balance
                }

        elif not isAdmin:
            filtered_employees = employees.filter(id=request.user.id)
            userdata = request.user
            leave_data, column_names = leaveViewTemplate.filterEmployeeLeave(userdata)

            for category in leave_data[0]:
                rejected_count = Leave.objects.filter(
                    employee__user__in=filtered_employees,
                    leave_type__name=category,
                    status__status='Rejected'
                ).count()
                pending_count = Leave.objects.filter(
                    employee__user__in=filtered_employees,
                    leave_type__name=category,
                    status__status='Pending'
                ).count()
                approved_count = Leave.objects.filter(
                    employee__user__in=filtered_employees,
                    leave_type__name=category,
                    status__status='Approved'
                ).count()

                remaining_balance = leave_data[0][category]

                leave_categories[category] = {
                    'rejected_count': rejected_count,
                    'pending_count': pending_count,
                    'approved_count': approved_count,
                    'remaining_balance': remaining_balance
                }

        leaves = Leave.objects.filter(
            employee__user__in=filtered_employees,
            leave_type__name__icontains=leave_type,
            status__status__icontains=leave_status,
        )
        if start_date:
            leaves = leaves.filter(start_date__gte=start_date)
        if end_date:
            leaves = leaves.filter(end_date__lte=end_date)

        leaves = leaves.exclude(start_date__isnull=True).exclude(end_date__isnull=True)

        if not isAdmin:
            exclude_columns = ['id', 'employee', 'type', 'requested_date', 'is_end_date_half_day', 'is_start_date_half_day']
        else:
            exclude_columns = ['id', 'type', 'requested_date', 'is_end_date_half_day', 'is_start_date_half_day', 'notes']

        fields = [field.name.replace("_", " ") for field in Leave._meta.get_fields() if field.name.lower() not in exclude_columns]
        fields.insert(fields.index('end date') + 1, 'no. of Days')

        paginator = Paginator(leaves, 10)
        page = request.GET.get('page', 1)

        try:
            leaves = paginator.page(page)
        except PageNotAnInteger:
            leaves = paginator.page(1)
        except EmptyPage:
            leaves = paginator.page(paginator.num_pages)

        if selected_employee_id or not isAdmin:
            return render(
                request, 
                self.template_name,
                {
                    'leaves': leaves,
                    'leave_categories': leave_categories,
                    'fields': fields,
                    'employees': employees, 
                    'is_superuser': isAdmin,
                    'is_marketing': isMarket,
                    'show_cards': bool(not isAdmin or selected_employee_id),
                    'leave_statuses': leave_statuses,
                    'types': types,
                    'categories': categories,
                }
            )
        else:
            return render(
                request, 
                self.template_name,
                {
                    'leaves': leaves,
                    'fields': fields,
                    'employees': employees, 
                    'is_superuser': isAdmin,
                    'is_marketing': isMarket,
                    'show_cards': bool(not isAdmin or selected_employee_id),
                    'leave_statuses': leave_statuses,
                    'types': types,
                    'categories': categories,
                }
            )
        
    def post(self, request, *args, **kwargs):

        isAdmin = global_filter.check_access_filter(request, ["isAdmin", "isManager"])

        try:
            leave_id = request.POST.get('leave_id')
            employee_name = request.POST.get('employee_name')
            leave_type_name = request.POST.get('leave_type')
            from_date = request.POST.get('from_date')
            end_date = request.POST.get('to_date')
            requested_date = request.POST.get('requested_date')
            status = request.POST.get('leave_status')
            reason = request.POST.get('reason_value')
            types = request.POST.get('type')
            notes = request.POST.get('notes')
            half_day_start = request.POST.get('half_day_start')
            half_day_end = request.POST.get('half_day_end')

            if not isAdmin:
                status = LeaveStatus.objects.get(status='Pending').id
                types = Type.objects.get(type='Paid').id
                requested_date = datetime.now().strftime("%d-%m-%Y")
                employee_name = request.user

            status_obj = LeaveStatus.objects.get(pk=status)
            type_obj = Type.objects.get(pk=types)
            leave_type_obj = LeaveCategory.objects.get(name=leave_type_name)
            employee_group = Group.objects.get(name='Employee')
            employee_instance = employee_group.user_set.get(username=employee_name)

            if leave_id:
                leave = get_object_or_404(Leave, pk=leave_id)

                if leave.status.status != 'Approved' and status_obj.status == 'Approved':
                    leave_balance_entry = LeaveBalence.objects.get(user=employee_instance, leave_category=leave_type_obj)
                    leave_balance_entry.leave_balance -= leave.total_days
                    leave_balance_entry.save()

                elif leave.status.status == 'Approved' and status_obj.status != 'Approved':
                    leave_balance_entry = LeaveBalence.objects.get(user=employee_instance, leave_category=leave_type_obj)
                    leave_balance_entry.leave_balance += leave.total_days
                    leave_balance_entry.save()

                elif leave.status.status != 'Approved' and status_obj.status != 'Approved':
                    leave_balance_entry = LeaveBalence.objects.get(user=employee_instance, leave_category=leave_type_obj)
                    leave_balance_entry.save()

                elif leave.status.status == 'Approved' and status_obj.status == 'Approved':
                    raise Exception('Applied Leave is already approved.')
                    
                leave.employee = leave_balance_entry
                leave.leave_type = leave_type_obj
                leave.start_date = from_date
                leave.end_date = end_date
                leave.status = status_obj
                leave.approved_by = request.user if isAdmin else None
                leave.reason = reason
                leave.type = type_obj
                leave.notes = notes
                leave.save() 
                
                message = 'Leave Updated Successfully'
            else:
                employee_instance = employee_group.user_set.get(username=employee_name)
                leave_balance_entry, created = LeaveBalence.objects.get_or_create(user=employee_instance, leave_category=leave_type_obj, defaults={'leave_balance': leave_type_obj.max_leaves})

                parsed_start_date = datetime.strptime(from_date, "%d-%m-%Y")
                parsed_end_date = datetime.strptime(end_date, "%d-%m-%Y")
                parsed_requested_date = datetime.strptime(requested_date, "%d-%m-%Y")

                start_date = parsed_start_date.strftime("%Y-%m-%d")
                end_date = parsed_end_date.strftime("%Y-%m-%d")
                requested_date = parsed_requested_date.strftime("%Y-%m-%d")

                if parsed_end_date < parsed_start_date:
                    raise Exception('End date cannot be less than start date.')
                
                if parsed_requested_date > parsed_start_date:
                    raise Exception('Requested date cannot be greater than start date.')

                date_difference = parsed_end_date - parsed_start_date

                if start_date == end_date:
                    if half_day_start or half_day_end:
                        total_days_left = 0.5
                    else:
                        total_days_left = date_difference.days + 1
                elif start_date != end_date:
                    if half_day_start and half_day_end:
                        total_days_left = date_difference.days
                    elif half_day_start or half_day_end:
                        total_days_left = date_difference.days + 0.5
                    else:
                        total_days_left = date_difference.days + 1

                existing_leaves = Leave.objects.filter(
                    Q(employee__user=employee_instance) &
                    (
                        Q(start_date__lte=start_date, end_date__gte=start_date, status__status__in=['Pending', 'Approved']) |
                        Q(start_date__lte=end_date, end_date__gte=end_date, status__status__in=['Pending', 'Approved']) |
                        Q(start_date__gte=start_date, end_date__lte=end_date, status__status__in=['Pending', 'Approved'])
                    )
                )

                if existing_leaves.exists():
                    raise Exception('Leave already applied for the selected date. Please select another date.')

                leave = Leave.objects.create(
                    employee=leave_balance_entry,
                    leave_type=leave_type_obj,
                    start_date = start_date,
                    end_date = end_date,
                    type = type_obj,
                    requested_date = requested_date,
                    status=status_obj,
                    approved_by = request.user if request.user.is_superuser else None,
                    reason=reason,
                    is_start_date_half_day=bool(half_day_start),
                    is_end_date_half_day=bool(half_day_end),
                )

                if status_obj.status == 'Approved':
                    leave_balance_entry.leave_balance -= total_days_left
                    leave_balance_entry.save()
                    
                message = 'Leave Added Successfully'
            
            messages.success(request, message)
        except Exception as e:
            messages.error(request, str(e))
        return redirect('leave:leave')

