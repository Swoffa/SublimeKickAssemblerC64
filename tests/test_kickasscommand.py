import sublime
import sys
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch, create_autospec
from module_references import kickassbuild

class TestKickAssCommand(TestCase):

    def test_commandText_returns_commandtext(self):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommand('TestCommandText', False, False, 'build')
        actual = target.CommandText
        self.assertEqual('TestCommandText', actual)

    def test_ctor_fields_are_set(self):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        actual = kickassbuild.KickAssCommand('TestCommandText', False, True, 'build')
        self.assertEqual('TestCommandText', actual._KickAssCommand__commandText) #Not best practice to test "private" fields...
        self.assertEqual(False, actual._KickAssCommand__hasPreCommand)
        self.assertEqual(True, actual._KickAssCommand__hasPostCommand)
        self.assertEqual('build', actual._KickAssCommand__buildMode)

    def test_updateEnvVars_has_precommand_is_false_and_haspostcommand_is_false_returns_unchanged_dict(self):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommand('TestCommandText', False, False, 'build')
        sourceDict = {'env': {'a': 'b'}}
        actual = target.updateEnvVars(sourceDict)
        self.assertEqual({'env': {'a': 'b'}}, actual)

    def test_updateEnvVars_has_precommand_is_true_and_haspostcommand_is_false_returns_dict_with_envvars(self):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommand('TestCommandText', True, False, 'build')
        sourceDict = {'env': {'a': 'b'}}
        expected = {'env': {'kickass_bin_folder': '${file_path}/${kickass_output_path}', 'kickass_prg_file': '${file_path}/${kickass_output_path}/${kickass_compiled_filename}', 'kickass_file': '${build_file_base_name}.${file_extension}', 'kickass_file_path': '${file_path}', 'a': 'b', 'kickass_buildmode': 'build'}}
        actual = target.updateEnvVars(sourceDict)
        self.assertEqual(expected, actual)

    def test_updateEnvVars_has_precommand_is_false_and_haspostcommand_is_true_returns_dict_with_envvars(self):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommand('TestCommandText', False, True, 'build')
        sourceDict = {'env': {'a': 'b'}}
        expected = {'env': {'kickass_bin_folder': '${file_path}/${kickass_output_path}', 'kickass_prg_file': '${file_path}/${kickass_output_path}/${kickass_compiled_filename}', 'kickass_file': '${build_file_base_name}.${file_extension}', 'kickass_file_path': '${file_path}', 'a': 'b', 'kickass_buildmode': 'build'}}
        actual = target.updateEnvVars(sourceDict)
        self.assertEqual(expected, actual)

    def test_updateEnvVars_has_precommand_is_true_and_haspostcommand_is_true_returns_dict_with_envvars(self):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommand('TestCommandText', True, True, 'build')
        sourceDict = {'env': {'a': 'b'}}
        expected = {'env': {'kickass_bin_folder': '${file_path}/${kickass_output_path}', 'kickass_prg_file': '${file_path}/${kickass_output_path}/${kickass_compiled_filename}', 'kickass_file': '${build_file_base_name}.${file_extension}', 'kickass_file_path': '${file_path}', 'a': 'b', 'kickass_buildmode': 'build'}}
        actual = target.updateEnvVars(sourceDict)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()