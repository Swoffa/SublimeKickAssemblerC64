from unittest import TestCase
from unittest.mock import patch, create_autospec
from testglobals import kickassbuild, default_settings_dict
from testsettings import TestSettings

class TestKickAssCommandFactory(TestCase):

    def setUp(self):
        self.platform_system_patch = patch('platform.system', autospec=True)
        self.platform_system = self.platform_system_patch.start()
        self.platform_system.return_value = 'Darwin'

        self.settings_mock = create_autospec(kickassbuild.SublimeSettings)
        self.settings_mock.getSetting.return_value = ''
        self.default_settings = TestSettings(default_settings_dict)
        self.target = kickassbuild.KickAssCommandFactory(self.default_settings)

    def tearDown(self):
        self.platform_system_patch.stop()

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createKickassCommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMakeCommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createCommand_buildmode_is_build_createkickasscommand_is_called_once(self, kickassCommand_mock, createMakeCommand_mock, createKickassCommand_mock):
        buildMode = 'build'
        actual = self.target.createCommand({}, buildMode)
        createKickassCommand_mock.assert_called_once_with(self.target, {}, buildMode)
        self.assertEqual(0, createMakeCommand_mock.call_count)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createKickassCommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMakeCommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createCommand_buildmode_is_buildrun_createkickasscommand_is_called_once(self, kickassCommand_mock, createMakeCommand_mock, createKickassCommand_mock):
        buildMode = 'build-run'
        actual = self.target.createCommand({}, buildMode)
        createKickassCommand_mock.assert_called_once_with(self.target, {}, buildMode)
        self.assertEqual(0, createMakeCommand_mock.call_count)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createKickassCommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMakeCommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createCommand_buildmode_is_make_createmakecommandÄ_is_called_once(self, kickassCommand_mock, createMakeCommand_mock, createKickassCommand_mock):
        buildMode = 'make'
        actual = self.target.createCommand({}, buildMode)
        createMakeCommand_mock.assert_called_once_with(self.target, {}, buildMode)
        self.assertEqual(0, createKickassCommand_mock.call_count)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createMakeCommand_makescript_does_not_exist_getrunscriptstatement_is_called_once(self, kickassCommand_mock, getRunScriptStatement_mock):
        buildMode = 'build'
        actual = self.target.createMakeCommand({}, buildMode)
        getRunScriptStatement_mock.assert_called_once_with(self.target, "make", "default_make_path")

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', return_value=None, autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createMakeCommand_makescript_does_not_exist_and_no_default_makepath_setting_exist_returns_error_command(self, kickassCommand_mock, getRunScriptStatement_mock):
        buildMode = 'build'
        actual = self.target.createMakeCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('echo Make file not found. Place a file named make.sh in ${file_path}.', True, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', return_value=None, autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createMakeCommand_makescript_does_not_exist_and_default_makepat_hsetting_exist_returns_error_command(self, kickassCommand_mock, getRunScriptStatement_mock):
        buildMode = 'build'
        settings = TestSettings(default_settings_dict)
        settings.addSetting('default_make_path', 'test-default-path')
        target = kickassbuild.KickAssCommandFactory(settings)
        actual = target.createMakeCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('echo Make file not found. Place a file named make.sh in ${file_path} or test-default-path.', True, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', return_value='test-make-script', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createMakeCommand_makescript_exist_returns_correct_makecommand(self, kickassCommand_mock, getRunScriptStatement_mock):
        buildMode = 'build'
        actual = self.target.createMakeCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('test-make-script', True, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', return_value=None, autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMonCommandsStatement', return_value='mocked-moncommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createKickassCommand_no_jarpath_setting_exist_returns_correct_compilecommand(self, kickassCommand_mock, createmonstatement_mock, getRunScriptStatement_mock):
        buildMode = 'build'
        actual = self.target.createKickassCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('java cml.kickass.KickAssembler ${kickass_compile_args}', False, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', return_value=None, autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMonCommandsStatement', return_value='mocked-moncommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createKickassCommand_jarpath_setting_exist_returns_correct_compilecommand(self, kickassCommand_mock, createmonstatement_mock, getRunScriptStatement_mock):
        buildMode = 'build'
        settings = TestSettings(default_settings_dict)
        settings.addSetting('kickass_jar_path', 'testpath')
        target = kickassbuild.KickAssCommandFactory(settings)
        actual = target.createKickassCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('java -cp "${kickass_jar_path}" cml.kickass.KickAssembler ${kickass_compile_args}', False, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', return_value=None, autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMonCommandsStatement', return_value='mocked-moncommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createKickassCommand_buildmode_is_buildrun_returns_correct_compilecommand(self, kickassCommand_mock, createmonstatement_mock, getRunScriptStatement_mock):
        buildMode = 'build-run'
        actual = self.target.createKickassCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('java cml.kickass.KickAssembler ${kickass_compile_args}  && ${kickass_run_command_x64}', False, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', return_value=None, autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMonCommandsStatement', return_value='mocked-moncommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createKickassCommand_buildmode_is_buildrun_and_runpath_setting_has_c64debugger_returns_correct_compilecommand(self, kickassCommand_mock, createmonstatement_mock, getRunScriptStatement_mock):
        buildMode = 'build-run'
        settings = TestSettings(default_settings_dict)
        settings.addSetting('kickass_run_path', 'c64debugger')
        target = kickassbuild.KickAssCommandFactory(settings)
        actual = target.createKickassCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('java cml.kickass.KickAssembler ${kickass_compile_args}  && ${kickass_run_command_c64debugger}', False, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', return_value=None, autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMonCommandsStatement', return_value='mocked-moncommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createKickassCommand_buildmode_is_builddebug_returns_correct_compilecommand(self, kickassCommand_mock, createmonstatement_mock, getRunScriptStatement_mock):
        buildMode = 'build-debug'
        actual = self.target.createKickassCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('java cml.kickass.KickAssembler ${kickass_compile_args}  ${kickass_compile_debug_additional_args} && mocked-moncommand && ${kickass_debug_command_x64}', False, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', return_value=None, autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMonCommandsStatement', return_value='mocked-moncommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createKickassCommand_buildmode_is_builddebug_and_runpath_setting_has_c64debugger_returns_correct_compilecommand(self, kickassCommand_mock, createmonstatement_mock, getRunScriptStatement_mock):
        buildMode = 'build-debug'
        settings = TestSettings(default_settings_dict)
        settings.addSetting('kickass_debug_path', 'c64debugger')
        target = kickassbuild.KickAssCommandFactory(settings)
        actual = target.createKickassCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('java cml.kickass.KickAssembler ${kickass_compile_args}  ${kickass_compile_debug_additional_args} && mocked-moncommand && ${kickass_debug_command_c64debugger}', False, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', side_effect=['test-pre-statement', None], autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMonCommandsStatement', return_value='mocked-moncommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createKickassCommand_buildmode_is_builddebug_and_has_prebuildscript_returns_correct_compilecommand(self, kickassCommand_mock, createmonstatement_mock, getRunScriptStatement_mock):
        buildMode = 'build-debug'
        actual = self.target.createKickassCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('test-pre-statement && java cml.kickass.KickAssembler ${kickass_compile_args}  ${kickass_compile_debug_additional_args} && mocked-moncommand && ${kickass_debug_command_x64}', True, False, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', side_effect=[None, 'test-post-statement'], autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMonCommandsStatement', return_value='mocked-moncommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createKickassCommand_buildmode_is_builddebug_and_has_postbuildscript_returns_correct_compilecommand(self, kickassCommand_mock, createmonstatement_mock, getRunScriptStatement_mock):
        buildMode = 'build-debug'
        actual = self.target.createKickassCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('java cml.kickass.KickAssembler ${kickass_compile_args}  ${kickass_compile_debug_additional_args} && mocked-moncommand && test-post-statement && ${kickass_debug_command_x64}', False, True, buildMode)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getRunScriptStatement', side_effect=['test-pre-statement', 'test-post-statement'], autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.createMonCommandsStatement', return_value='mocked-moncommand', autospec=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommand', autospec=True)
    def test_createKickassCommand_buildmode_is_builddebug_and_hasprebuildscript_and_haspostbuildscript_returns_correct_compilecommand(self, kickassCommand_mock, createmonstatement_mock, getRunScriptStatement_mock):
        buildMode = 'build-debug'
        actual = self.target.createKickassCommand({}, buildMode)
        kickassCommand_mock.assert_called_once_with('test-pre-statement && java cml.kickass.KickAssembler ${kickass_compile_args}  ${kickass_compile_debug_additional_args} && mocked-moncommand && test-post-statement && ${kickass_debug_command_x64}', True, True, buildMode)

    @patch('platform.system', return_value='Windows', autospec=True)
    def test_getExt_platform_is_windows_returns_bat(self, platform_mock):
        actual = self.target.getExt()
        self.assertEqual('bat', actual)

    @patch('platform.system', return_value='Linux', autospec=True)
    def test_getExt_platform_is_linux_returns_sh(self, platform_mock):
        actual = self.target.getExt()
        self.assertEqual('sh', actual)

    @patch('platform.system', return_value='Darwin', autospec=True)
    def test_getExt_platform_is_Darwin_returns_sh(self, platform_mock):
        actual = self.target.getExt()
        self.assertEqual('sh', actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getExt', return_value='test-ext', autospec=True)
    @patch('glob.glob', side_effect=[False,False], autospec=True)
    def test_getRunScriptStatement_no_command_or_defaultcommand_exist_returns_none(self, glob_mock, getext_mock):
        actual = self.target.getRunScriptStatement('test-script-name', 'test-setting-name')
        self.assertEqual(None, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getExt', return_value='test-ext', autospec=True)
    @patch('glob.glob', side_effect=[False,True], autospec=True)
    @patch('platform.system', return_value='Windows', autospec=True)
    def test_getRunScriptStatement_platform_is_windows_and_command_exist_and_no_default_commandexist_returns_scriptstatement(self, platform_mock, glob_mock, getext_mock):
        actual = self.target.getRunScriptStatement('test-script-name', 'test-setting-name')
        self.assertEqual('call "test-script-name.test-ext"', actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getExt', return_value='test-ext', autospec=True)
    @patch('glob.glob', side_effect=[False,True], autospec=True)
    @patch('platform.system', return_value='Darwin', autospec=True)
    def test_getRunScriptStatement_platform_is_darwin_and_command_exist_and_no_default_command_exist_returns_scriptstatement(self, platform_mock, glob_mock, getext_mock):
        actual = self.target.getRunScriptStatement('test-script-name', 'test-setting-name')
        self.assertEqual('. "test-script-name.test-ext"', actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getExt', return_value='test-ext', autospec=True)
    @patch('glob.glob', side_effect=[False,True], autospec=True)
    @patch('platform.system', return_value='Linux', autospec=True)
    def test_getRunScriptStatement_platform_is_linux_and_command_exist_and_no_default_command_exist_returns_scriptstatement(self, platform_mock, glob_mock, getext_mock):
        actual = self.target.getRunScriptStatement('test-script-name', 'test-setting-name')
        self.assertEqual('. "test-script-name.test-ext"', actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getExt', return_value='test-ext', autospec=True)
    @patch('glob.glob', side_effect=[True,False], autospec=True)
    @patch('platform.system', return_value='Windows', autospec=True)
    def test_getRunScriptStatement_platform_is_windows_and_no_command_exist_and_default_command_exist_returndefaultscriptstatement(self, platform_mock, glob_mock, getext_mock):
        settingName = 'test-setting-name'
        settings = TestSettings(default_settings_dict)
        settings.addSetting(settingName, 'test-default-path')
        target = kickassbuild.KickAssCommandFactory(settings)
        actual = target.getRunScriptStatement('test-script-name', settingName)
        self.assertEqual('call "test-default-path/test-script-name.test-ext"', actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickAssCommandFactory.getExt', return_value='test-ext', autospec=True)
    @patch('glob.glob', side_effect=[True,True], autospec=True)
    @patch('platform.system', return_value='Windows', autospec=True)
    def test_getRunScriptStatement_platform_is_windows_and_command_exist_and_default_command_exist_returndefaultscriptstatement(self, platform_mock, glob_mock, getext_mock):
        settingName = 'test-setting-name'
        settings = TestSettings(default_settings_dict)
        settings.addSetting(settingName, 'test-default-path')
        target = kickassbuild.KickAssCommandFactory(settings)
        actual = target.getRunScriptStatement('test-script-name', settingName)
        self.assertEqual('call "test-script-name.test-ext"', actual)

    @patch('platform.system', return_value='Windows', autospec=True)
    def test_createMonCommandsStatement_platform_is_windows_returns_correct_moncommand_statement(self, platform_mock):
        actual = self.target.createMonCommandsStatement()
        self.assertEqual('copy /Y \"${kickass_output_path}\\\\${build_file_base_name}.vs\" + \"${kickass_output_path}\\\\${kickass_breakpoint_filename}\" \"${kickass_output_path}\\\\${build_file_base_name}_MonCommands.mon\"', actual)

    @patch('platform.system', return_value='Darwin', autospec=True)
    def test_createMonCommandsStatement_platform_is_darwin_returns_correct_moncommand_statement(self, platform_mock):
        actual = self.target.createMonCommandsStatement()
        self.assertEqual('[ -f \"${kickass_output_path}/${kickass_breakpoint_filename}\" ] && cat \"${kickass_output_path}/${build_file_base_name}.vs\" \"${kickass_output_path}/${kickass_breakpoint_filename}\" > \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\" || cat \"${kickass_output_path}/${build_file_base_name}.vs\" > \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\"', actual)

    @patch('platform.system', return_value='Linux', autospec=True)
    def test_createMonCommandsStatement_platform_is_linux_returns_correct_moncommand_statement(self, platform_mock):
        actual = self.target.createMonCommandsStatement()
        self.assertEqual('[ -f \"${kickass_output_path}/${kickass_breakpoint_filename}\" ] && cat \"${kickass_output_path}/${build_file_base_name}.vs\" \"${kickass_output_path}/${kickass_breakpoint_filename}\" > \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\" || cat \"${kickass_output_path}/${build_file_base_name}.vs\" > \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\"', actual)

if __name__ == '__main__':
    unittest.main()