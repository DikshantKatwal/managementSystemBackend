from django.db import models
from django.utils import timezone
from django_softdelete.models import SoftDeleteModel

from users.models import NewUser


class Employee(SoftDeleteModel, models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, null=True, blank=True, related_name='employee_user')
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    dob = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=timezone.now)
    pan_no = models.CharField(max_length=20, null=True, blank=True)
    personal_contact = models.CharField(max_length=255, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    nationality = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_relation = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_contact_no = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "employee"
