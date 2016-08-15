import logging
import paho.mqtt.client as mqtt
import json


class DooblrMqttError(Exception):
    def __init__(self, *args,**kwargs):
        Exception.__init__(self, *args, **kwargs)


class MqttClient(object):
    def __init__(self, callback):
        self._logger = logging.getLogger(__name__)
        self._paho_client = mqtt.Client()
        self._measurements = {}
        self._callback = callback

    def _parse_message(self, measurement_name, message_string):
        parsed_message = {"measurement": measurement_name,
                          "fields": {},
                          "tags": {}}
        try:
            message = json.loads(message_string)
        except ValueError:
            raise DooblrMqttError("Unable to decode json for {message}".format(message=message_string))

        measurement = self._measurements[measurement_name]

        for field in measurement["fields"]:
            try:
                parsed_message["fields"][field] = message[field]
            except KeyError:
                raise DooblrMqttError("Message does not contain field '{field}'".format(field=field))

        for tag in measurement["tags"]:
            try:
                parsed_message["tags"][tag] = message[tag]
            except KeyError:
                raise DooblrMqttError("Message does not contain tag '{field}'".format(field=tag))

        return parsed_message