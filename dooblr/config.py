from configparser import ConfigParser, NoOptionError, NoSectionError
from io import StringIO
import logging
import re
import os.path


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
            self._parse(unicode(config_file.read()))

    def _parse(self, config_text):
        fileish_string = StringIO(config_text)
        self._config.read_file(fileish_string)

        self.mqtt_host = self._get_with_default("mqtt", "host", default="localhost")
        self.mqtt_port = self._get_with_default("mqtt", "port", default=1883)

        self.influx_host = self._get_with_default("influxdb", "host", default="localhost")
        self.influx_port = self._get_with_default("influxdb", "port", default=8086)
        self.influx_username = self._get_with_default("influxdb", "username", default="root")
        self.influx_password = self._get_with_default("influxdb", "password", default="root")
        self.influx_database = self._get_with_default("influxdb", "database", default="dooblr")

        default_config_dir = os.path.join(os.path.expanduser("~"), ".dooblr", "measurements")
        self.config_dir = self._get_with_default("globaL", "config-dir", default=default_config_dir)

    def _get_with_default(self, section, option, default):
        try:
            return self._config.get(section, option)
        except (NoSectionError, NoOptionError):
            return default


class MeasurementConfig(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._config = ConfigParser()
        self.measurements = {}

    def load(self, filepath):
        with open(filepath, 'r') as config_file:
            self._parse(unicode(config_file.read()))

    def _parse(self, config_text):
        fileish_string = StringIO(config_text)
        self._config.read_file(fileish_string)

        for measurement in self._config.sections():
            self.measurements[measurement] = {}
            if not self._config.has_option(measurement, "fields"):
                raise DooblrConfigError("Measurement {m} does not contain required option 'fields'".format(m=measurement))
            else:
                self.measurements[measurement]["fields"] = self._parse_option(self._config.get(measurement, "fields"))

            if not self._config.has_option(measurement, "topics"):
                raise DooblrConfigError("Measurement {m} does not contain required option 'topics'".format(m=measurement))
            else:
                self.measurements[measurement]["topics"] = self._parse_option(self._config.get(measurement, "topics"))

            if not self._config.has_option(measurement, "tags"):
                self._logger.info("Measurement {m} does not contain optional option 'tags'".format(m=measurement))
            else:
                self.measurements[measurement]["tags"] = self._parse_option(self._config.get(measurement, "tags"))

    @staticmethod
    def _parse_option(option_string):
        return re.split(r'[\s,]+', option_string)

