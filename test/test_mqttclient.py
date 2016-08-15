import unittest
from dooblr import mqttclient


class ParseMessageTestCase(unittest.TestCase):

    def test_fields_and_tags_are_parsed(self):
        client = mqttclient.MqttClient(None)
        client._measurements = {"environment":
                                    {"fields": ["temperature", "humidity"],
                                     "tags": ["location", "address"]
                                     }
                                }

        parsed = client._parse_message("environment", '{"temperature": 25.6, "humidity": 19.44, "location": "tool", "address": "1dec40"}')
        expected = {"measurement": "environment",
                    "fields": {"temperature": 25.6, "humidity": 19.44},
                    "tags": {"location": u"tool", "address": u"1dec40"}}
        self.assertEquals(parsed, expected)

    def test_missing_tag_raises_error(self):
        client = mqttclient.MqttClient(None)
        client._measurements = {"environment":
                                    {"fields": ["temperature"],
                                     "tags": ["location"]
                                     }
                                }
        with self.assertRaises(mqttclient.DooblrMqttError):
            client._parse_message("environment", '{"temperature": 25.6}')

    def test_missing_field_raises_error(self):
        client = mqttclient.MqttClient(None)
        client._measurements = {"environment":
                                    {"fields": ["temperature"],
                                     "tags": ["location"]
                                     }
                                }
        with self.assertRaises(mqttclient.DooblrMqttError):
            client._parse_message("environment", '{"location": "tool"}')