
from django.core.mail import send_mail
from django.conf import settings
from .models import Leave, LeaveBalence, LeaveCategory
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from datetime import timedelta, timezone, datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ValidationError
import re

def send_email(subject, message, recipient_list):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
        )
        print("Email sent successfully.")
        return True
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        return False
    
class LeaveViewTemplate:
    def __init__(self):
        self.leave_categories = LeaveCategory.objects.all()

    def filterEmployeeLeave(self, employee):

        leave_categories = self.leave_categories
        leave_data = []
        column_names = []

        column_names.extend(category.name for category in leave_categories)
        employee =employee
        leave_balance = LeaveBalence.objects.filter(user=employee).first()

        if leave_balance:
            data_dict = {'Employee': f"{employee.first_name} {employee.last_name}"}
            for category in leave_categories:
                leave_entry = LeaveBalence.objects.filter(user=employee, leave_category=category).first()
                data_dict[category.name] = leave_entry.leave_balance if leave_entry else category.max_leaves
            leave_data.append(data_dict)
        else:
            data_dict = {'Employee': f"{employee.first_name} {employee.last_name}"}
            for category in leave_categories:
                data_dict[category.name] = category.max_leaves
            leave_data.append(data_dict)

        return leave_data, column_names
    
    def leave_summary(self, user):
        """
        Display a summary of leave information for the logged-in user.

        This function retrieves leave balance data for the logged-in user, calculates
        the total leave, taken leaves, and balanced leaves, and renders a template
        to display the leave summary.
        """
        leave_balances = LeaveBalence.objects.filter(user=user)

        total_leave = sum(balance.leave_category.max_leaves for balance in leave_balances)
        taken_leave = sum(balance.leave_balance for balance in leave_balances)
        balanced_leave = total_leave - taken_leave

        context = {
            'total_leave': total_leave,
            'taken_leave': taken_leave,
            'balanced_leave': balanced_leave,
            'leave_balances': leave_balances,
        }
        return context
    
    def other_staff_leave_list(self, user):
        current_date = datetime.now(timezone.utc).date()

        end_date = current_date + timedelta(days=60)

        logged_in_user = user

        leaves = Leave.objects.filter(
            start_date__gte=current_date,
            end_date__lte=end_date
        ).exclude(employee__user=logged_in_user)

        leave_data = [{"Name": f"{leave.employee.user.first_name} {leave.employee.user.last_name}" if leave.employee.user.first_name else leave.employee.user.username, "Date": leave.start_date.strftime("%d-%m-%Y")} for leave in leaves]
        context= {'other_staff_leave_list': leave_data}
        return context
    
    def get_leave_categories(self):
        return self.leave_categories

    def get_employees(self):
        return User.objects.filter(groups__name='Employee')

    def get_leave_data_for_employee(self, employee):
        leave_balance = LeaveBalence.objects.filter(user=employee).first()
        data_dict = {'Employee': f"{employee.first_name} {employee.last_name}" if employee.first_name else employee.username}
        
        for category in self.leave_categories:
            leave_entry = LeaveBalence.objects.filter(user=employee, leave_category=category).first()
            data_dict[category.name] = leave_entry.leave_balance if leave_entry else category.max_leaves
        
        return data_dict

    def get_leave_status_counts(self, employee, category):
        return {
            'rejected_count': Leave.objects.filter(employee__user=employee, leave_type__name=category, status__status='Rejected').count(),
            'pending_count': Leave.objects.filter(employee__user=employee, leave_type__name=category, status__status='Pending').count(),
            'approved_count': Leave.objects.filter(employee__user=employee, leave_type__name=category, status__status='Approved').count()
        }

    def paginate_data(self, data, page, per_page=10):
        paginator = Paginator(data, per_page)
        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)

    def safe_parse_date(self, date_str):
        try:
            return parse_date(date_str) if date_str else None
        except ValidationError:
            return None


