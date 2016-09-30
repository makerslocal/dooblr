import unittest
from dooblr import mqttclient


class ParseMessageTestCase(unittest.TestCase):

    def test_good_message_is_parsed(self):
        client = mqttclient.MqttClient(None)
        client._measurements = {
            "environment": {
                    "fields": [
                        "temperature",
                        "humidity"
                    ],
                    "tags": [
                        "location",
                        "address"
                    ],
                    "optional_tags": [
                        "machine",
                        "label"
                    ]
                }
        }

        parsed = client._parse_message("environment", '{"temperature": 25.6, "humidity": 19.44, "location": "tool", "address": "1dec40", "machine": "ts9000", "label": "blue"}')
        expected = {"measurement": "environment",
                    "fields": {"temperature": 25.6, "humidity": 19.44},
                    "tags": {"location": u"tool", "address": u"1dec40", "machine": u"ts9000", "label": u"blue"}}
        self.assertEquals(parsed, expected)

    def test_missing_required_tag_raises_error(self):
        client = mqttclient.MqttClient(None)
        client._measurements = {
            "environment": {
                "fields": ["temperature"],
                "tags": ["location"]
            }
        }

        with self.assertRaises(mqttclient.DooblrMqttError):
            client._parse_message("environment", '{"temperature": 25.6}')

    def test_missing_optional_tag_does_not_raise_error(self):
        client = mqttclient.MqttClient(None)
        client._measurements = {
            "environment": {
                "fields": ["temperature"],
                "tags": ["location"],
                "optional_tags": ["machine_type"]
            }
        }

        try:
            client._parse_message("environment", '{"temperature": 25.6, "location":"kitchen"}')
        except Exception as e:
            self.fail("Unexpected error was raised: {e}".format(e=e))

    def test_missing_field_raises_error(self):
        client = mqttclient.MqttClient(None)
        client._measurements = {"environment":
                                    {"fields": ["temperature"],
                                     "tags": ["location"]
                                     }
                                }
        with self.assertRaises(mqttclient.DooblrMqttError):
            client._parse_message("environment", '{"location": "tool"}')
