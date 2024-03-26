from .models import Performance, PerformanceCategory
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from datetime import datetime

class performanceUtils:

    def get_or_create_performance(data):

        employee_name = get_object_or_404(User, pk=data.get('employee_name'))
        performance_date_str = data.get('performance_date')
        performance_date = datetime.strptime(performance_date_str, '%d-%m-%Y')
        performance_category = data.getlist('performance_category')
        rating = data.get('rating')
        productive = data.get('productive_2')
        progress = data.get('progress')
        comment = data.get('comment')
        
        performance, created = Performance.objects.get_or_create(
            user=employee_name,
            performance_date=performance_date,
            defaults={
                'rating': rating,
                'is_productive': productive,
                'progress': progress,
                'comment': comment
            }
        )

        performance.performance_categories.set(performance_category)

        return performance
