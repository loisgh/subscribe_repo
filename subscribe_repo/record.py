from dateutil import parser

class Record:
    """This record is used to parse the input file"""

    def __init__(self, cust_id, first, last,
                 addr, state, zip, status,
                 prod_cust_id, prod_name,
                 prod_cost, date):
        self.cust_id = cust_id
        self.first = first
        self.last = last
        self.addr = addr
        self.state = state
        self.zip = zip
        self.status = status
        self.prod_cust_id = prod_cust_id
        self.prod_name = prod_name
        self.prod_cost = prod_cost
        self.date = parser.isoparse(date)
