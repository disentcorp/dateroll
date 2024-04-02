import datetime
import os
import unittest

import dateroll.parser.parsers as parsers
from dateroll.date.date import Date
from dateroll.duration.duration import Duration
from dateroll.settings import Settings, default_settings_validation, path


class TestSettings(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_init(self):
        """
        test init of settings
        """

        # try removing so defaults are inherited
        os.remove(path)
        settings = Settings()
        self.assertEqual(settings.convention, "MDY")

    def test_load_validation_of_settings(self):
        """
        test the validation of settings
        """

        # load
        settings = Settings()
        # backup
        original = settings.convention

        # change /confirm
        settings.convention = "YMD"
        self.assertEqual(settings.convention, "YMD")

        # change /confirm
        settings.convention = "DMY"
        self.assertEqual(settings.convention, "DMY")

        # reset back to original
        settings.convention = original

    def test_setattr(self):
        """
        set bad attributes
        """
        settings = Settings()

        with self.assertRaises(Exception):
            settings.convention = "ABC"

    def test_repr(self):
        settings = Settings()
        x = repr(settings)

    def test_user_settings(self):
        ...
        # good key
        settings = Settings()
        backup = settings
        with open(path, "w") as f:
            f.write('convention="YMD"')

        settings = Settings()
        self.assertEqual(settings.convention, "YMD")
        settings = backup
        settings.save()

    def test_bad_settings(self):
        ...
        # bad key warns and ignores
        settings = Settings()
        backup = settings
        with self.assertWarns(Warning):
            with open(path, "w") as f:
                f.write("bad_setting=123")
            settings = Settings()
        settings = backup
        settings.save()

        # syntax error
        backup = settings
        with self.assertWarns(Warning):
            with open(path, "w") as f:
                f.write("/")
            settings = Settings()
        settings = backup
        settings.save()

    def test_validate_settings(self):
        sett = {'convention':False}
        settings = Settings()
        with self.assertRaises(Exception):
            settings.validate(sett)

if __name__ == "__main__":
    unittest.main()
