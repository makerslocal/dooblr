import logging
import os.path
import yaml

DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".dooblr", "measurements")
DEFAULT_MAIN_CONFIG = {
    "global": {
        "config-dir": DEFAULT_CONFIG_DIR,
    },
    "mqtt": {
        "host": "localhost",
        "port": 1883,
    },
    "influxdb": {
        "host": "localhost",
        "port": 8086,
        "username": "root",
        "password": "root",
        "database": "dooblr",
    },
}


class DooblrConfigError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MainConfig(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._config = None
        self.mqtt_host = None
        self.mqtt_port = None
        self.influx_host = None
        self.influx_port = None
        self.influx_username = None
        self.influx_password = None
        self.influx_database = None
        self.config_dir = None

    def load(self, filepath):
        with open(filepath, 'r') as config_file:
            self._parse(config_file.read())

    def _parse(self, config_text):
        config = yaml.safe_load(config_text)

        if config is None:
            self._logger.warning("Main config was empty.")
            return

        self._config = self._dict_merge(config, DEFAULT_MAIN_CONFIG)

        self.mqtt_host = self._config["mqtt"].get("host")
        self.mqtt_port = self._config["mqtt"].get("port")

        self.influx_host = self._config["influxdb"].get("host")
        self.influx_port = self._config["influxdb"].get("port")
        self.influx_username = self._config["influxdb"].get("username")
        self.influx_password = self._config["influxdb"].get("password")
        self.influx_database = self._config["influxdb"].get("database")

        self.config_dir = self._config["global"].get("config-dir")

    # Made our own dict_merge because dict.update doesn't do sub trees
    def _dict_merge(self, user, default):
        if isinstance(user, dict) and isinstance(default, dict):
            for k, v in default.items():
                if k not in user:
                    user[k] = v
                else:
                    user[k] = self._dict_merge(user[k], v)
        return user

    @staticmethod
    def save_default_config(path):
        with open(path, 'w') as f:
            yaml.dump(DEFAULT_MAIN_CONFIG, f, default_flow_style=False)


class MeasurementConfig(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._config = None
        self.measurements = {}

    def load(self, filepath):
        with open(filepath, 'r') as config_file:
            self._parse(config_file.read())

    def _parse(self, config_text):
        self._config = yaml.safe_load(config_text)
        if self._config is None:
            self._logger.warning("Measurement config was empty.")
            return

        for measurement in self._config:
            self.measurements[measurement] = {}

            parser = self._config[measurement].get("parser", "json")
            self.measurements[measurement]["parser"] = parser

            if parser == "single-value":
                if "value_type" not in self._config[measurement]:
                    raise DooblrConfigError("Measurement {m} does not contain required property 'value_type'".format(
                        m=measurement))
                else:
                    if self._config[measurement]["value_type"] not in ["integer", "boolean", "string", "float"]:
                        raise DooblrConfigError("Value type '{t}' is not a valid value type, in measurement {m}".format(
                            t=self._config[measurement]["value_type"],
                            m=measurement))
                    else:
                        self.measurements[measurement]["value_type"] = self._config[measurement]["value_type"]

                if "topics" not in self._config[measurement]:
                    raise DooblrConfigError("Measurement {m} does not contain required property 'topics'".format(
                        m=measurement))
                else:
                    self.measurements[measurement]["topics"] = self._listify(self._config[measurement]["topics"])

                if "field_name" not in self._config[measurement]:
                    self._logger.info("Using default field name 'value' for measurement {m}".format(m=measurement))
                    self.measurements[measurement]["field_name"] = 'value'
                else:
                    self.measurements[measurement]["field_name"] = self._config[measurement]["field_name"]

            elif parser == "json":
                if "fields" not in self._config[measurement]:
                    raise DooblrConfigError("Measurement {m} does not contain required property 'fields'".format(
                        m=measurement))
                else:
                    self.measurements[measurement]["fields"] = self._listify(self._config[measurement]["fields"])

                if "topics" not in self._config[measurement]:
                    raise DooblrConfigError("Measurement {m} does not contain required property 'topics'".format(
                        m=measurement))
                else:
                    self.measurements[measurement]["topics"] = self._listify(self._config[measurement]["topics"])

                if "tags" not in self._config[measurement]:
                    self._logger.info("Measurement {m} does not contain optional property 'tags'".format(m=measurement))
                    self.measurements[measurement]["tags"] = []
                else:
                    self.measurements[measurement]["tags"] = self._listify(self._config[measurement]["tags"])

                if "optional_tags" not in self._config[measurement]:
                    self._logger.info("Measurement {m} does not contain optional property 'optional_tags'".format(
                        m=measurement))
                    self.measurements[measurement]["optional_tags"] = []
                else:
                    self.measurements[measurement]["optional_tags"] = self._listify(
                        self._config[measurement]["optional_tags"])

            else:
                raise DooblrConfigError("'{p}' is not a valid parser, in measurement {m}".format(
                    p=parser, m=measurement))

    @staticmethod
    def _listify(items):
        item_list = items
        if not isinstance(item_list, list):
            item_list = [items]
        return item_list

    @staticmethod
    def save_default_config(path):
        sample_config = {
            "my_measurement": {
                "fields": ["important_value"],
                "topics": ["dooblr/testing/device"],
                "tags": ["tag1", "tag2"],
                "optional_tags": ["option"]
            }}
        with open(path, 'w') as f:
            yaml.dump(sample_config, f, default_flow_style=False)
