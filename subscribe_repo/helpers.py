from .models import Customer
from subscribe_repo.record import Record


def parse_subs(infile):
    error_dict = {}
    num_recs_processed = 0

    for line in infile:
        line = line.decode()
        cust_id, first, last, addr, state, zip, status, \
        prod_cust_id, prod_name, prod_cost, date = line.strip().split('\t')
        rec = (Record(cust_id, first, last, addr, state, zip, status, \
                              prod_cust_id, prod_name, prod_cost, date))

        cust = Customer.check_for_customer(rec.cust_id)
        if not Customer.val_dates(cust, rec):
            error_dict = update_error_dict(error_dict, rec.cust_id, "current mod date <= date on update record")
        if not Customer.val_status(cust, rec):
            error_dict = update_error_dict(error_dict, rec.cust_id, "status is inconsistant")
        if not rec.cust_id in error_dict:
            Customer.create_update_cust(cust, rec)
            num_recs_processed += 1

    return error_dict, num_recs_processed

def update_error_dict(error_dict, cst_id, message):

    if cst_id in error_dict:
        val = error_dict[cst_id]
        val.append(message)
        error_dict[cst_id] = val
    else:
        error_dict[cst_id] = [message]
    return error_dict
