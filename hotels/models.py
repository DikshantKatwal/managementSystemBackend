from django.db import models
from django_softdelete.models import SoftDeleteModel

from users.models import NewUser


class Hotel(SoftDeleteModel, models.Model):
    company = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True, related_name='hotel_company')
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)

    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "db_hotel"
