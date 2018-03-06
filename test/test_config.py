import unittest
from dooblr.config import MeasurementConfig, MainConfig, DooblrConfigError


class MainConfigParseTestCase(unittest.TestCase):

    def test_empty_section_does_not_raise_error(self):
        config = MainConfig()
        config_text = u""
        try:
            config._parse(config_text)
        except Exception as e:
            self.fail("Missing config option raised an exception! ({e})".format(e=e))

    def test_partial_section_does_not_raise_error(self):
        config = MainConfig()
        config_text = "\n".join((
            u"mqtt:",
            "  host: blah"))
        try:
            config._parse(config_text)
        except Exception as e:
            self.fail("Missing config option raised an exception! ({e})".format(e=e))

class MeasurementConfigTestCase(unittest.TestCase):
    def test_invalid_parser_raises_error(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: bad-parser"))
        with self.assertRaises(DooblrConfigError):
            config._parse(config_text)


class MeasurementConfigParseJsonTestCase(unittest.TestCase):

    def test_missing_field_value_raises_error(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice",
            "  tags:",
            "    - supertag",
            "    - awesometag"))
        with self.assertRaises(DooblrConfigError):
            config._parse(config_text)

    def test_missing_topic_value_raises_error(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  fields:",
            "    - coolfield",
            "    - neatfield",
            "  tags: ",
            "    - supertag",
            "    - awesometag"))
        with self.assertRaises(DooblrConfigError):
            config._parse(config_text)

    def test_missing_tag_value_does_not_raise_error(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice",
            "  fields:",
            "    - coolfield",
            "    - neatfield"))
        try:
            config._parse(config_text)
        except DooblrConfigError as e:
            self.fail("Missing tag config raised an exception! ({e})".format(e=e))

    def test_valid_config_does_not_raise_error(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice",
            "  fields: ",
            "    - coolfield",
            "    - neatfield",
            "  tags: ",
            "    - supertag",
            "    - awesometag"))
        try:
            config._parse(config_text)
        except DooblrConfigError as e:
            self.fail("Valid config raised an exception! ({e})".format(e=e))

    def test_single_optional_tag_is_parsed(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "  fields: ",
            "    - coolfield",
            "  optional_tags: ",
            "    - optiontag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["optional_tags"], ["optiontag"])

    def test_no_optional_tags_acts_as_empty_list(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "  fields: ",
            "    - coolfield"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["optional_tags"], [])

    def test_multiple_optional_tags_are_parsed(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "  fields: ",
            "    - coolfield",
            "  optional_tags: ",
            "    - optiontag",
            "    - label"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["optional_tags"], ["optiontag", "label"])

    def test_single_topic_is_parsed(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics: ml256/topic/device",
            "  fields: ",
            "    - coolfield",
            "    - neatfield",
            "  tags: ",
            "    - supertag",
            "    - awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["topics"], ["ml256/topic/device"])

    def test_multiple_topics_are_parsed(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice",
            "  fields: ",
            "    - coolfield",
            "    - neatfield",
            "  tags: ",
            "    - supertag",
            "    - awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["topics"], ["ml256/topic/device", "ml256/topic/otherdevice"])

    def test_single_field_is_parsed(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice",
            "  fields: coolfield",
            "  tags: ",
            "    - supertag",
            "    - awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["fields"], ["coolfield"])

    def test_multiple_fields_are_parsed(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice",
            "  fields:",
            "    - coolfield",
            "    - neatfield",
            "  tags:",
            "    - supertag",
            "    - awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["fields"], ["coolfield", "neatfield"])

    def test_single_tag_is_parsed(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice",
            "  fields:",
            "    - coolfield",
            "    - neatfield",
            "  tags: supertag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["tags"], ["supertag"])

    def test_multiple_tags_are_parsed(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice",
            "  fields:",
            "    - coolfield",
            "    - neatfield",
            "  tags:",
            "    - supertag",
            "    - awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["tags"], ["supertag", "awesometag"])

    def test_explicit_json_parser(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: json",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice",
            "  fields: ",
            "    - coolfield",
            "    - neatfield",
            "  tags: ",
            "    - supertag",
            "    - awesometag"))
        try:
            config._parse(config_text)
        except DooblrConfigError as e:
            self.fail("Valid config raised an exception! ({e})".format(e=e))

class MeasurementConfigParseSingleValueTestCase(unittest.TestCase):

    def test_singlevalue_parser_default_field(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: single-value",
            "  value_type: integer",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["field_name"], "value")

    def test_singlevalue_parser_custom_field(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: single-value",
            "  value_type: integer",
            "  field_name: foo",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["field_name"], "foo")

    def test_singlevalue_parser_without_valuetype_raises_error(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: single-value",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice"))

        with self.assertRaises(DooblrConfigError):
            config._parse(config_text)

    def test_singlevalue_parser_with_bad_valuetype_raises_error(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: single-value",
            "  value_type: nonsense",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice"))

        with self.assertRaises(DooblrConfigError):
            config._parse(config_text)

    def test_singlevalue_parser_integer_type(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: single-value",
            "  value_type: integer",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["value_type"], "integer")

    def test_singlevalue_parser_float_type(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: single-value",
            "  value_type: float",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["value_type"], "float")

    def test_singlevalue_parser_string_type(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: single-value",
            "  value_type: string",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["value_type"], "string")

    def test_singlevalue_parser_boolean_type(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: single-value",
            "  value_type: boolean",
            "  topics:",
            "    - ml256/topic/device",
            "    - ml256/topic/otherdevice"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["value_type"], "boolean")

    def test_missing_topic_value_raises_error(self):
        config = MeasurementConfig()
        config_text = "\n".join((
            u"measurement:",
            "  parser: single-value",
            "  value_type: boolean"))

        with self.assertRaises(DooblrConfigError):
            config._parse(config_text)
