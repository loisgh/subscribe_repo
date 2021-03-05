from django.test import TestCase
from .models import Customer
from .record import Record
from subscribe_repo import helpers
from dateutil import parser
import mock


class SubscribeRepoClass(TestCase):
    def test_val_state(self):
        # Test with a valid State.
        rec = Record(
            "1",
            "first",
            "last",
            "addr",
            "NY",
            "12345",
            "status",
            "1",
            "prod_name",
            "12.34",
            "2021-02-05T16:30Z",
        )
        expected_result = True
        cust = Customer()
        actual_result = cust.val_state(rec)
        self.assertEqual(expected_result, actual_result)

        # Test with an invalid State.
        rec.state = "ZZ"
        expected_result = False
        actual_result = cust.val_state(rec)
        self.assertEqual(expected_result, actual_result)

    def test_val_zip(self):
        # Test with a valid zipcode
        rec = Record(
            "1",
            "first",
            "last",
            "addr",
            "NY",
            "12345",
            "status",
            "1",
            "prod_name",
            "12.34",
            "2021-02-05T16:30Z",
        )
        expected_result = True
        cust = Customer()
        actual_result = cust.val_zip(rec)
        self.assertEqual(expected_result, actual_result)

        # Test with a zipcode that's < 5 positions
        rec = Record(
            "1",
            "first",
            "last",
            "addr",
            "NY",
            "1234",
            "status",
            "1",
            "prod_name",
            "12.34",
            "2021-02-05T16:30Z",
        )
        expected_result = False
        cust = Customer()
        actual_result = cust.val_zip(rec)
        self.assertEqual(expected_result, actual_result)

        # Test with a zipcode that's not numeric
        rec = Record(
            "1",
            "first",
            "last",
            "addr",
            "NY",
            "ABCD5",
            "status",
            "1",
            "prod_name",
            "12.34",
            "2021-02-05T16:30Z",
        )
        expected_result = False
        cust = Customer()
        actual_result = cust.val_zip(rec)
        self.assertEqual(expected_result, actual_result)

        # Test with a zipcode that's not numeric and is < 5 positions
        rec = Record(
            "1",
            "first",
            "last",
            "addr",
            "NY",
            "ABCD",
            "status",
            "1",
            "prod_name",
            "12.34",
            "2021-02-05T16:30Z",
        )
        expected_result = False
        cust = Customer()
        actual_result = cust.val_zip(rec)
        self.assertEqual(expected_result, actual_result)

    def test_valid_dates(self):
        cust = Customer()
        cust.cust_id = 1

        # New Date is > than cust.mod_date
        rec = Record(
            "1",
            "Snake",
            "Plisken",
            "123 Fake St.",
            "AZ",
            "12345",
            "new",
            "432",
            "Masthead",
            "100.12",
            "2021-02-05T16:30Z",
        )
        cust.mod_date = parser.isoparse("2021-02-05T14:30Z")
        expected_result = True
        actual_result = cust.val_dates(cust, rec)
        self.assertEqual(actual_result, expected_result)

        # New Date is < than cust.mod_date
        rec = Record(
            "1",
            "Snake",
            "Plisken",
            "123 Fake St.",
            "AZ",
            "12345",
            "new",
            "432",
            "Masthead",
            "100.12",
            "2021-02-02T16:30Z",
        )
        cust.mod_date = parser.isoparse("2021-02-05T14:30Z")
        expected_result = False
        actual_result = cust.val_dates(cust, rec)
        self.assertEqual(actual_result, expected_result)

        # New Date is == than cust.mod_date
        rec = Record(
            "1",
            "Snake",
            "Plisken",
            "123 Fake St.",
            "AZ",
            "12345",
            "new",
            "432",
            "Masthead",
            "100.12",
            "2021-02-05T14:30Z",
        )
        cust.mod_date = parser.isoparse("2021-02-05T14:30Z")
        expected_result = False
        actual_result = cust.val_dates(cust, rec)
        self.assertEqual(actual_result, expected_result)

    def test_valid_status(self):

        cust = Customer()
        cust.cust_id = 1

        cust2 = Customer()

        # customer has invalid status
        rec = Record(
            "1",
            "Snake",
            "Plisken",
            "123 Fake St.",
            "AZ",
            "12345",
            "NEW",
            "432",
            "Masthead",
            "100.12",
            "2021-02-05T16:30Z",
        )
        expected_result = False
        actual_result = cust.val_status(cust, rec)
        self.assertEqual(actual_result, expected_result)

        # customer has invalid status
        rec = Record(
            "1",
            "Snake",
            "Plisken",
            "123 Fake St.",
            "AZ",
            "12345",
            "Blah",
            "432",
            "Masthead",
            "100.12",
            "2021-02-05T16:30Z",
        )
        expected_result = False
        actual_result = cust.val_status(cust, rec)
        self.assertEqual(actual_result, expected_result)

        # customer exists and status eq new
        cust.cust_change_in_purchase_status = "canceled"
        rec = Record(
            "1",
            "Snake",
            "Plisken",
            "123 Fake St.",
            "AZ",
            "12345",
            "new",
            "432",
            "Masthead",
            "100.12",
            "2021-02-05T16:30Z",
        )
        expected_result = False
        actual_result = cust.val_status(cust, rec)
        self.assertEqual(actual_result, expected_result)

        # customer exists and status eq canceled
        cust.cust_change_in_purchase_status = "new"
        rec = Record(
            "1",
            "Snake",
            "Plisken",
            "123 Fake St.",
            "AZ",
            "12345",
            "canceled",
            "432",
            "Masthead",
            "100.12",
            "2021-02-05T16:30Z",
        )
        expected_result = True
        actual_result = cust.val_status(cust, rec)
        self.assertEqual(actual_result, expected_result)

        # customer does not exist and status eq new
        rec = Record(
            "1",
            "Snake",
            "Plisken",
            "123 Fake St.",
            "AZ",
            "12345",
            "new",
            "432",
            "Masthead",
            "100.12",
            "2021-02-05T16:30Z",
        )
        expected_result = True
        actual_result = cust.val_status(cust2, rec)
        self.assertEqual(actual_result, expected_result)

        # customer does not exist and status eq canceled
        rec = Record(
            "1",
            "Snake",
            "Plisken",
            "123 Fake St.",
            "AZ",
            "12345",
            "canceled",
            "432",
            "Masthead",
            "100.12",
            "2021-02-05T16:30Z",
        )

        expected_result = False
        actual_result = cust.val_status(cust2, rec)
        self.assertEqual(actual_result, expected_result)

    @mock.patch("subscribe_repo.models.Customer.create_update_cust")
    @mock.patch("subscribe_repo.models.Customer.check_for_customer")
    def test_parse_data(self, mock_check_for_customer, mock_create_update_cust):

        # # customer does not exists status eq new
        infile = [
            b"1\tSnake\tPlisken\t123 Fake St.\tAZ\t12345\tnew\t432\tMasthead\t100.12\t2007-04-03T14:30Z\n"
        ]
        cust = Customer()
        mock_check_for_customer.return_value = cust
        expected_dict = {}
        expected_processed = 1
        actual_dict, actual_processed = helpers.parse_subs(infile)
        self.assertDictEqual(actual_dict, expected_dict)
        self.assertEqual(expected_processed, actual_processed)

        # customer does not exists status eq canceled
        infile = [
            b"1\tSnake\tPlisken\t123 Fake St.\tAZ\t12345\tcanceled\t432\tMasthead\t100.12\t2007-04-03T14:30Z\n"
        ]
        cust = Customer()
        mock_check_for_customer.return_value = cust
        expected_dict = {"1": ["status is inconsistant"]}
        expected_processed = 0
        actual_dict, actual_processed = helpers.parse_subs(infile)
        self.assertDictEqual(actual_dict, expected_dict)
        self.assertEqual(expected_processed, actual_processed)

        # customer exists status eq new
        infile = [
            b"1\tSnake\tPlisken\t123 Fake St.\tAZ\t12345\tnew\t432\tMasthead\t100.12\t2021-02-05T16:30Z\n"
        ]
        cust = Customer()
        cust.cust_id = 1
        cust.cust_change_in_purchase_status = "new"
        cust.mod_date = parser.isoparse("2021-02-04T16:30Z")
        mock_check_for_customer.return_value = cust
        actual_dict, actual_processed = helpers.parse_subs(infile)
        expected_dict = {"1": ["status is inconsistant"]}
        expected_processed = 0
        self.assertDictEqual(actual_dict, expected_dict)
        self.assertEqual(expected_processed, actual_processed)

        # customer exists status eq canceled
        infile = [
            b"1\tSnake\tPlisken\t123 Fake St.\tAZ\t12345\tcanceled\t432\tMasthead\t100.12\t2021-02-05T16:30Z\n"
        ]
        cust = Customer()
        cust.cust_id = 1
        cust.cust_change_in_purchase_status = "canceled"
        cust.mod_date = parser.isoparse("2021-02-04T16:30Z")
        mock_check_for_customer.return_value = cust
        actual_dict, actual_processed = helpers.parse_subs(infile)
        expected_dict = {"1": ["status is inconsistant"]}
        expected_processed = 0
        self.assertDictEqual(actual_dict, expected_dict)
        self.assertEqual(expected_processed, actual_processed)

        # customer exists date < current date
        infile = [
            b"1\tSnake\tPlisken\t123 Fake St.\tAZ\t12345\tcanceled\t432\tMasthead\t100.12\t2021-02-03T16:30Z\n"
        ]
        cust = Customer()
        cust.cust_id = 1
        cust.cust_change_in_purchase_status = "new"
        cust.mod_date = parser.isoparse("2021-02-04T16:30Z")
        mock_check_for_customer.return_value = cust
        actual_dict, actual_processed = helpers.parse_subs(infile)
        expected_dict = {"1": ["current mod date <= date on update record"]}
        expected_processed = 0
        self.assertDictEqual(actual_dict, expected_dict)
        self.assertEqual(expected_processed, actual_processed)

        # customer exists date < current date and record status is cancelled
        infile = [
            b"1\tSnake\tPlisken\t123 Fake St.\tAZ\t12345\tcanceled\t432\tMasthead\t100.12\t2021-02-03T16:30Z\n"
        ]
        cust = Customer()
        cust.cust_id = 1
        cust.cust_change_in_purchase_status = "canceled"
        cust.mod_date = parser.isoparse("2021-02-04T16:30Z")
        mock_check_for_customer.return_value = cust
        actual_dict, actual_processed = helpers.parse_subs(infile)
        expected_dict = {
            "1": ["current mod date <= date on update record", "status is inconsistant"]
        }
        self.assertDictEqual(actual_dict, expected_dict)
        self.assertEqual(expected_processed, actual_processed)

        # customer doesn't exist All data is good
        infile = [
            b"1\tSnake\tPlisken\t123 Fake St.\tAZ\t12345\tnew\t432\tMasthead\t100.12\t2021-02-03T16:30Z\n"
        ]
        cust = Customer()
        mock_check_for_customer.return_value = cust
        actual_dict, actual_processed = helpers.parse_subs(infile)
        expected_dict = {}
        expected_processed = 1
        self.assertDictEqual(actual_dict, expected_dict)
        self.assertEqual(expected_processed, actual_processed)

    def test_update_error_dict(self):

        error_dict = {}
        cust_id = "1"

        # update with status error
        message = "status is inconsistant"
        expected_result = {"1": ["status is inconsistant"]}
        actual_result = helpers.update_error_dict(error_dict, cust_id, message)
        self.assertDictEqual(actual_result, expected_result)

        # update with date error
        error_dict = {}
        message = "current mod date <= date on update record"
        expected_result = {"1": ["current mod date <= date on update record"]}
        actual_result = helpers.update_error_dict(error_dict, cust_id, message)
        self.assertDictEqual(actual_result, expected_result)

        # update with both errors
        error_dict = {"1": ["current mod date <= date on update record"]}
        message = "status is inconsistant"
        expected_result = {
            "1": ["current mod date <= date on update record", "status is inconsistant"]
        }
        actual_result = helpers.update_error_dict(error_dict, cust_id, message)
        self.assertDictEqual(actual_result, expected_result)
