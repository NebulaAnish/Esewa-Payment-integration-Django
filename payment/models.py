from django.db import models

# Create your models here.

class Order(models.Model):
    order_id = models.CharField(max_length=6, null=True, unique=True)
    name = models.CharField(max_length=100)
    total_price = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(null=True, blank=True)