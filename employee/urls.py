from django.urls import path

from .api import *

urlpatterns = [
    path('', EmployeeDetails.as_view(), name='employee_details'),
]
