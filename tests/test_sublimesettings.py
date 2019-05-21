from unittest import TestCase
from unittest.mock import Mock, patch
from testglobals import kickassbuild

class TestSublimeSettings(TestCase):
    def setUp(self):
        self.command_mock = Mock()
        self.command_mock.window.project_data.return_value =  None
        self.command_mock.window.active_view.return_value.settings.return_value = {}
        self.target = kickassbuild.SublimeSettings(self.command_mock)

    def test_isLoaded_setting_exist_returns_true(self):
        self.command_mock.window.active_view.return_value.settings.return_value = {'kickass_output_path': 'value'}
        actual = kickassbuild.SublimeSettings(self.command_mock).isLoaded()
        self.assertEqual(True, actual)

    def test_isLoaded_setting_not_exist_returns_false(self):
        self.command_mock.window.active_view.return_value.settings.return_value = {'another_setting': 'value'}
        actual = kickassbuild.SublimeSettings(self.command_mock).isLoaded()
        self.assertEqual(False, actual)

    def test_isLoaded_nosettingsexist_returns_false(self):
        actual = self.target.isLoaded()
        self.assertEqual(False, actual)

    def test_getSetting_no_setting_sexist_returns_empty_string(self):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting')
        self.assertEqual('', actual)

    def test_getSettingas_parent_commandwindow_has_viewsetting_returns_viewsetting_value(self):
        self.command_mock.window.active_view.return_value.settings.return_value = {'test-setting': 'test-view-value'}
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting')
        self.assertEqual('test-view-value', actual)

    def test_getSettingas_parent_commandwindow_has_projectsetting_returns_project_setting_value(self):
        self.command_mock.window.project_data.return_value = {'settings': {'test-setting': 'test-project-value'}}
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting')
        self.assertEqual('test-project-value', actual)

    def test_getSettingas_parent_commandwindow_has_viewsetting_and_projectetting_returns_viewsetting_value(self):
        self.command_mock.window.active_view.return_value.settings.return_value = {'test-setting': 'test-view-value'}
        self.command_mock.window.project_data.return_value = {'settings': {'test-setting': 'test-project-value'}}
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting')
        self.assertEqual('test-view-value', actual)

    def test_getSettingas_parent_commandwindow_has_neither_viewsetting_or_projectsetting_return_empty_string(self):
        self.command_mock.window.active_view.return_value.settings.return_value = {'test-setting': 'test-view-value'}
        self.command_mock.window.project_data.return_value = {'settings': {'test-setting': 'test-project-value'}}
        actual = kickassbuild.SublimeSettings(self.command_mock).getSetting('test-setting1')
        self.assertEqual('', actual)

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value='true', autospec=True)
    def test_getSettingasbool_setting_value_is_true_returns_true(self, getSettings_mock):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')
        self.assertEqual(True, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value='TRUE', autospec=True)
    def test_getSettingasbool_setting_value_is_capital_true_returns_true(self, getSettings_mock):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')
        self.assertEqual(True, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value='false', autospec=True)
    def test_getSettingasbool_setting_value_is_false_returns_false(self, getSettings_mock):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')
        self.assertEqual(False, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value=None, autospec=True)
    def test_getSettingasbool_setting_value_is_none_raises_attributeerror(self, getSettings_mock):
        with self.assertRaisesRegexp(AttributeError, "'NoneType' object has no attribute 'lower'") as cm:
            actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')

    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings.getSetting', return_value='abc', autospec=True)
    def test_getSettingasbool_setting_value_is_abc_returns_false(self, getSettings_mock):
        actual = kickassbuild.SublimeSettings(self.command_mock).getSettingAsBool('any')
        self.assertEqual(False, actual)

if __name__ == '__main__':
    unittest.main()