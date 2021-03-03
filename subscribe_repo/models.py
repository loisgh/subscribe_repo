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

    @staticmethod
    def check_for_customer(cst_id):
        try:
            cust = Customer.objects.get(pk=int(cst_id))
        except Customer.DoesNotExist:
            cust = None

        return cust

    @staticmethod
    def create_update_cust(cust, rec):

        if not cust:
            cust = Customer()
            cust.cust_cst_id = rec.cust_id
            cust.cust_first_name = rec.first
            cust.cust_last_name = rec.last
            cust.cust_address = rec.addr
            cust.cust_state = rec.state
            cust.cust_zip = rec.inzip
            cust.cust_change_in_purchase_status = rec.status
            cust.prod_id = rec.prod_cust_id
            cust.prod_name = rec.prod_name
            cust.prod_purchase_amount = float(rec.prod_cost)
            cust.mod_date = rec.date
        else:
            cust = Customer.check_for_customer(rec.cust_id)
            cust.mod_date = rec.date
            cust.cust_change_in_purchase_status = rec.status

        cust.save()


    @staticmethod
    def val_dates(cust, rec):
        try:
            if cust.mod_date >= rec.date:
                return False
            return True
        except AttributeError:
            return True

    @staticmethod
    def val_status(cust, rec):

        if not cust:
            if rec.status == 'canceled':
                return False
        else:
            if (cust.cust_change_in_purchase_status == 'canceled' and rec.status == 'new') or \
               (cust.cust_change_in_purchase_status == 'new' and rec.status == 'new') or \
               (cust.cust_change_in_purchase_status == 'canceled' and rec.status == 'canceled'):
                return False
        return True

    def __repr__(self):
        return "{}: {} {}".format(self.cust_id, self.cust_first_name, self.cust_last_name)

    def __str__(self):
        return "{}: {} {}".format(self.cust_id, self.cust_first_name, self.cust_last_name)
