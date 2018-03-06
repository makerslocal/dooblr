import logging
import paho.mqtt.client as mqtt
from dooblr.transformers.influxdbclient import DooblrInfluxDBError


class DooblrMqttError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MqttClient(object):
    def __init__(self, callback, influx_transformer):
        self._logger = logging.getLogger(__name__)
        self._paho_client = mqtt.Client()
        self._paho_client.on_message = self._on_message
        self._paho_client.on_subscribe = self._on_subscribe
        self._measurements = {}
        self._mid = {}
        self._callback = callback
        self._influx_transformer = influx_transformer

    def connect(self, host, port):
        self._paho_client.connect(host, port=port)
        self._logger.info("Connected to broker: {h}:{p}".format(h=host, p=port))

    def loop(self, timeout=1.0):
        self._paho_client.loop(timeout=timeout)

    def register_measurement(self, name, measurement):
        for topic in measurement["topics"]:
            result, mid = self._paho_client.subscribe(topic)
            if not result == mqtt.MQTT_ERR_SUCCESS:
                raise DooblrMqttError("Unable to subscribe to topic {t} for '{m}'".format(t=topic, m=name))
            self._mid[mid] = {'topic': topic, 'measurement': name}
        self._measurements[name] = measurement
        self._measurements[name]["name"] = name

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        self._logger.debug("Registered measurement '{m}' on topics {t}".format(m=self._mid[mid]["measurement"],
                                                                               t=self._mid[mid]["topic"]))

    def _on_message(self, client, userdata, message):
        self._logger.debug("Received message on topic {t}: {m}".format(t=message.topic, m=message.payload))
        for measurement_name in self._measurements:
            for topic in self._measurements[measurement_name]["topics"]:
                if mqtt.topic_matches_sub(topic, message.topic):
                    measurement = self._measurements[measurement_name]
                    try:
                        parsed_message = self._influx_transformer._parse_message(measurement, message.payload)
                    except DooblrInfluxDBError as e:
                        self._logger.error("Parsing failed for message: {e}".format(t=message.topic, e=e))
                    else:
                        if not callable(self._callback):
                            self._logger.error("Callback is not callable.")
                        else:
                            self._callback(parsed_message)
