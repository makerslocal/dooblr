import logging
import influxdb
from influxdb.exceptions import InfluxDBClientError
from schema import Schema, And, Or, Optional, SchemaError
import six

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
