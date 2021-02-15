from django.db import models
import localflavor.us.forms


class Customer(models.Model):
    PURCHASE_CHOICES = (('new', 'new'), ('canceled', 'canceled'))
    cust_id = models.IntegerField(null=False, primary_key=True, unique=True)
    cust_first_name = models.CharField(null=False, max_length=30)
    cust_last_name = models.CharField(null=False, max_length=30)
    cust_address = models.CharField(null=False, max_length=75)
    cust_state = localflavor.us.forms.USStateField
    cust_zip = models.CharField(null=False, max_length=5)
    cust_change_in_purchase_status = models.CharField(null=False, max_length=15, choices=PURCHASE_CHOICES)
    prod_id = models.IntegerField(null=False)
    prod_name = models.CharField(null=False, max_length=100)
    prod_purchase_amount = models.DecimalField(null=False, max_digits=5, decimal_places=2)
    mod_date = models.DateTimeField(null=False)
