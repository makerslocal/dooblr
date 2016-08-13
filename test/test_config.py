import unittest
from dooblr.config import Config, DooblrConfigError


class ParseTestCase(unittest.TestCase):

    def test_missing_field_value_raises_error(self):
        config = Config()
        config_text = "\n".join((
                       "[measurement]",
                       "topics: ml256/topic/device",
                       "        ml256/topic/otherdevice",
                       "tags: supertag, awesometag"))
        with self.assertRaises(DooblrConfigError):
            config._parse(config_text)

    def test_missing_topic_value_raises_error(self):
        config = Config()
        config_text = "\n".join((
                       "[measurement]",
                       "fields: coolfield, neatfield",
                       "tags: supertag, awesometag"))
        with self.assertRaises(DooblrConfigError):
            config._parse(config_text)

    def test_missing_tag_value_does_not_raise_error(self):
        config = Config()
        config_text = "\n".join((
                       "[measurement]",
                       "topics: ml256/topic/device",
                       "        ml256/topic/otherdevice",
                       "fields: coolfield,neatfield"))
        try:
            config._parse(config_text)
        except DooblrConfigError as e:
            self.fail("Missing tag config raised an exception! ({e})".format(e=e))

    def test_valid_config_does_not_raise_error(self):
        config = Config()
        config_text = "\n".join((
                       "[measurement]",
                       "topics: ml256/topic/device",
                       "        ml256/topic/otherdevice",
                       "fields: coolfield, neatfield",
                       "tags: supertag, awesometag"))
        try:
            config._parse(config_text)
        except DooblrConfigError as e:
            self.fail("Valid config raised an exception! ({e})".format(e=e))

    def test_single_topic_is_parsed(self):
        config = Config()
        config_text = "\n".join((
                       "[measurement]",
                       "topics: ml256/topic/device",
                       "fields: coolfield, neatfield",
                       "tags: supertag, awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["topics"], ["ml256/topic/device"])

    def test_multiple_topics_are_parsed(self):
        config = Config()
        config_text = "\n".join((
                       "[measurement]",
                       "topics: ml256/topic/device",
                       "        ml256/topic/otherdevice",
                       "fields: coolfield, neatfield",
                       "tags: supertag, awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["topics"], ["ml256/topic/device", "ml256/topic/otherdevice"])

    def test_single_field_is_parsed(self):
        config = Config()
        config_text = "\n".join((
            "[measurement]",
            "topics: ml256/topic/device",
            "        ml256/topic/otherdevice",
            "fields: coolfield",
            "tags: supertag, awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["fields"], ["coolfield"])

    def test_multiple_fields_are_parsed(self):
        config = Config()
        config_text = "\n".join((
            "[measurement]",
            "topics: ml256/topic/device",
            "        ml256/topic/otherdevice",
            "fields: coolfield, neatfield",
            "tags: supertag, awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["fields"], ["coolfield", "neatfield"])

    def test_single_tag_is_parsed(self):
        config = Config()
        config_text = "\n".join((
                       "[measurement]",
                       "topics: ml256/topic/device",
                       "        ml256/topic/otherdevice",
                       "fields: coolfield, neatfield",
                       "tags: supertag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["tags"], ["supertag"])

    def test_multiple_tags_are_parsed(self):
        config = Config()
        config_text = "\n".join((
                       "[measurement]",
                       "topics: ml256/topic/device",
                       "        ml256/topic/otherdevice",
                       "fields: coolfield, neatfield",
                       "tags: supertag, awesometag"))

        config._parse(config_text)
        self.assertEquals(config.measurements["measurement"]["tags"], ["supertag", "awesometag"])


class ParseOptionTestCase(unittest.TestCase):
    def test_multiple_options_newlines_are_parsed(self):
        config = Config()
        option_text = "foo\n        bar"
        self.assertEquals(config._parse_option(option_text), ["foo", "bar"])

    def test_multiple_options_commas_are_parsed(self):
        config = Config()
        option_text = "foo, bar"
        self.assertEquals(config._parse_option(option_text), ["foo", "bar"])

    def test_multiple_options_commas_and_newlines_are_parsed(self):
        config = Config()
        option_text = "foo\n        bar, bah"
        self.assertEquals(config._parse_option(option_text), ["foo", "bar", "bah"])
