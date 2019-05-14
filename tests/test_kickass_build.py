import sublime
import sys
import os
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch, create_autospec, mock_open
from testsettings import TestSettings
from module_references import kickassbuild

#Use project path as root, if exist?
#Use platform from variables

all_settings_dict = {
            "kickass_run_path": "x64",
            "kickass_debug_path": "x64",
            "kickass_startup_file_path": "Startup",
            "kickass_empty_bin_folder_before_build" : "true",
            "kickass_breakpoint_filename" : "breakpoints.txt",
            "kickass_compiled_filename": "${build_file_base_name}.prg",
            "kickass_output_path": "bin",
            "default_prebuild_path": "",
            "default_postbuild_path": "",
            "default_make_path": "",
            "kickass_debug_command_c64debugger": "\"${kickass_debug_path}\" -autojmp -layout 10 -breakpoints \"${kickass_output_path}/${kickass_breakpoint_filename}\" -symbols \"${kickass_output_path}/${build_file_base_name}.vs\" -wait 2500 -prg \"${kickass_output_path}/${start_filename}\"",
            "kickass_debug_command_x64": "\"${kickass_debug_path}\" -logfile \"${kickass_output_path}/${build_file_base_name}_ViceLog.txt\" -moncommands \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\" ${kickass_debug_args} \"${kickass_output_path}/${start_filename}\"",
            "kickass_run_command_x64": "\"${kickass_run_path}\" -logfile \"${kickass_output_path}/${build_file_base_name}_ViceLog.txt\" -moncommands \"${kickass_output_path}/${build_file_base_name}.vs\" ${kickass_run_args} \"${kickass_output_path}/${start_filename}\"",
            "kickass_run_command_c64debugger": "\"${kickass_run_path}\" -autojmp -layout 1 -symbols \"${kickass_output_path}/${build_file_base_name}.vs\" -wait 2500 -prg \"${kickass_output_path}/${start_filename}\"",
            "kickass_compile_args": "\"${build_file_base_name}.${file_extension}\" -log \"${kickass_output_path}/${build_file_base_name}_BuildLog.txt\" -o \"${kickass_output_path}/${build_file_base_name}.prg\" -vicesymbols -showmem -odir \"${kickass_output_path}\" ${kickass_args}",
            "kickass_compile_debug_additional_args": "-afo :afo=true"
            }

class TestKickassBuildCommand(TestCase):

    def setUp(self):
        self.platform_system_patch = patch('platform.system')
        self.platform_system = self.platform_system_patch.start()
        self.platform_system.return_value = 'Darwin'

        self.window_mock = Mock()
        self.window_mock.extract_variables.return_value = {
            #'file_name': 'Test.asm', 
            #'platform': 'Windows', 
            #'packages': 'C:\\Users\\SimonOskarsson\\AppData\\Roaming\\Sublime Text 3\\Packages', 
            #'folder': filePath, 
            #'file': filePath+'Test.asm', 
            'file_extension': 'asm', 
            'file_path': '', 
            'file_base_name': 'Test'
            }

        self.settings_mock = create_autospec(kickassbuild.SublimeSettings)
        self.settings_mock.getSetting.return_value = ''

        self.all_settings = TestSettings(all_settings_dict)

        self.target = kickassbuild.KickassBuildCommand(self.window_mock)

        self.maxDiff = None

    def tearDown(self):
        self.platform_system_patch.stop()

    def test_getPathDelimiter_platformiswindows_returnsemicolon(self):
        self.platform_system.return_value = 'Windows'

        actual = self.target.getPathDelimiter()

        self.assertEqual(';', actual)

    def test_getPathDelimiter_platformislinux_returncolon(self):
        self.platform_system.return_value = 'Linux'

        actual = self.target.getPathDelimiter()

        self.assertEqual(':', actual)

    def test_getPathDelimiter_platformisDarwin_returncolon(self):
        self.platform_system.return_value = 'Darwin'

        actual = self.target.getPathDelimiter()

        self.assertEqual(':', actual)

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmodeisbuild_sourcedictitemsisreturned(self, file_mock):
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

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmodeisbuild_returndictionarywithcorrectbuildcommand(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "Test.asm" -log "bin/Test_BuildLog.txt" -o "bin/Test.prg" -vicesymbols -showmem -odir "bin" '

        actual = self.target.createExecDict(sourceDict, 'build', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmodeisbuildstartup_returndictionarywithcorrectbuildcommand(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "Startup.asm" -log "bin/Startup_BuildLog.txt" -o "bin/Startup.prg" -vicesymbols -showmem -odir "bin" '

        actual = self.target.createExecDict(sourceDict, 'build-startup', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmodeisbuildandrun_returndictionarywithcorrectbuildcommand(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "Test.asm" -log "bin/Test_BuildLog.txt" -o "bin/Test.prg" -vicesymbols -showmem -odir "bin"   && "x64" -logfile "bin/Test_ViceLog.txt" -moncommands "bin/Test.vs"  "bin/Test.prg"'

        actual = self.target.createExecDict(sourceDict, 'build-and-run', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmodeisbuildandrunstartup_returndictionarywithcorrectbuildcommand(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "Startup.asm" -log "bin/Startup_BuildLog.txt" -o "bin/Startup.prg" -vicesymbols -showmem -odir "bin"   && "x64" -logfile "bin/Startup_ViceLog.txt" -moncommands "bin/Startup.vs"  "bin/Startup.prg"'

        actual = self.target.createExecDict(sourceDict, 'build-and-run-startup', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmodeisbuildandrun_returndictionarywithcorrectbuildcommand(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "Test.asm" -log "bin/Test_BuildLog.txt" -o "bin/Test.prg" -vicesymbols -showmem -odir "bin"   -afo :afo=true && [ -f "bin/breakpoints.txt" ] && cat "bin/Test.vs" "bin/breakpoints.txt" > "bin/Test_MonCommands.mon" || cat "bin/Test.vs" > "bin/Test_MonCommands.mon" && "x64" -logfile "bin/Test_ViceLog.txt" -moncommands "bin/Test_MonCommands.mon"  "bin/Test.prg"'

        actual = self.target.createExecDict(sourceDict, 'build-and-debug', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    def test_createExecDict_buildmodeisbuildandrunstartup_returndictionarywithcorrectbuildcommand(self, file_mocks):
        sourceDict = {}
        expected = 'java cml.kickass.KickAssembler "Startup.asm" -log "bin/Startup_BuildLog.txt" -o "bin/Startup.prg" -vicesymbols -showmem -odir "bin"   -afo :afo=true && [ -f "bin/breakpoints.txt" ] && cat "bin/Startup.vs" "bin/breakpoints.txt" > "bin/Startup_MonCommands.mon" || cat "bin/Startup.vs" > "bin/Startup_MonCommands.mon" && "x64" -logfile "bin/Startup_ViceLog.txt" -moncommands "bin/Startup_MonCommands.mon"  "bin/Startup.prg"'

        actual = self.target.createExecDict(sourceDict, 'build-and-debug-startup', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    def test_createExecDict_buildmodeismake_returndictionarywithcorrectmakecommand(self, glob_mock, file_mock):
        sourceDict = {'env':{}}
        expected = '. "make.sh"'

        actual = self.target.createExecDict(sourceDict, 'make', self.all_settings)

        self.assertEqual(expected, actual['shell_cmd'])

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    def test_createExecDict_buildmodeismake_returndictionarywithcorrectenvvariables(self, glob_mock, file_mock):
        sourceDict = {'env':{}}
        expected = {
            'kickass_buildmode': 'make', 
            'kickass_file': 'Test.asm', 
            'kickass_file_path': '', 
            'kickass_bin_folder': '/bin', 
            'kickass_prg_file': '/bin/Test.prg'
            }

        actual = self.target.createExecDict(sourceDict, 'make', self.all_settings)

        self.assertEqual(expected, actual['env'])

    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    @patch('sublime.error_message')
    def test_run_settingsnotloaded_returnwitherrormessage(self, sublime_error_mock, settings_mock, glob_mock, file_mock):
        settings_mock.return_value.isLoaded.return_value = False

        actual = self.target.run(buildmode = 'build', env = {})

        sublime_error_mock.assert_called_once_with("Settings could not be loaded, please restart Sublime Text.")
        settings_mock.getSetings.assert_not_called()


    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_allconditionsvalid_createsoutputdirfromsetting(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSetting.return_value = 'outputdir'

        actual = self.target.run(buildmode = 'build', env = {})

        os_mock.assert_called_once_with('outputdir', exist_ok=True)

    @patch('os.path.isdir', return_value=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.emptyFolder')
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_emptybinfolderisenabled_emptyfolderiscalled(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock, emptyfolder_mock, isdir_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSetting.return_value = 'outputdir'
        settings_mock.return_value.getSettingAsBool.return_value = True
        
        actual = self.target.run(buildmode = 'build', env = {})

        emptyfolder_mock.assert_called_once_with('outputdir')

    @patch('os.path.isdir', return_value=True)
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.emptyFolder')
    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_emptybinfolderisdisabled_emptyfolderisnotcalled(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock, emptyfolder_mock, isdir_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSetting.return_value = 'outputdir'
        settings_mock.return_value.getSettingAsBool.return_value = False
        
        actual = self.target.run(buildmode = 'build', env = {})

        emptyfolder_mock.assert_not_called('outputdir')

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_allconditionsvalid_windowruncommandiscalledonce(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSettingAsBool.return_value = False
        exec_dict_val = {'key11':'val11'}
        execDict_mock.return_value = exec_dict_val

        actual = self.target.run(buildmode = 'build', env = {})

        self.window_mock.run_command.assert_called_once_with('exec', exec_dict_val)

    @patch('SublimeKickAssemblerC64.kickass_build.KickassBuildCommand.createExecDict')
    @patch('builtins.open', new_callable=mock_open, read_data='.filenamespace goatPowerExample')
    @patch('glob.glob', return_value=True)
    @patch('os.makedirs')
    @patch('SublimeKickAssemblerC64.kickass_build.SublimeSettings')
    def test_run_allconditionsvalid_createexecdictiscalledonce(self, settings_mock, os_mock, glob_mock, file_mock, execDict_mock):
        settings_mock.return_value.isLoaded.return_value = True
        settings_mock.return_value.getSettingAsBool.return_value = False

        actual = self.target.run(buildmode = 'build', env = {})

        execDict_mock.assert_called_once_with({'env': {}}, 'build', settings_mock.return_value)

    #TODO: mergeDictionaries
    #TODO: emptyFolder
    #TODO: parseAnnotations
    #TODO: getFilenameVariables
    #TODO: Maybe fix or rework createExecDict tests for all build modes, another file (integration tests? use run?)    

if __name__ == '__main__':
    unittest.main()