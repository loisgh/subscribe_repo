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

    def check_for_customer(cst_id):
        try:
            cust = Customer.objects.get(pk=int(cst_id))
            print("customer: {} DOES exist".format(cst_id))
        except Customer.DoesNotExist:
            print("customer: {} does NOT exist".format(cst_id))
            cust = None

        return cust

    def create_update_cust(cust, rec):

        if not cust:
            cust = Customer()
            cust.cust_cst_id = rec.cust_id
            cust.cust_first_name = rec.first
            cust.cust_last_name = rec.last
            cust.cust_address = rec.addr
            cust.cust_state = rec.state
            cust.cust_zip = rec.zip
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

    def val_dates(cust, rec):
        try:
            if cust.mod_date >= rec.date:
                print("The mod date on the record is >= the input date.")
                return False
            print("The mod date on the record is < the input date. This is good.")
            return True
        except AttributeError:
            print("AttributeError. This is not a problem.")
            return True

    def val_status(cust, rec):

        if not cust:
            if rec.status == 'canceled':
                print("We don't have a customer so the status can't be cancelled")
                return False
        else:
            if (cust.cust_change_in_purchase_status == 'canceled' and rec.status == 'new') or \
               (cust.cust_change_in_purchase_status == 'new' and rec.status == 'new') or \
               (cust.cust_change_in_purchase_status == 'canceled' and rec.status == 'canceled'):
                print("We have a customer but the status is weird")
                return False
        print("The status is okay")
        return True

    def __repr__(self):
        return "{}: {} {}".format(self.cust_id, self.cust_first_name, self.cust_last_name)

    def __str__(self):
        return "{}: {} {}".format(self.cust_id, self.cust_first_name, self.cust_last_name)