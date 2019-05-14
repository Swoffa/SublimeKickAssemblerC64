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

    def test_isLoaded_setting_exist_returns_true(self):
        view_settings = {'kickass_output_path': 'value'}
        self.command_mock.window.active_view.return_value.settings.return_value = view_settings
        self.target = kickassbuild.SublimeSettings(self.command_mock)
        actual = self.target.isLoaded()
        self.assertEqual(True, actual)

    def test_isLoaded_setting_not_exist_returns_false(self):
        view_settings = {'another_setting': 'value'}
        self.command_mock.window.active_view.return_value.settings.return_value = view_settings
        self.target = kickassbuild.SublimeSettings(self.command_mock)
        actual = self.target.isLoaded()
        self.assertEqual(False, actual)

    def test_isLoaded_nosettingsexist_returns_false(self):
        actual = self.target.isLoaded()
        self.assertEqual(False, actual)

    def test_getSetting_no_setting_sexist_returns_empty_string(self):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting')
        self.assertEqual('', actual)

    def test_getSettingas_parent_commandwindow_has_viewsetting_returns_viewsetting_value(self):
        view_settings = {'test-setting': 'test-view-value'}
        self.command_mock.window.active_view.return_value.settings.return_value = view_settings
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting')
        self.assertEqual('test-view-value', actual)

    def test_getSettingas_parent_commandwindow_has_projectsetting_returns_project_setting_value(self):
        project_settings = {'test-setting': 'test-project-value'}
        self.command_mock.window.project_data.return_value = {'settings': project_settings}
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting')
        self.assertEqual('test-project-value', actual)

    def test_getSettingas_parent_commandwindow_has_viewsetting_and_projectetting_returns_viewsetting_value(self):
        view_settings = {'test-setting': 'test-view-value'}
        project_settings = {'test-setting': 'test-project-value'}
        self.command_mock.window.active_view.return_value.settings.return_value = view_settings
        self.command_mock.window.project_data.return_value = {'settings': project_settings}
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting')
        self.assertEqual('test-view-value', actual)

    def test_getSettingas_parent_commandwindow_has_neither_viewsetting_or_projectsetting_return_empty_string(self):
        view_settings = {'test-setting': 'test-view-value'}
        project_settings = {'test-setting': 'test-project-value'}
        self.command_mock.window.active_view.return_value.settings.return_value = view_settings
        self.command_mock.window.project_data.return_value = {'settings': project_settings}
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting1')
        self.assertEqual('', actual)

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value='true')
    def test_getSettingasbool_setting_value_is_true_returns_true(self, getSettings_mock):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')
        self.assertEqual(True, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value='TRUE')
    def test_getSettingasbool_setting_value_is_capital_true_returns_true(self, getSettings_mock):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')
        self.assertEqual(True, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value='false')
    def test_getSettingasbool_setting_value_is_false_returns_false(self, getSettings_mock):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')
        self.assertEqual(False, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value=None)
    def test_getSettingasbool_setting_value_is_none_raises_attributeerror(self, getSettings_mock):
        with self.assertRaises(AttributeError) as cm:
            actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value='abc')
    def test_getSettingasbool_setting_value_is_abc_returns_false(self, getSettings_mock):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')
        self.assertEqual(False, actual)

if __name__ == '__main__':
    unittest.main()