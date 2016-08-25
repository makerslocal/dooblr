from configparser import ConfigParser, NoOptionError, NoSectionError
from io import StringIO
import logging
import re
import os.path
import yaml

DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".dooblr", "measurements")
DEFUALT_MAIN_CONFIG = {
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
    def __init__(self, *args,**kwargs):
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
            self._parse(unicode(config_file.read()))

    def _parse(self, config_text):
        config = yaml.safe_load(config_text)
        self._config = self._dict_merge(config, DEFUALT_MAIN_CONFIG)
        print(self._config)

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
        if isinstance(user,dict) and isinstance(default,dict):
            for k,v in default.iteritems():
                if k not in user:
                    user[k] = v
                else:
                    user[k] = self._dict_merge(user[k],v)
        return user


class MeasurementConfig(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._config = ConfigParser()
        self.measurements = {}

    def load(self, filepath):
        with open(filepath, 'r') as config_file:
            self._parse(unicode(config_file.read()))

    def _parse(self, config_text):
        self._config = yaml.safe_load(config_text)

        for measurement in self._config:
            self.measurements[measurement] = {}

            if "fields" not in self._config[measurement]:
                raise DooblrConfigError("Measurement {m} does not contain required option 'fields'".format(m=measurement))
            else:
                self.measurements[measurement]["fields"] = self._listify(self._config[measurement]["fields"])

            if "topics" not in self._config[measurement]:
                raise DooblrConfigError("Measurement {m} does not contain required option 'topics'".format(m=measurement))
            else:
                self.measurements[measurement]["topics"] = self._listify(self._config[measurement]["topics"])

            if "tags" not in self._config[measurement]:
                self._logger.info("Measurement {m} does not contain optional option 'tags'".format(m=measurement))
            else:
                self.measurements[measurement]["tags"] = self._listify(self._config[measurement]["tags"])

    def _listify(self, items):
        item_list = items
        if not isinstance(item_list, list):
            item_list = [items]
        return item_list
