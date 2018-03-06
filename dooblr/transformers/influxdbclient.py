import logging
import influxdb
from influxdb.exceptions import InfluxDBClientError
from schema import Schema, And, Or, Optional, SchemaError
import six
import json

LOGGER = logging.getLogger(__name__)


class DooblrInfluxDBError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class InfluxDBClient(object):
    def __init__(self, host="localhost", port=8086, username="root", password="root", database="dooblr", dryrun=False):
        LOGGER.info("Connecting to InfluxDB at {h}:{p} as user {u}".format(h=host, p=port, u=username))
        self._client = influxdb.InfluxDBClient(host=host, port=port, username=username, password=password,
                                               database=database)
        self.dryrun = dryrun
        if not self.dryrun:
            try:
                self._client.create_database(database)
            except InfluxDBClientError as e:
                LOGGER.warning("Unable to create database '{db}': {e}".format(db=database, e=e))

    def write(self, data_dict):
        try:
            self._validate_data(data_dict)
        except SchemaError as e:
            LOGGER.error("Data in InfluxDB write() is not valid: {e}".format(e=e))
        if not self.dryrun:
            self._client.write_points([data_dict])

    @staticmethod
    def _validate_data(data_dict):
        schema = Schema({
            "measurement": And(Or(*six.string_types), len),
            "fields": And(dict, len),
            Optional("tags"): And(dict)
        })

        try:
            schema.validate(data_dict)
        except SchemaError as e:
            raise DooblrInfluxDBError(e)

    @staticmethod
    def _parse_message(measurement, message):
        if measurement["parser"] == "json":
            return InfluxDBClient._parse_json_message(measurement, message)
        elif measurement["parser"] == "single-value":
            return InfluxDBClient._parse_singlevalue_message(measurement, message)

    @staticmethod
    def _parse_json_message(measurement, message):
        try:
            message = json.loads(message)
        except ValueError:
            raise DooblrInfluxDBError("unable to decode json")

        if not isinstance(message, dict):
            raise DooblrInfluxDBError("message is not a json object")

        parsed_message = {"measurement": measurement["name"],
                          "fields": {},
                          "tags": {}}

        for field in measurement["fields"]:
            try:
                parsed_message["fields"][field] = message[field]
            except KeyError:
                raise DooblrInfluxDBError("Message does not contain field '{field}'".format(field=field))

        for tag in measurement["tags"]:
            try:
                parsed_message["tags"][tag] = message[tag]
            except KeyError:
                raise DooblrInfluxDBError("Message does not contain required tag '{tag}'".format(tag=tag))

        for tag in measurement["optional_tags"]:
            try:
                parsed_message["tags"][tag] = message[tag]
            except KeyError:
                LOGGER.info("Message does not contain optional tag '{tag}'".format(tag=tag))

        return parsed_message

    @staticmethod
    def _parse_singlevalue_message(measurement, message):
        parsed_message = {"measurement": measurement["name"],
                          "fields": {},
                          "tags": {}}

        if measurement["value_type"] == "integer":
            try:
                parsed_message["fields"][measurement["field_name"]] = int(message)
            except ValueError:
                raise DooblrInfluxDBError("Message {m} is not a valid integer".format(m=message))
        elif measurement["value_type"] == "float":
            try:
                parsed_message["fields"][measurement["field_name"]] = float(message)
            except ValueError:
                raise DooblrInfluxDBError("Message {m} is not a valid integer".format(m=message))
        elif measurement["value_type"] == "string":
            parsed_message["fields"][measurement["field_name"]] = message
        elif measurement["value_type"] == "boolean":
            if message.lower() in ['t', 'true', 'y', 'yes', 'on']:
                parsed_message["fields"][measurement["field_name"]] = True
            elif message.lower() in ['f', 'false', 'n', 'no', 'off']:
                parsed_message["fields"][measurement["field_name"]] = False
            else:
                raise DooblrInfluxDBError("Message {m} is not a valid boolean".format(m=message))

        return parsed_message
