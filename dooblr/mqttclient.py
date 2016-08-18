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
        self._paho_client.on_message = self._on_message
        self._measurements = {}
        self._callback = callback

    def connect(self, host, port):
        self._paho_client.connect(host, port=port)
        self._logger.info("Connected to broker: {h}:{p}".format(h=host, p=port))

    def loop(self, timeout=1.0):
        self._paho_client.loop(timeout=timeout)

    def register_measurement(self, name, topics, fields, tags):
        for topic in topics:
            result, _ = self._paho_client.subscribe(topic)
            if not result == mqtt.MQTT_ERR_SUCCESS:
                raise DooblrMqttError("Unable to subscribe to topic {t} for '{m}'".format(t=topic, m=name))
        self._measurements[name] = {'topics': topics, 'fields': fields, 'tags': tags}
        self._logger.debug("Registered measurement '{m}' on topics {t}".format(m=name, t=topics))

    def _on_message(self, client, userdata, message):
        self._logger.debug("Received message on topic {t}: {m}".format(t=message.topic, m=message.payload))
        for measurement in self._measurements:
            for topic in self._measurements[measurement]["topics"]:
                if mqtt.topic_matches_sub(message.topic, topic):
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
                raise DooblrMqttError("Message does not contain tag '{field}'".format(field=tag))

        return parsed_message
