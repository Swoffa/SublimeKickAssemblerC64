import sublime
import sys
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch
from module_references import kickassbuild

class TestSublimeSettings(TestCase):
    def setUp(self):
        self.command_mock = Mock()
        self.command_mock.window.project_data.return_value =  None
        self.command_mock.window.active_view.return_value.settings.return_value = {}
        self.target = kickassbuild.SublimeSettings(self.command_mock)

    def test_isLoaded_settingexist_returns_true(self):
        view_settings = {'kickass_output_path': 'value'}
        self.command_mock.window.active_view.return_value.settings.return_value = view_settings
        self.target = kickassbuild.SublimeSettings(self.command_mock)
        actual = self.target.isLoaded()
        self.assertEqual(True, actual)

    def test_isLoaded_settingnotexist_returns_false(self):
        view_settings = {'another_setting': 'value'}
        self.command_mock.window.active_view.return_value.settings.return_value = view_settings
        self.target = kickassbuild.SublimeSettings(self.command_mock)
        actual = self.target.isLoaded()
        self.assertEqual(False, actual)

    def test_isLoaded_nosettingsexist_returns_false(self):
        actual = self.target.isLoaded()
        self.assertEqual(False, actual)

    def test_getSetting_settingexist_returnsettingvalue(self):
        view_settings = {'test-setting': 'test-value'}
        self.command_mock.window.active_view.return_value.settings.return_value = view_settings
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting("test-setting")
        self.assertEqual("test-value", actual)

    def test_getSetting_settingnotexist_returnemptystring(self):
        view_settings = {'test-setting': 'test-value'}
        self.command_mock.window.active_view.return_value.settings.return_value = view_settings
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting("test-setting2")
        self.assertEqual('', actual)

    def test_getSetting_nosettingsnotexist_returnemptystring(self):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting("test-settingp")
        self.assertEqual('', actual)

if __name__ == '__main__':
    unittest.main()