import sublime
import sys
import os
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch, create_autospec   
from testsettings import TestSettings
from testglobals import kickassbuild, default_settings_dict, mock_open34

#Use project path as root, if exist?
#Use platform from variables

class TestKickassBuildCommand(TestCase):

    def setUp(self):
        self.platform_system_patch = patch('platform.system')
        self.platform_system = self.platform_system_patch.start()
        self.platform_system.return_value = 'Darwin'

        self.default_variables = {
            #'file_name': 'test-file.asm',
            #'platform': 'Windows', 
            #'packages': 'C:\\Users\\SimonOskarsson\\AppData\\Roaming\\Sublime Text 3\\Packages', 
            #'folder': filePath, 
            #'file': filePath+'test-file.asm', 
            'file_extension': 'asm', 
            'file_path': 'test-path', 
            'file_base_name': 'test-file'
            }

        self.window_mock = Mock()
        self.window_mock.extract_variables.return_value = self.default_variables

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

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_build_returns_sourcedict_items(self, file_mock):
        sourceDict = {
            'path': '%PATH%', 
            'shell': True, 
            'encoding': 'cp1252', 
            'env': {'CLASSPATH': '%CLASSPATH%;C:/C64/Tools/KickAssembler/KickAss.jar'}, 
            'file_regex': '^\\s*\\((.+\\.\\S+)\\s(\\d*):(\\d*)\\)\\s(.*)'
            }
        expected = sourceDict.copy()
        expected['shell_cmd'] = 'java cml.kickass.KickAssembler ';

        actual = self.target.createExecDict(sourceDict, 'build', self.settings_mock)

        self.assertEqual(expected, actual)

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_build_returns_dictionary_with_correct_build_command(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "test-file.asm" -log "bin/test-file_BuildLog.txt" -o "bin/test-file.prg" -vicesymbols -showmem -odir "bin" '

        actual = self.target.createExecDict(sourceDict, 'build', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildstartup_returns_dictionary_with_correct_build_command(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "Startup.asm" -log "bin/Startup_BuildLog.txt" -o "bin/Startup.prg" -vicesymbols -showmem -odir "bin" '

        actual = self.target.createExecDict(sourceDict, 'build-startup', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildandrun_returns_dictionary_with_correct_build_command(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "test-file.asm" -log "bin/test-file_BuildLog.txt" -o "bin/test-file.prg" -vicesymbols -showmem -odir "bin"   && "x64" -logfile "bin/test-file_ViceLog.txt" -moncommands "bin/test-file.vs"  "bin/test-file.prg"'

        actual = self.target.createExecDict(sourceDict, 'build-and-run', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildandrunstartup_returns_dictionary_with_correct_build_command(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "Startup.asm" -log "bin/Startup_BuildLog.txt" -o "bin/Startup.prg" -vicesymbols -showmem -odir "bin"   && "x64" -logfile "bin/Startup_ViceLog.txt" -moncommands "bin/Startup.vs"  "bin/Startup.prg"'

        actual = self.target.createExecDict(sourceDict, 'build-and-run-startup', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildandrun_returns_dictionary_with_correct_build_command(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "test-file.asm" -log "bin/test-file_BuildLog.txt" -o "bin/test-file.prg" -vicesymbols -showmem -odir "bin"   -afo :afo=true && [ -f "bin/breakpoints.txt" ] && cat "bin/test-file.vs" "bin/breakpoints.txt" > "bin/test-file_MonCommands.mon" || cat "bin/test-file.vs" > "bin/test-file_MonCommands.mon" && "x64" -logfile "bin/test-file_ViceLog.txt" -moncommands "bin/test-file_MonCommands.mon"  "bin/test-file.prg"'

        actual = self.target.createExecDict(sourceDict, 'build-and-debug', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmode_is_buildandrunstartup_returns_dictionary_with_correct_build_command(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "Startup.asm" -log "bin/Startup_BuildLog.txt" -o "bin/Startup.prg" -vicesymbols -showmem -odir "bin"   -afo :afo=true && [ -f "bin/breakpoints.txt" ] && cat "bin/Startup.vs" "bin/breakpoints.txt" > "bin/Startup_MonCommands.mon" || cat "bin/Startup.vs" > "bin/Startup_MonCommands.mon" && "x64" -logfile "bin/Startup_ViceLog.txt" -moncommands "bin/Startup_MonCommands.mon"  "bin/Startup.prg"'

        actual = self.target.createExecDict(sourceDict, 'build-and-debug-startup', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    def test_createExecDict_buildmode_is_make_returns_dictionary_with_correct_makecommand(self, glob_mock, file_mock):
        sourceDict = {'env':{}}
        expected = '. "make.sh"'

        actual = self.target.createExecDict(sourceDict, 'make', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    def test_createExecDict_buildmode_is_make_returns_dictionary_with_correct_env_variables(self, glob_mock, file_mock):
        sourceDict = {'env':{}}
        expected = {
            'kickass_buildmode': 'make', 
            'kickass_file': 'test-file.asm', 
            'kickass_file_path': 'test-path', 
            'kickass_bin_folder': 'test-path/bin', 
            'kickass_prg_file': 'test-path/bin/test-file.prg'
            }

        actual = self.target.createExecDict(sourceDict, 'make', self.all_settings)

        self.assertEqual(expected, actual['env'])

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    @patch('sublime.error_message')
    def test_run_settings_not_loaded_sets_error_message_and_returns(self, sublime_error_mock, settings_mock, glob_mock, file_mock):
        settings_mock.return_value.isLoaded.return_value = False

        actual = self.target.run(buildmode = 'build', env = {})

        sublime_error_mock.assert_called_once_with("Settings could not be loaded, please restart Sublime Text.")
        settings_mock.getSetings.assert_not_called()


    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_creates_makedirs_called_once(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSetting.return_value = 'outputdir'

        actual = self.target.run(buildmode = 'build', env = {})

        os_mock.assert_called_once_with('outputdir', exist_ok=True)

    @patch('os.path.isdir', return_value=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.emptyFolder')
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_emptybinfolder_setting_is_true_emptyfolder_is_called_once(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock, emptyfolder_mock, isdir_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSetting.return_value = 'outputdir'
        settings_mock.return_value.getSettingAsBool.return_value = True
        
        actual = self.target.run(buildmode = 'build', env = {})

        emptyfolder_mock.assert_called_once_with('outputdir')

    @patch('os.path.isdir', return_value=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.emptyFolder')
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_emptybinfolder_setting_is_false_emptyfolder_is_not_called(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock, emptyfolder_mock, isdir_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSetting.return_value = 'outputdir'
        settings_mock.return_value.getSettingAsBool.return_value = False
        
        actual = self.target.run(buildmode = 'build', env = {})

        emptyfolder_mock.assert_not_called('outputdir')

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_window_runcommand_is_called_once(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSettingAsBool.return_value = False
        exec_dict_val = {'key11':'val11'}
        execDict_mock.return_value = exec_dict_val

        actual = self.target.run(buildmode = 'build', env = {})

        self.window_mock.run_command.assert_called_once_with('exec', exec_dict_val)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_createexecdict_is_called_once(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSettingAsBool.return_value = False

        actual = self.target.run(buildmode = 'build', env = {})

        execDict_mock.assert_called_once_with({'env': {}}, 'build', settings_mock.return_value)

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
        filename = 'test-file.asm'
        actual = self.target.parseAnnotations(filename)

        open_mock.return_value.readline.assert_called_once()

    @patch('builtins.open', new_callable=mock_open34, read_data='')
    def test_parseAnnotations_firstline_is_empty(self, open_mock):
        open_mock.return_value.__iter__ = lambda self:self
        open_mock.return_value.__next__ = lambda self: self.readline()
        filename = 'test-file.asm'
        actual = self.target.parseAnnotations(filename)

        self.assertEqual({}, actual)

    @patch('builtins.open', new_callable=mock_open34, read_data='.filenamespace goatPowerExample')
    def test_parseAnnotations_firstline_not_annotation_returns_empty_dict(self, open_mock):
        open_mock.return_value.__iter__ = lambda self:self
        open_mock.return_value.__next__ = lambda self: self.readline()
        filename = 'test-file.asm'
        actual = self.target.parseAnnotations(filename)

        self.assertEqual({}, actual)

    @patch('builtins.open', new_callable=mock_open34, read_data='@kickass-build "test-annotation-1": "val1"')
    def test_parseAnnotations_firstline_is_not_a_comment_returns_empty_dict(self, open_mock):
        open_mock.return_value.__iter__ = lambda self:self
        open_mock.return_value.__next__ = lambda self: self.readline()
        filename = 'test-file.asm'
        actual = self.target.parseAnnotations(filename)

        self.assertEqual({}, actual)

    @patch('builtins.open', new_callable=mock_open34, read_data='// @kickass-not-build "test-annotation-1": "val1"')
    def test_parseAnnotations_firstline_is_a_comment_no_kickassbuild_directive_returns_empty_dict(self, open_mock):
        open_mock.return_value.__iter__ = lambda self:self
        open_mock.return_value.__next__ = lambda self: self.readline()
        filename = 'test-file.asm'
        actual = self.target.parseAnnotations(filename)

        self.assertEqual({}, actual)

    @patch("builtins.open", new_callable=mock_open34, read_data='// @kickass-build "test-annotation-1": "val1", "test-annotation-2": "val2"')
    def test_parseAnnotations_firstline_is_a_comment_has_kickassbuild_directive_returns_parsed_dict(self, open_mock):
        open_mock.return_value.__iter__ = lambda self:self
        open_mock.return_value.__next__ = lambda self: self.readline()
        filename = 'test-file.asm'
        actual = self.target.parseAnnotations(filename)

        self.assertEqual({'test-annotation-1': 'val1', 'test-annotation-2': 'val2'}, actual)

    @patch("builtins.open", new_callable=mock_open34, read_data='// @kickass-build "test-annotation-1"= "val1"')
    def test_parseAnnotations_firstline_is_a_comment_has_kickassbuild_directive_illegal_format_raises_valueerror(self, open_mock):
        open_mock.return_value.__iter__ = lambda self:self
        open_mock.return_value.__next__ = lambda self: self.readline()
        filename = 'test-file.asm'
        with self.assertRaisesRegexp(ValueError, 'Could not parse build annotations: .*') as cm:
            actual = self.target.parseAnnotations(filename)

    @patch('builtins.open', new_callable=mock_open34, read_data='// some-extra-text @kickass-build "test-annotation-1": "val1"')
    def test_parseAnnotations_firstline_is_a_comment_has_kickassbuild_directive_and_extra_text_returns_parsed_dict(self, open_mock):
        filename = 'test-file.asm'
        actual = self.target.parseAnnotations(filename)

        self.assertEqual({'test-annotation-1': 'val1'}, actual)

    @patch('builtins.open', new_callable=mock_open34, read_data='  //  @kickass-build  "test-annotation-1":  "val1" ')
    def test_parseAnnotations_firstline_is_a_comment_has_kickassbuild_directive_and_extra_spaces_returns_parsed_dict(self, open_mock):
        filename = 'test-file.asm'
        actual = self.target.parseAnnotations(filename)

        self.assertEqual({'test-annotation-1': 'val1'}, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', return_value={})
    def test_getFilenameVariables_buildmode_does_not_have_startup_no_annotations_returns_correct_dictionary(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name'})
        actual = self.target.getFilenameVariables('build', settings, self.default_variables)

        self.assertEqual({'build_file_base_name': 'test-file', 'start_filename': 'test-file.prg'}, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', return_value={})
    def test_getFilenameVariables_buildmode_has_startup_no_annotations_returns_correct_dictionary(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name'})
        actual = self.target.getFilenameVariables('build-startup', settings, self.default_variables)

        self.assertEqual({'build_file_base_name': 'test-startup-base-name', 'start_filename': 'test-startup-base-name.prg'}, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', return_value={})
    def test_getFilenameVariables_calls_parseAnnotations_once(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name'})
        actual = self.target.getFilenameVariables('build', settings, self.default_variables)

        parseannotations_mock.assert_called_once_with('test-path/test-file.asm')

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', return_value={'file-to-run': 'test-run-file.ext'})
    def test_getFilenameVariables_has_filetorun_annotation_returns_correct_dictionary(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name'})
        actual = self.target.getFilenameVariables('build', settings, self.default_variables)

        self.assertEqual({'build_file_base_name': 'test-file', 'start_filename': 'test-run-file.ext'}, actual)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.parseAnnotations', return_value={'file-to-not-run': 'test-run-file.ext'})
    def test_getFilenameVariables_has_other_annotation_returns_correct_dictionary(self, parseannotations_mock):
        settings = TestSettings({'kickass_startup_file_path': 'test-startup-base-name'})
        actual = self.target.getFilenameVariables('build', settings, self.default_variables)

        self.assertEqual({'build_file_base_name': 'test-file', 'start_filename': 'test-file.prg'}, actual)

    #TODO: Maybe fix or rework createExecDict tests for all build modes, another file (system tests?)    

if __name__ == '__main__':
    unittest.main()