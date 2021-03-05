from django.db import models


class Customer(models.Model):
    PURCHASE_CHOICES = ["new", "canceled"]
    STATE_CHOICES = [
        "AL",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY" "AK",
        "DC",
        "PR",
    ]
    cust_id = models.IntegerField(null=False, primary_key=True, unique=True)
    cust_first_name = models.CharField(null=False, max_length=30)
    cust_last_name = models.CharField(null=False, max_length=30)
    cust_address = models.CharField(null=False, max_length=75)
    cust_state = models.CharField(max_length=2)
    cust_zip = models.CharField(max_length=5)
    cust_change_in_purchase_status = models.CharField(null=False, max_length=15)
    prod_id = models.IntegerField(null=False)
    prod_name = models.CharField(null=False, max_length=100)
    prod_purchase_amount = models.DecimalField(
        null=False, max_digits=5, decimal_places=2
    )
    mod_date = models.DateTimeField(null=False)

    def check_for_customer(self, cst_id):
        try:
            return Customer.objects.get(pk=int(cst_id))
        except Customer.DoesNotExist:
            return Customer()

    def create_update_cust(self, cust, rec):

        if not cust.cust_id:
            Customer.objects.create(
                cust_id=rec.cust_id,
                cust_first_name=rec.first,
                cust_last_name=rec.last,
                cust_address=rec.addr,
                cust_state=rec.state,
                cust_zip=rec.inzip,
                cust_change_in_purchase_status=rec.status,
                prod_id=rec.prod_cust_id,
                prod_name=rec.prod_name,
                prod_purchase_amount=float(rec.prod_cost),
                mod_date=rec.date,
            )
        else:
            cust = Customer()
            cust = cust.check_for_customer(rec.cust_id)
            cust.mod_date = rec.date
            cust.cust_change_in_purchase_status = rec.status
            cust.save()

    def val_dates(self, cust, rec):
        try:
            if cust.mod_date >= rec.date:
                return False
            return True
        except TypeError:
            return True

    def val_status(self, cust, rec):
        if rec.status not in Customer.PURCHASE_CHOICES:
            return False
        elif not cust.cust_change_in_purchase_status:
            if rec.status == "canceled":
                return False
        else:
            if (
                (
                    cust.cust_change_in_purchase_status == "canceled"
                    and rec.status == "new"
                )
                or (
                    cust.cust_change_in_purchase_status == "new" and rec.status == "new"
                )
                or (
                    cust.cust_change_in_purchase_status == "canceled"
                    and rec.status == "canceled"
                )
            ):
                return False
        return True

    def val_state(self, rec):
        return True if rec.state in Customer.STATE_CHOICES else False

    def val_zip(self, rec):
        return True if len(rec.inzip) == 5 and rec.inzip.isdigit() else False

    def __repr__(self):
        return "{}: {} {}".format(
            self.cust_id, self.cust_first_name, self.cust_last_name
        )

    def __str__(self):
        return "{}: {} {}".format(
            self.cust_id, self.cust_first_name, self.cust_last_name
        )
