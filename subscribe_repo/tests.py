from django.test import TestCase
from .models import Customer
from subscribe_repo import helpers
from dateutil import parser
import mock


class SubscribeRepoClass(TestCase):

    def test_valid_dates(self):
        cust = Customer()
        cust.cust_id = 1

        # New Date is > than cust.mod_date
        data = ['1', 'Snake', 'Plisken', '123 Fake St.', 'AZ', '12345', 'new', '432', 'Masthead', '100.12',
                '2021-02-05T16:30Z']
        cust.mod_date = parser.isoparse('2021-02-05T14:30Z')
        expected_result = True
        actual_result = helpers.valid_dates(cust, data)
        self.assertEqual(actual_result, expected_result)

        # New Date is < than cust.mod_date
        data = ['1', 'Snake', 'Plisken', '123 Fake St.', 'AZ', '12345', 'new', '432', 'Masthead', '100.12',
                '2021-02-02T16:30Z']
        cust.mod_date = parser.isoparse('2021-02-05T14:30Z')
        expected_result = False
        actual_result = helpers.valid_dates(cust, data)
        self.assertEqual(actual_result, expected_result)

        # New Date is == than cust.mod_date
        data = ['1', 'Snake', 'Plisken', '123 Fake St.', 'AZ', '12345', 'new', '432', 'Masthead', '100.12',
                '2021-02-05T14:30Z']
        cust.mod_date = parser.isoparse('2021-02-05T14:30Z')
        expected_result = False
        actual_result = helpers.valid_dates(cust, data)
        self.assertEqual(actual_result, expected_result)

    def test_valid_status(self):
        cust = Customer()
        cust.cust_id = 1

        cust2 = None

        # customer exists and status eq new
        cust.cust_change_in_purchase_status = 'canceled'
        data = ['1', 'Snake', 'Plisken', '123 Fake St.', 'AZ', '12345', 'new', '432', 'Masthead', '100.12',
                '2021-02-05T16:30Z']
        expected_result = False
        actual_result = helpers.valid_status(cust, data)
        self.assertEqual(actual_result, expected_result)

        # customer exists and status eq canceled
        cust.cust_change_in_purchase_status = 'new'
        data = ['1', 'Snake', 'Plisken', '123 Fake St.', 'AZ', '12345', 'canceled', '432', 'Masthead', '100.12',
                '2021-02-05T16:30Z']
        expected_result = True
        actual_result = helpers.valid_status(cust, data)
        self.assertEqual(actual_result, expected_result)

        # customer does not exist and status eq new
        data = ['1', 'Snake', 'Plisken', '123 Fake St.', 'AZ', '12345', 'new', '432', 'Masthead', '100.12',
                '2021-02-05T16:30Z']
        expected_result = True
        actual_result = helpers.valid_status(cust2, data)
        self.assertEqual(actual_result, expected_result)

        # customer does not exist and status eq canceled
        data = ['1', 'Snake', 'Plisken', '123 Fake St.', 'AZ', '12345', 'canceled', '432', 'Masthead', '100.12',
                '2021-02-05T16:30Z']

        expected_result = False
        actual_result = helpers.valid_status(cust2, data)
        self.assertEqual(actual_result, expected_result)

    @mock.patch('subscribe_repo.helpers.check_for_record')
    def test_parse_data(self, mock_check_for_record):

        # customer does not exists status eq new
        line = '1	Snake	Plisken	123 Fake St.	AZ	12345	new	432	Masthead	100.12	2021-02-03T16:30Z'
        cust = None
        mock_check_for_record.return_value = cust
        expected_result = {}
        actual_result = helpers.parse_subs(line)
        self.assertDictEqual(actual_result, expected_result)

        # customer does not exists status eq canceled
        line = '1	Snake	Plisken	123 Fake St.	AZ	12345	canceled	432	Masthead	100.12	2021-02-03T16:30Z'
        cust = None
        mock_check_for_record.return_value = cust
        expected_result = {'1': ['status is inconsistant']}
        actual_result = helpers.parse_subs(line)
        self.assertDictEqual(actual_result, expected_result)

        # customer exists status eq new
        line = '1	Snake	Plisken	123 Fake St.	AZ	12345	new	432	Masthead	100.12	2021-02-05T16:30Z'
        cust = Customer()
        cust.cust_id = 1
        cust.cust_change_in_purchase_status = 'new'
        cust.mod_date = parser.isoparse('2021-02-04T16:30Z')
        mock_check_for_record.return_value = cust

        actual_result = helpers.parse_subs(line)
        expected_result = {'1': ['status is inconsistant']}
        self.assertDictEqual(actual_result, expected_result)

        # customer exists status eq canceled
        line = '1	Snake	Plisken	123 Fake St.	AZ	12345	canceled	432	Masthead	100.12	2021-02-05T16:30Z'
        cust = Customer()
        cust.cust_id = 1
        cust.cust_change_in_purchase_status = 'canceled'
        cust.mod_date = parser.isoparse('2021-02-04T16:30Z')
        mock_check_for_record.return_value = cust
        actual_result = helpers.parse_subs(line)
        expected_result = {'1': ['status is inconsistant']}
        self.assertDictEqual(actual_result, expected_result)

        # customer exists date < current date
        line = '1	Snake	Plisken	123 Fake St.	AZ	12345	canceled	432	Masthead	100.12	2021-02-03T16:30Z'
        cust = Customer()
        cust.cust_id = 1
        cust.cust_change_in_purchase_status = 'new'
        cust.mod_date = parser.isoparse('2021-02-04T16:30Z')
        mock_check_for_record.return_value = cust
        actual_result = helpers.parse_subs(line)
        expected_result = {'1': ["current mod date <= date on update record"]}
        self.assertDictEqual(actual_result, expected_result)

        # customer exists date < current date and record status is cancelled
        line = '1	Snake	Plisken	123 Fake St.	AZ	12345	canceled	432	Masthead	100.12	2021-02-03T16:30Z'
        cust = Customer()
        cust.cust_id = 1
        cust.cust_change_in_purchase_status = 'canceled'
        cust.mod_date = parser.isoparse('2021-02-04T16:30Z')
        mock_check_for_record.return_value = cust
        actual_result = helpers.parse_subs(line)
        expected_result = {'1': ['current mod date <= date on update record', 'status is inconsistant']}
        self.assertDictEqual(actual_result, expected_result)

        # customer doesn't exist All data is good
        line = '1	Snake	Plisken	123 Fake St.	AZ	12345	new	432	Masthead	100.12	2021-02-03T16:30Z'
        cust = None
        mock_check_for_record.return_value = cust
        actual_result = helpers.parse_subs(line)
        expected_result = {}
        self.assertDictEqual(actual_result, expected_result)

    def test_update_error_dict(self):

        error_dict = {}
        cust_id = '1'

        # update with status error
        message = 'status is inconsistant'
        expected_result = {'1': ['status is inconsistant']}
        actual_result = helpers.update_error_dict(error_dict, cust_id, message)
        self.assertDictEqual(actual_result, expected_result)

        # update with date error
        error_dict = {}
        message = 'current mod date <= date on update record'
        expected_result = {'1': ['current mod date <= date on update record']}
        actual_result = helpers.update_error_dict(error_dict, cust_id, message)
        self.assertDictEqual(actual_result, expected_result)

        # update with both errors
        error_dict = {'1': ['current mod date <= date on update record']}
        message = 'status is inconsistant'
        expected_result = {'1': ['current mod date <= date on update record', 'status is inconsistant']}
        actual_result = helpers.update_error_dict(error_dict, cust_id, message)
        self.assertDictEqual(actual_result, expected_result)
