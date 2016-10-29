import logging
import paho.mqtt.client as mqtt
import json


class DooblrMqttError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MqttClient(object):
    def __init__(self, callback):
        self._logger = logging.getLogger(__name__)
        self._paho_client = mqtt.Client()
        self._paho_client.on_message = self._on_message
        self._paho_client.on_subscribe = self._on_subscribe
        self._measurements = {}
        self._mid = {}
        self._callback = callback

    def connect(self, host, port):
        self._paho_client.connect(host, port=port)
        self._logger.info("Connected to broker: {h}:{p}".format(h=host, p=port))

    def loop(self, timeout=1.0):
        self._paho_client.loop(timeout=timeout)

    def register_measurement(self, name, topics, fields, tags, optional_tags):
        for topic in topics:
            result, mid = self._paho_client.subscribe(topic)
            if not result == mqtt.MQTT_ERR_SUCCESS:
                raise DooblrMqttError("Unable to subscribe to topic {t} for '{m}'".format(t=topic, m=name))
            self._mid[mid] = {'topic': topic, 'measurement': name}
        self._measurements[name] = {'topics': topics, 'fields': fields, 'tags': tags, 'optional_tags': optional_tags}

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        self._logger.debug("Registered measurement '{m}' on topics {t}".format(m=self._mid[mid]["measurement"],
                                                                               t=self._mid[mid]["topic"]))

    def _on_message(self, client, userdata, message):
        self._logger.debug("Received message on topic {t}: {m}".format(t=message.topic, m=message.payload))
        for measurement in self._measurements:
            for topic in self._measurements[measurement]["topics"]:
                if mqtt.topic_matches_sub(topic, message.topic):
                    try:
                        parsed_message = self._parse_message(measurement, message.payload)
                    except DooblrMqttError as e:
                        self._logger.error("Parsing failed: {e}".format(e=e))
                    else:
                        if not callable(self._callback):
                            self._logger.error("Callback is not callable.")
                        else:
                            self._callback(parsed_message)

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
                raise DooblrMqttError("Message does not contain required tag '{tag}'".format(tag=tag))

        for tag in measurement["optional_tags"]:
            try:
                parsed_message["tags"][tag] = message[tag]
            except KeyError:
                self._logger.info("Message does not contain optional tag '{tag}'".format(tag=tag))

        return parsed_message
