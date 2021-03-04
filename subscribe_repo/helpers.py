from .models import Customer
from subscribe_repo.record import Record

#TODO Add test cases in test file for all negative test cases

def parse_subs(infile):
    error_dict = {}
    num_recs_processed = 0
    cust = Customer()


    for line in infile:
        line = line.decode()
        print(line)
        cust_id, first, last, addr, state, inzip, status, \
        prod_cust_id, prod_name, prod_cost, date = line.strip().split('\t')
        rec = (Record(cust_id, first, last, addr, state, inzip, status, \
                              prod_cust_id, prod_name, prod_cost, date))

        cust = cust.check_for_customer(rec.cust_id)
        if not cust.val_dates(cust, rec):
            error_dict = update_error_dict(error_dict, rec.cust_id, "current mod date <= date on update record")
        if not cust.val_status(cust, rec):
            error_dict = update_error_dict(error_dict, rec.cust_id, "status is inconsistant")
        if not cust.val_state(rec):
            error_dict = update_error_dict(error_dict, rec.cust_id, "The state code is invalid")
        if not cust.val_zip(rec):
            error_dict = update_error_dict(error_dict, rec.cust_id, "The zip code is invalid")
        if not rec.cust_id in error_dict:
            cust.create_update_cust(cust, rec)
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
