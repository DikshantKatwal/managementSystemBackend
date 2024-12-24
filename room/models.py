from django.db import models
from django_softdelete.models import SoftDeleteModel

from customer.models import Costumer


class Room(SoftDeleteModel, models.Model):
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    room_no = models.IntegerField(null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=True)

    class Meta:
        db_table = "room"


class CheckIn(SoftDeleteModel, models.Model):
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Costumer, null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE)
    agreed_price = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    advance = models.IntegerField(null=True, blank=True)
    total_people = models.IntegerField(null=True, blank=True)
    male_count = models.IntegerField(null=True, blank=True)
    female_count = models.IntegerField(null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_in_time = models.TimeField(null=True, blank=True)

    check_out = models.BooleanField(null=True, blank=True, default=False)
    check_out_date = models.DateField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    total_days = models.IntegerField(null=True, blank=True)
    total_paid = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "check_in"


class Payment(SoftDeleteModel, models.Model):
    checkin = models.ForeignKey(CheckIn, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='checkin_payments')
    agreed_price = models.IntegerField(null=True, blank=True)
    amount_paid = models.IntegerField(null=True, blank=True)
    remaining = models.IntegerField(null=True, blank=True)
    payment_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payments"


class CheckInHistory(SoftDeleteModel, models.Model):
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Costumer, null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE)
    agreed_price = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    advance = models.IntegerField(null=True, blank=True)
    total_people = models.IntegerField(null=True, blank=True)
    male_count = models.IntegerField(null=True, blank=True)
    female_count = models.IntegerField(null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_in_time = models.TimeField(null=True, blank=True)

    class Meta:
        db_table = "check_in_history"
