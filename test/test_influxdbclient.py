import unittest
from dooblr.influxdbclient import InfluxDBClient, DooblrInfluxDBError


class ValidateDataTestCase(unittest.TestCase):

    def test_validate_does_not_raise_error_with_all_data(self):
        data = {
            "measurement": "mymeasure",
            "fields": {"coolfield": 3},
            "tags": {"neattag": "tagalicious"}
        }
        try:
            InfluxDBClient._validate_data(data)
        except Exception as e:
            self.fail("Unexpected error was raised: {e}".format(e=e))

    def test_validate_does_not_raise_error_with_unicode_data(self):
        data = {
            u"measurement": u"mymeasure",
            u"fields": {u"coolfield": u"dfg"},
            u"tags": {u"neattag": u"tagalicious"}
        }
        try:
            InfluxDBClient._validate_data(data)
        except Exception as e:
            self.fail("Unexpected error was raised: {e}".format(e=e))

    def test_validate_does_not_raise_error_with_no_tags(self):
        data = {
            "measurement": "mymeasure",
            "fields": {"coolfield": 3}
        }
        try:
            InfluxDBClient._validate_data(data)
        except Exception as e:
            self.fail("Unexpected error was raised: {e}".format(e=e))

    def test_validate_does_not_raise_error_with_empty_tags(self):
        data = {
            "measurement": "mymeasure",
            "fields": {"coolfield": 3},
            "tags": {}
        }
        try:
            InfluxDBClient._validate_data(data)
        except Exception as e:
            self.fail("Unexpected error was raised: {e}".format(e=e))

    def test_validate_raises_error_with_nonstring_measurement(self):
        data = {
            "measurement": 3,
            "fields": {"coolfield": 3},
            "tags": {"neattag": "tagalicious"}
        }
        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._validate_data(data)

    def test_validate_raises_error_with_empty_measurement(self):
        data = {
            "measurement": "",
            "fields": {"coolfield": 3},
            "tags": {"neattag": "tagalicious"}
        }
        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._validate_data(data)

    def test_validate_raises_error_with_missing_measurement(self):
        data = {
            "fields": {"coolfield": 3},
            "tags": {"neattag": "tagalicious"}
        }
        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._validate_data(data)

    def test_validate_raises_error_with_empty_fields(self):
        data = {
            "measurement": "mymeasure",
            "fields": {},
            "tags": {"neattag": "tagalicious"}
        }
        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._validate_data(data)

    def test_validate_raises_error_with_missing_fields(self):
        data = {
            "measurement": "mymeasure",
            "tags": {"neattag": "tagalicious"}
        }
        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._validate_data(data)
