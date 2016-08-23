from configparser import ConfigParser, NoOptionError, NoSectionError
from io import StringIO
import logging
import re
import os.path
import yaml


class DooblrConfigError(Exception):
    def __init__(self, *args,**kwargs):
        Exception.__init__(self, *args, **kwargs)


class MainConfig(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._config = ConfigParser()
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
            self._parse(yaml.safe_load(config_file))

    def _parse(self, config):
        self._config = config

        self.mqtt_host = self._get_with_default("mqtt", "host", default="localhost")
        self.mqtt_port = self._get_with_default("mqtt", "port", default=1883)

        self.influx_host = self._get_with_default("influxdb", "host", default="localhost")
        self.influx_port = self._get_with_default("influxdb", "port", default=8086)
        self.influx_username = self._get_with_default("influxdb", "username", default="root")
        self.influx_password = self._get_with_default("influxdb", "password", default="root")
        self.influx_database = self._get_with_default("influxdb", "database", default="dooblr")

        default_config_dir = os.path.join(os.path.expanduser("~"), ".dooblr", "measurements")
        self.config_dir = self._get_with_default("global", "config-dir", default=default_config_dir)

    def _get_with_default(self, section, option, default):
        try:
            #return self._config.get(section, option)
            return self._config[section][option]
        except KeyError:
            return default


class MeasurementConfig(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._config = ConfigParser()
        self.measurements = {}

    def load(self, filepath):
        with open(filepath, 'r') as config_file:
            self._parse(yaml.safe_load(config_file))

    def _parse(self, config):
        self._config = config

        for measurement in self._config:
            self.measurements[measurement] = {}

            if self._config[measurement]["fields"] is None:
                raise DooblrConfigError("Measurement {m} does not contain required option 'fields'".format(m=measurement))
            else:
                self.measurements[measurement]["fields"] = self._config[measurement]["fields"]

            if self._config[measurement]["topics"] is None:
                raise DooblrConfigError("Measurement {m} does not contain required option 'topics'".format(m=measurement))
            else:
                self.measurements[measurement]["topics"] = self._config[measurement]["topics"]

            if self._config[measurement]["tags"] is None:
                self._logger.info("Measurement {m} does not contain optional option 'tags'".format(m=measurement))
            else:
                self.measurements[measurement]["tags"] = self._config[measurement]["tags"]
