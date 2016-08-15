from configparser import ConfigParser
from io import StringIO
import logging
import re


class DooblrConfigError(Exception):
    def __init__(self, *args,**kwargs):
        Exception.__init__(self, *args, **kwargs)


class Config(object):
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

