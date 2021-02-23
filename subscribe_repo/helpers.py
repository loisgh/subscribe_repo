from .models import Customer
from dateutil import parser
import re


CUST_ID = 0
FIRST = 1
LAST = 2
ADDR = 3
STATE = 4
ZIP = 5
STATUS = 6
PROD_cst_id = 7
PROD_NAME = 8
PROD_COST = 9
DATE = 10


def parse_subs(data):
    error_dict = {}

    cdata = re.split(r'\t+', data)
    cust = check_for_record(cdata[CUST_ID])
    if not valcst_id_dates(cust, cdata):
        error_dict = update_error_dict(error_dict, cdata[CUST_ID], "current mod date <= date on update record")
    if not valcst_id_status(cust, cdata):
        error_dict = update_error_dict(error_dict, cdata[CUST_ID], "status is inconsistant")
    if not cdata[CUST_ID] in error_dict:
        create_update_cust(cust, cdata)

    return error_dict


def update_error_dict(error_dict, cst_id, message):

    if cst_id in error_dict:
        val = error_dict[CUST_ID]
        val.append(message)
        error_dict[CUST_ID] = val
    else:
        error_dict[CUST_ID] = [message]
    return error_dict


def valcst_id_dates(cust, data):
    try:
        the_date = parser.isoparse(data[DATE])
        if cust.mod_date >= the_date:
            return False
        return True
    except AttributeError:
        return True


def valcst_id_status(cust, data):

    if not cust:
        if data[STATUS] == 'canceled':
            return False
    else:
        if (cust.cust_change_in_purchase_status == 'canceled' and data[STATUS] == 'new') or \
           (cust.cust_change_in_purchase_status == 'new' and data[STATUS] == 'new') or \
           (cust.cust_change_in_purchase_status == 'canceled' and data[STATUS] == 'canceled'):
            return False
    return True


def check_for_record(cst_id):
    try:
        cust = Customer.objects.get(pk=int(cst_id))
    except Customer.DoesNotExist:
        cust = None

    return cust


def create_update_cust(cust, data):

    if not cust:
        cust = Customer()
        cust.cust_cst_id = data[CUST_ID]
        cust.cust_first_name = data[FIRST]
        cust.cust_last_name = data[LAST]
        cust.cust_address = data[ADDR]
        cust.cust_state = data[STATE]
        cust.cust_zip = data[ZIP]
        cust.cust_change_in_purchase_status = data[STATUS]
        cust.prod_id = data[PROD_cst_id]
        cust.prod_name = data[PROD_NAME]
        cust.prod_purchase_amount = float(data[PROD_COST])
        cust.mod_date = data[DATE]
    else:
        cust = check_for_record(data[CUST_ID])
        cust.mod_date = data[DATE]
        cust.cust_change_in_purchase_status = data[STATUS]

    cust.save()
