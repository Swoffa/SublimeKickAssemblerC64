from unittest import TestCase
from unittest.mock import Mock, patch, create_autospec, PropertyMock
from testsettings import TestSettings
from testglobals import kickassbuild, default_settings_dict, default_variables_dict, mock_open34, CopyingMock

def createCommand_mock(command_text='test-command-text'):
    return fix_createCommand_mock(create_autospec(kickassbuild.KickAssCommand), command_text)

def fix_createCommand_mock(mock, command_text='test-command-text'):
    mock.updateEnvVars.side_effect = (lambda dict: dict)
    type(mock).CommandText = PropertyMock(return_value=command_text)
    return mock

class TestKickassBuildCommand(TestCase):

    def setUp(self):
        self.platform_system_patch = patch('platform.system', autospec=True)
        self.platform_system = self.platform_system_patch.start()
        self.platform_system.return_value = 'Darwin'

        self.window_mock = Mock()
        self.window_mock.extract_variables.return_value = default_variables_dict.copy()

        self.settings_mock = create_autospec(kickassbuild.SublimeSettings)
        self.settings_mock.getSetting.return_value = ''

        self.all_settings = TestSettings(default_settings_dict)

        self.target = kickassbuild.KickassBuildCommand(self.window_mock)

        self.maxDiff = None

    def tearDown(self):
        self.platform_system_patch.stop()

    def test_getPathDelimiter_platform_is_windows_returns_semicolon(self):
        self.platform_system.return_value = 'Windows'
        actual = self.target.getPathDelimiter()
        self.assertEqual(';', actual)

    def test_getPathDelimiter_platform_is_linux_returns_colon(self):
        self.platform_system.return_value = 'Linux'
        actual = self.target.getPathDelimiter()
        self.assertEqual(':', actual)

    def test_getPathDelimiter_platform_is_Darwin_returns_colon(self):
        self.platform_system.return_value = 'Darwin'
        actual = self.target.getPathDelimiter()
        self.assertEqual(':', actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_buildmode_is_build_returns_sourcedict_items_and_shellcmd(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        sourceDict = {
            'path': '%PATH%', 
            'shell': True, 
            'encoding': 'cp1252', 
            'env': {'CLASSPATH': '%CLASSPATH%;C:/C64/Tools/KickAssembler/KickAss.jar'}, 
            'file_regex': '^\\s*\\((.+\\.\\S+)\\s(\\d*):(\\d*)\\)\\s(.*)'
            }
        expected = sourceDict.copy()
        expected['shell_cmd'] = 'test-command-text';
        actual = self.target.createExecDict(sourceDict, 'build', self.settings_mock)
        self.assertEqual(expected, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_path_is_dict_path_and_settings_path(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        settings = TestSettings({'kickass_path': 'test-settings-path'})
        sourceDict = {'path': 'test-dict-path'}
        actual = self.target.createExecDict(sourceDict, 'build', settings)
        self.assertEqual('test-settings-path:test-dict-path', actual['path'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_path_is_not_expanded(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        settings = TestSettings({'kickass_path': '${file_path}'})
        sourceDict = {'path': '${file_extension}'}
        actual = self.target.createExecDict(sourceDict, 'build', settings)
        self.assertEqual('${file_path}:${file_extension}', actual['path'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory', autospec=True)
    def test_createExecDict_kickasscommandfactory_ctor_is_called_once(self, commandFactory_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        commandFactory_mock.return_value.createCommand.return_value.updateEnvVars.side_effect = (lambda dict: dict)
        actual = self.target.createExecDict({}, 'build', self.settings_mock)
        commandFactory_mock.assert_called_once_with(self.settings_mock)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory', autospec=True)
    def test_createExecDict_kickasscommand_createcommand_is_called_once(self, commandFactory_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        commandFactory_mock.return_value.createCommand = CopyingMock()
        commandFactory_mock.return_value.createCommand.return_value.updateEnvVars.side_effect = (lambda dict: dict)
        actual = self.target.createExecDict({}, 'build', self.settings_mock)
        commandFactory_mock.return_value.createCommand.assert_called_once_with(default_variables_dict, 'build')

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={'test-filename-var':'test-filename'})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', new_callable=CopyingMock)
    def test_createExecDict_kickasscommand_is_called_with_window_variables_and_filename_variables(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        fix_createCommand_mock(createCommand_mock.return_value)
        self.window_mock.extract_variables.return_value = {'test-var':'test-value'}
        actual = self.target.createExecDict({}, 'build', self.settings_mock)
        createCommand_mock.assert_called_once_with({'test-filename-var':'test-filename', 'test-var':'test-value'}, 'build')

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_returns_dict_with_shellcmd_from_kickasscommand(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        actual = self.target.createExecDict({}, 'build', self.settings_mock)
        self.assertEqual('test-command-text', actual['shell_cmd'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_returns_dict_with_envvars_from_kickasscommand(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        createCommand_mock.return_value.updateEnvVars.side_effect = (lambda dict: {'env': {'test-env-var1':'env-var1','test-env-var2':'env-var2'}})
        actual = self.target.createExecDict({}, 'build', self.settings_mock)
        self.assertEqual({'test-env-var1':'env-var1','test-env-var2':'env-var2'}, actual['env'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_expandable_settings_gets_expanded(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        settings = TestSettings({
            'kickass_compile_args': 'kickass_compile_args-value',
            'kickass_compile_debug_additional_args': 'kickass_compile_debug_additional_args-value',
            'kickass_run_command_c64debugger': 'kickass_run_command_c64debugger-value',
            'kickass_debug_command_c64debugger': 'kickass_debug_command_c64debugger-value',
            'kickass_run_command_x64': 'kickass_run_command_x64-value',
            'kickass_debug_command_x64': 'kickass_debug_command_x64-value',
            'kickass_run_path': 'kickass_run_path-value',
            'kickass_debug_path': 'kickass_debug_path-value',
            'kickass_jar_path': 'kickass_jar_path-value',
            'kickass_args': 'kickass_args-value',
            'kickass_run_args': 'kickass_run_args-value',
            'kickass_debug_args': 'kickass_debug_args-value',
            'kickass_startup_file_path': 'kickass_startup_file_path-value',
            'kickass_breakpoint_filename': 'kickass_breakpoint_filename-value',
            'kickass_compiled_filename': 'kickass_compiled_filename-value',
            'kickass_output_path': 'kickass_output_path-value',
            'default_prebuild_path': 'default_prebuild_path-value',
            'default_postbuild_path': 'default_postbuild_path-value'
            })
        sourceDict = {'test-key': '${kickass_compile_args} ${kickass_compile_debug_additional_args} ${kickass_run_command_c64debugger} ${kickass_debug_command_c64debugger} ${kickass_run_command_x64} ${kickass_debug_command_x64} ${kickass_run_path} ${kickass_debug_path} ${kickass_jar_path} ${kickass_args} ${kickass_run_args} ${kickass_debug_args} ${kickass_startup_file_path} ${kickass_breakpoint_filename} ${kickass_compiled_filename} ${kickass_output_path} ${default_prebuild_path} ${default_postbuild_path}'}
        expected = 'kickass_compile_args-value kickass_compile_debug_additional_args-value kickass_run_command_c64debugger-value kickass_debug_command_c64debugger-value kickass_run_command_x64-value kickass_debug_command_x64-value kickass_run_path-value kickass_debug_path-value kickass_jar_path-value kickass_args-value kickass_run_args-value kickass_debug_args-value kickass_startup_file_path-value kickass_breakpoint_filename-value kickass_compiled_filename-value kickass_output_path-value default_prebuild_path-value default_postbuild_path-value'
        actual = self.target.createExecDict(sourceDict, 'build', settings)
        self.assertEqual(expected, actual['test-key'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_non_expandable_gets_emptied(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        settings = TestSettings({'kickass_args1': 'test-args'})
        sourceDict = {'test-key': '${kickass_args1} a'}
        actual = self.target.createExecDict(sourceDict, 'build', settings)
        self.assertEqual(' a', actual['test-key'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_expandalbe_variables_gets_expanded(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        settings = TestSettings({
            'kickass_compile_args': 'kickass_compile_args-value',
            'kickass_run_command_x64': '${kickass_compiled_filename} ${kickass_args}',
            'kickass_compiled_filename': 'kickass_compiled_filename-value',
            'kickass_args': 'kickass_args-value'
            })
        sourceDict = {'test-key': '${kickass_run_command_x64} ${kickass_compile_args}'}
        actual = self.target.createExecDict(sourceDict, 'build', settings)
        self.assertEqual('kickass_compiled_filename-value kickass_args-value kickass_compile_args-value', actual['test-key'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_expandable_variables_gets_double_expanded(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        createCommand_mock
        settings = TestSettings({
            'kickass_compiled_filename': 'kickass_compiled_filename-value',
            'kickass_compile_args': 'kickass_compile_args-value ${kickass_compiled_filename}',
            'kickass_run_command_x64': '${kickass_compile_args}'
            })
        sourceDict = {'test-key': '${kickass_run_command_x64}'}
        actual = self.target.createExecDict(sourceDict, 'build', settings)
        self.assertEqual('kickass_compile_args-value kickass_compiled_filename-value', actual['test-key'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock(command_text='test-command-text ${kickass_run_command_x64}'))
    def test_createExecDict_expandable_variables_gets_double_expanded1(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        createCommand_mock
        settings = TestSettings({
            'kickass_compiled_filename': 'kickass_compiled_filename-value',
            'kickass_compile_args': 'kickass_compile_args-value ${kickass_compiled_filename}',
            'kickass_run_command_x64': 'x64 ${kickass_compile_args}'
            })
        actual = self.target.createExecDict({}, 'build', settings)
        self.assertEqual('test-command-text x64 kickass_compile_args-value kickass_compiled_filename-value', actual['shell_cmd'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_non_expandalbe_variables_not_expanded(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        settings = TestSettings({
            'kickass_compile_args': 'kickass_compile_args-value',
            'kickass_breakpoint_filename': '${kickass_compiled_filename} ${kickass_args}',
            'kickass_compiled_filename': 'kickass_compiled_filename-value',
            'kickass_args': 'kickass_args-value'
            })
        sourceDict = {'test-key': '${kickass_breakpoint_filename} ${kickass_compile_args}'}
        actual = self.target.createExecDict(sourceDict, 'build', settings)
        self.assertEqual('${kickass_compiled_filename} ${kickass_args} kickass_compile_args-value', actual['test-key'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_returns_dict_with_envvars_from_settings(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        settings = TestSettings({'kickass_env': {'test-settings-env-var1':'env-var1','test-settings-env-var2':'env-var2'}})
        actual = self.target.createExecDict({'env':{}}, 'build', settings)
        self.assertEqual({'test-settings-env-var1':'env-var1','test-settings-env-var2':'env-var2'}, actual['env'])

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getFilenameVariables', autospec=True, return_value={})
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.getPathDelimiter', autospec=True, return_value=':')
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createCommand', autospec=True, return_value=createCommand_mock())
    def test_createExecDict_error_occurs_returns_dict_with_error_command(self, createCommand_mock, getPathDelimiter_mock, getFilenameVariables_mock):
        self.window_mock.extract_variables.side_effect = Exception('test-error')
        actual = self.target.createExecDict({}, 'build', self.settings_mock)
        self.assertEqual('echo test-error', actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', autospec=True, return_value=True)
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings', autospec=True)
    @patch('sublime.error_message', autospec=True)
    def test_run_settings_not_loaded_sets_error_message_and_returns(self, sublime_error_mock, settings_mock, glob_mock, getFilenameVariables_mock):
        settings_mock.return_value.isLoaded.return_value = False
        actual = self.target.run(buildmode = 'build', env = {})
        sublime_error_mock.assert_called_once_with("Settings could not be loaded, please restart Sublime Text.")
        self.assertEqual(0, settings_mock.return_value.getSetting.call_count)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict', autospec=True)
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', autospec=True, return_value=True)
    @patch('os.makedirs', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings', autospec=True)
    def test_run_creates_makedirs_called_once(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSetting.return_value = 'outputdir'
        actual = self.target.run(buildmode = 'build', env = {})
        os_mock.assert_called_once_with('outputdir', exist_ok=True)

    @patch('os.path.isdir', return_value=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.emptyFolder', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict', autospec=True)
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', autospec=True, return_value=True)
    @patch('os.makedirs', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings', autospec=True)
    def test_run_emptybinfolder_setting_is_true_emptyfolder_is_called_once(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock, emptyfolder_mock, isdir_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSetting.return_value = 'outputdir'
        settings_mock.return_value.getSettingAsBool.return_value = True
        actual = self.target.run(buildmode = 'build', env = {})
        emptyfolder_mock.assert_called_once_with(self.target, 'outputdir')

    @patch('os.path.isdir', return_value=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.emptyFolder', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict', autospec=True)
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', autospec=True, return_value=True)
    @patch('os.makedirs', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings', autospec=True)
    def test_run_emptybinfolder_setting_is_false_emptyfolder_is_not_called(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock, emptyfolder_mock, isdir_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSetting.return_value = 'outputdir'
        settings_mock.return_value.getSettingAsBool.return_value = False
        actual = self.target.run(buildmode = 'build', env = {})
        self.assertEqual(0, emptyfolder_mock.call_count)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict', autospec=True)
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', autospec=True, return_value=True)
    @patch('os.makedirs', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings', autospec=True)
    def test_run_window_runcommand_is_called_once(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSettingAsBool.return_value = False
        exec_dict_val = {'key11':'val11'}
        execDict_mock.return_value = exec_dict_val
        actual = self.target.run(buildmode = 'build', env = {})
        self.window_mock.run_command.assert_called_once_with('exec', exec_dict_val)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict', autospec=True)
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', autospec=True, return_value=True)
    @patch('os.makedirs', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings', autospec=True)
    def test_run_createexecdict_is_called_once(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSettingAsBool.return_value = False
        actual = self.target.run(buildmode = 'build', env = {})
        execDict_mock.assert_called_once_with(self.target, {'env': {}}, 'build', settings_mock.return_value)

    def test_mergedictionaries_no_collisions_dictionaries_merged(self):
        dict1 = {'a':'b'}
        dict2 = {'c':'d'}
        expected = {'a':'b', 'c':'d'}
        actual = self.target.mergeDictionaries(dict1, dict2)
        self.assertEqual(expected, actual)

    def test_mergedictionaries_collisions_dictionaries_merged(self):
        dict1 = {'a':'b'}
        dict2 = {'a':'d'}
        expected = {'a':'d'}
        actual = self.target.mergeDictionaries(dict1, dict2)
        self.assertEqual(expected, actual)

    def test_mergedictionaries_source_dictionaries_unchanged(self):
        dict1 = {'a':'b'}
        dict2 = {'c':'d'}
        actual = self.target.mergeDictionaries(dict1, dict2)
        self.assertEqual({'a':'b'}, dict1)
        self.assertEqual({'c':'d'}, dict2)

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_parseAnnotations_open_is_called_oince(self, open_mock):
        filename = 'test-file.asm'
        actual = self.target.parseAnnotations(filename)
        open_mock.assert_called_once_with(filename, 'r')

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_parseAnnotations_readline_is_called_oince(self, open_mock):
        actual = self.target.parseAnnotations('test-file.asm')
        open_mock.return_value.readline.assert_called_once_with()

    @patch('builtins.open', new_callable=mock_open34, read_data='')
    def test_parseAnnotations_firstline_is_empty(self, open_mock):
        actual = self.target.parseAnnotations('test-file.asm')
        self.assertEqual({}, actual)

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_parseAnnotations_firstline_not_annotation_returns_empty_dict(self, open_mock):
        actual = self.target.parseAnnotations('test-file.asm')
        self.assertEqual({}, actual)

    @patch('builtins.open', new_callable=mock_open34, read_data='@kickass-build "test-annotation-1": "val1"')
    def test_parseAnnotations_firstline_is_not_a_comment_returns_empty_dict(self, open_mock):
        actual = self.target.parseAnnotations('test-file.asm')
        self.assertEqual({}, actual)

    @patch('builtins.open', new_callable=mock_open34, read_data='// @kickass-not-build "test-annotation-1": "val1"')
    def test_parseAnnotations_firstline_is_a_comment_no_kickassbuild_directive_returns_empty_dict(self, open_mock):
        actual = self.target.parseAnnotations('test-file.asm')
        self.assertEqual({}, actual)

    @patch("builtins.open", new_callable=mock_open34, read_data='// @kickass-build "test-annotation-1": "val1", "test-annotation-2": "val2"')
    def test_parseAnnotations_firstline_is_a_comment_has_kickassbuild_directive_returns_parsed_dict(self, open_mock):
        actual = self.target.parseAnnotations('test-file.asm')
        self.assertEqual({'test-annotation-1': 'val1', 'test-annotation-2': 'val2'}, actual)

    @patch("builtins.open", new_callable=mock_open34, read_data='// @kickass-build "test-annotation-1"= "val1"')
    def test_parseAnnotations_firstline_is_a_comment_has_kickassbuild_directive_illegal_format_raises_valueerror(self, open_mock):
        filename = 'test-file.asm'
        with self.assertRaisesRegexp(ValueError, 'Could not parse build annotations: .*') as cm:
            actual = self.target.parseAnnotations('test-file.asm')

    @patch('builtins.open', new_callable=mock_open34, read_data='// some-extra-text @kickass-build "test-annotation-1": "val1"')
    def test_parseAnnotations_firstline_is_a_comment_has_kickassbuild_directive_and_extra_text_returns_parsed_dict(self, open_mock):
        actual = self.target.parseAnnotations('test-file.asm')
        self.assertEqual({'test-annotation-1': 'val1'}, actual)

    @patch('builtins.open', new_callable=mock_open34, read_data='  //  @kickass-build  "test-annotation-1":  "val1" ')
    def test_parseAnnotations_firstline_is_a_comment_has_kickassbuild_directive_and_extra_spaces_returns_parsed_dict(self, open_mock):
        actual = self.target.parseAnnotations('test-file.asm')
        self.assertEqual({'test-annotation-1': 'val1'}, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', autospec=True, return_value={})
    def test_getFilenameVariables_buildmode_does_not_have_startup_no_annotations_returns_correct_dictionary(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name', 'kickass_compiled_filename': 'test-file.prg'})
        actual = self.target.getFilenameVariables('build', settings, default_variables_dict.copy())
        self.assertEqual({'build_file_base_name': 'test-file', 'start_filename': 'test-file.prg'}, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', autospec=True, return_value={})
    def test_getFilenameVariables_buildmode_has_startup_no_annotations_returns_correct_dictionary(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name', 'kickass_compiled_filename': 'test-startup-file.prg'})
        actual = self.target.getFilenameVariables('build-startup', settings, default_variables_dict.copy())
        self.assertEqual({'build_file_base_name': 'test-startup-base-name', 'start_filename': 'test-startup-file.prg'}, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', autospec=True, return_value={})
    def test_getFilenameVariables_calls_parseAnnotations_once(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name'})
        actual = self.target.getFilenameVariables('build', settings, default_variables_dict.copy())
        parseannotations_mock.assert_called_once_with(self.target, 'test-path/test-file.asm')

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', autospec=True, return_value={'file-to-run': 'test-run-file.ext'})
    def test_getFilenameVariables_has_filetorun_annotation_returns_correct_dictionary(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name'})
        actual = self.target.getFilenameVariables('build', settings, default_variables_dict.copy())
        self.assertEqual({'build_file_base_name': 'test-file', 'start_filename': 'test-run-file.ext'}, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', autospec=True, return_value={'file-to-not-run': 'test-run-file.ext'})
    def test_getFilenameVariables_has_other_annotation_returns_correct_dictionary(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name', 'kickass_compiled_filename': 'test-file.prg'})
        actual = self.target.getFilenameVariables('build', settings, default_variables_dict.copy())
        self.assertEqual({'build_file_base_name': 'test-file', 'start_filename': 'test-file.prg'}, actual)

    #System tests
    #TODO: Maybe rework or move createExecDict system tests for all build modes, another file?

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_build_returns_dictionary_with_correct_build_command(self, file_mocks):
        expected = 'java cml.kickass.KickAssembler "test-file.asm" -log "bin/test-file_BuildLog.txt" -o "bin/test-file.prg" -vicesymbols -showmem -odir "bin" '
        actual = self.target.createExecDict({}, 'build', self.all_settings)
        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildstartup_returns_dictionary_with_correct_build_command(self, file_mocks):
        expected = 'java cml.kickass.KickAssembler "Startup.asm" -log "bin/Startup_BuildLog.txt" -o "bin/Startup.prg" -vicesymbols -showmem -odir "bin" '
        actual = self.target.createExecDict({}, 'build-startup', self.all_settings)
        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildandrun_returns_dictionary_with_correct_build_command(self, file_mocks):
        expected = 'java cml.kickass.KickAssembler "test-file.asm" -log "bin/test-file_BuildLog.txt" -o "bin/test-file.prg" -vicesymbols -showmem -odir "bin"   && "x64" -logfile "bin/test-file_ViceLog.txt" -moncommands "bin/test-file.vs"  "bin/test-file.prg"'
        actual = self.target.createExecDict({}, 'build-and-run', self.all_settings)
        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildandrunstartup_returns_dictionary_with_correct_build_command(self, file_mocks):
        expected = 'java cml.kickass.KickAssembler "Startup.asm" -log "bin/Startup_BuildLog.txt" -o "bin/Startup.prg" -vicesymbols -showmem -odir "bin"   && "x64" -logfile "bin/Startup_ViceLog.txt" -moncommands "bin/Startup.vs"  "bin/Startup.prg"'
        actual = self.target.createExecDict({}, 'build-and-run-startup', self.all_settings)
        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildandrun_returns_dictionary_with_correct_build_command(self, file_mocks):
        expected = 'java cml.kickass.KickAssembler "test-file.asm" -log "bin/test-file_BuildLog.txt" -o "bin/test-file.prg" -vicesymbols -showmem -odir "bin"   -afo :afo=true && [ -f "bin/breakpoints.txt" ] && cat "bin/test-file.vs" "bin/breakpoints.txt" > "bin/test-file_MonCommands.mon" || cat "bin/test-file.vs" > "bin/test-file_MonCommands.mon" && "x64" -logfile "bin/test-file_ViceLog.txt" -moncommands "bin/test-file_MonCommands.mon"  "bin/test-file.prg"'
        actual = self.target.createExecDict({}, 'build-and-debug', self.all_settings)
        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildandrunstartup_returns_dictionary_with_correct_build_command(self, file_mocks):
        expected = 'java cml.kickass.KickAssembler "Startup.asm" -log "bin/Startup_BuildLog.txt" -o "bin/Startup.prg" -vicesymbols -showmem -odir "bin"   -afo :afo=true && [ -f "bin/breakpoints.txt" ] && cat "bin/Startup.vs" "bin/breakpoints.txt" > "bin/Startup_MonCommands.mon" || cat "bin/Startup.vs" > "bin/Startup_MonCommands.mon" && "x64" -logfile "bin/Startup_ViceLog.txt" -moncommands "bin/Startup_MonCommands.mon"  "bin/Startup.prg"'
        actual = self.target.createExecDict({}, 'build-and-debug-startup', self.all_settings)
        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', autospec=True, return_value=True)
    def test_createExecDict_buildmode_is_make_returns_dictionary_with_correct_makecommand(self, glob_mock, getFilenameVariables_mock):
        actual = self.target.createExecDict({'env':{}}, 'make', self.all_settings)
        self.assertEqual('. "make.sh"', actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', autospec=True, return_value=True)
    def test_createExecDict_buildmode_is_make_returns_dictionary_with_correct_env_variables(self, glob_mock, getFilenameVariables_mock):
        expected = {
            'kickass_buildmode': 'make', 
            'kickass_file': 'test-file.asm', 
            'kickass_file_path': 'test-path', 
            'kickass_bin_folder': 'test-path/bin', 
            'kickass_prg_file': 'test-path/bin/test-file.prg'
            }
        actual = self.target.createExecDict({'env':{}}, 'make', self.all_settings)
        self.assertEqual(expected, actual['env'])

if __name__ == '__main__':
    unittest.main()