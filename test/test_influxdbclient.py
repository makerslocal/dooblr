import unittest
from dooblr.transformers import InfluxDBClient, DooblrInfluxDBError
from dooblr import mqttclient
import json


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


class ParseJsonMessageTestCase(unittest.TestCase):

    def test_good_message_is_parsed(self):
        measurement = {"name": "environment",
                       "fields": ["temperature", "humidity"],
                       "tags": ["location", "address"],
                       "optional_tags": ["machine", "label"],
                       "parser": "json"
        }
        message = '{"temperature": 25.6, "humidity": 19.44, "location": "tool", "address": "1dec40", "machine": "ts9000", "label": "blue"}'

        parsed = InfluxDBClient._parse_message(measurement, message)
        expected = {"measurement": "environment",
                    "fields": {"temperature": 25.6, "humidity": 19.44},
                    "tags": {"location": u"tool", "address": u"1dec40", "machine": u"ts9000", "label": u"blue"}}
        self.assertEquals(parsed, expected)

    def test_missing_required_tag_raises_error(self):
        measurement = {"name": "environment",
                       "fields": ["temperature"],
                       "tags": ["location"],
                       "parser": "json"
        }
        message = '{"temperature": 25.6}'

        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._parse_message(measurement, message)

    def test_missing_optional_tag_does_not_raise_error(self):
        measurement = {"name": "environment",
                       "fields": ["temperature"],
                       "tags": ["location"],
                       "optional_tags": ["machine_type"],
                       "parser": "json"
        }
        message = '{"temperature": 25.6, "location":"kitchen"}'

        try:
            InfluxDBClient._parse_message(measurement, message)
        except Exception as e:
            self.fail("Unexpected error was raised: {e}".format(e=e))

    def test_missing_field_raises_error(self):
        measurement = {"name": "environment",
                       "fields": ["temperature"],
                       "tags": ["location"],
                       "parser": "json"
        }
        message = '{"location": "tool"}'

        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._parse_message(measurement, message)

class ParseSingleValueMessageTestCase(unittest.TestCase):

    def test_integer_is_parsed(self):
        measurement = {"name": "environment",
                       "value_type": "integer",
                       "parser": "single-value",
                       "field_name": "value"
        }
        message = '13'

        parsed = InfluxDBClient._parse_message(measurement, message)
        expected = {"measurement": "environment",
                    "fields": {"value": 13},
                    "tags": {}}
        self.assertEquals(parsed, expected)

    def test_bad_integer_raises_error(self):
        measurement = {"name": "environment",
                       "value_type": "integer",
                       "parser": "single-value",
                       "field_name": "value"
        }
        message = 'blah'

        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._parse_message(measurement, message)

    def test_float_is_parsed(self):
        measurement = {"name": "environment",
                       "value_type": "float",
                       "parser": "single-value",
                       "field_name": "value"
        }
        message = '13.37'

        parsed = InfluxDBClient._parse_message(measurement, message)
        expected = {"measurement": "environment",
                    "fields": {"value": 13.37},
                    "tags": {}}
        self.assertEquals(parsed, expected)

    def test_bad_float_raises_error(self):
        measurement = {"name": "environment",
                       "value_type": "float",
                       "parser": "single-value",
                       "field_name": "value"
        }
        message = 'blah'

        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._parse_message(measurement, message)

    def test_string_is_parsed(self):
        measurement = {"name": "environment",
                       "value_type": "string",
                       "parser": "single-value",
                       "field_name": "value"
        }
        message = 'test'

        parsed = InfluxDBClient._parse_message(measurement, message)
        expected = {"measurement": "environment",
                    "fields": {"value": "test"},
                    "tags": {}}
        self.assertEquals(parsed, expected)

    def test_bool_false_is_parsed(self):
        measurement = {"name": "environment",
                       "value_type": "boolean",
                       "parser": "single-value",
                       "field_name": "value"
        }
        message = 'FaLsE'

        parsed = InfluxDBClient._parse_message(measurement, message)
        expected = {"measurement": "environment",
                    "fields": {"value": False},
                    "tags": {}}
        self.assertEquals(parsed, expected)

    def test_bool_f_is_parsed(self):
        measurement = {"name": "environment",
                       "value_type": "boolean",
                       "parser": "single-value",
                       "field_name": "value"
        }
        message = 'F'

        parsed = InfluxDBClient._parse_message(measurement, message)
        expected = {"measurement": "environment",
                    "fields": {"value": False},
                    "tags": {}}
        self.assertEquals(parsed, expected)

    def test_bad_bool_raises_error(self):
        measurement = {"name": "environment",
                       "value_type": "boolean",
                       "parser": "single-value",
                       "field_name": "value"
        }
        message = 'not-true'

        with self.assertRaises(DooblrInfluxDBError):
            InfluxDBClient._parse_message(measurement, message)
