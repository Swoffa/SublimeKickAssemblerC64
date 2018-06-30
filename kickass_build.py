import sublime, sublime_plugin 
import os 
import platform 

# This file is based on work from:
# https://github.com/STealthy-and-haSTy/SublimeScraps/blob/master/build_enhancements/custom_build_variables.py
#
# Huge thanks to OdatNurd!!
 
# List of variable names we want to support 
custom_var_list = ["kickass_run_path", "kickass_debug_path"] 

class KickassBuildCommand(sublime_plugin.WindowCommand):
    """
    Provide custom build variables to a build system, such as a value that needs
    to be specific to a current project.
    """
    def createExecDict(self, sourceDict, buildMode, settings):
        global custom_var_list

        # Save path variable from expansion
        tmpPath = sourceDict.pop('path', None)

        # Create the command
        sourceDict['shell_cmd'] = self.createCommand(sourceDict, buildMode)

        # Variables to expand; start with defaults, then add ours.
        useStartup = 'startup' in buildMode
        variables = self.window.extract_variables()
        variables.update({"build_file_base_name": "Startup" if useStartup else variables["file_base_name"]})
        for custom_var in custom_var_list:
            variables[custom_var] = settings.getSetting(custom_var)
        
        # Create arguments to return by expanding variables in the
        # arguments given.
        args = sublime.expand_variables (sourceDict, variables)

        # Reset path to unexpanded
        if tmpPath:
            args['path'] = tmpPath

        return args
 
    def createMonCommandsScript(self):
        if platform.system()=='Windows':
            return "copy /Y \"bin\\\\${build_file_base_name}.vs\" + \"bin\\\\breakpoints.txt\" \"bin\\\\${build_file_base_name}_MonCommands.mon\")"
        else:
            return "[ -f \"bin/breakpoints.txt\" ] && cat \"bin/${build_file_base_name}.vs\" \"bin/breakpoints.txt\" > \"bin/${build_file_base_name}_MonCommands.mon\" || cat \"bin/${build_file_base_name}.vs\" > \"bin/${build_file_base_name}_MonCommands.mon\""

    def createCommand(self, sourceDict, buildMode):
        compileCommand = "java cml.kickass.KickAssembler \"${build_file_base_name}.${file_extension}\" -log \"bin/${build_file_base_name}_BuildLog.txt\" -o \"bin/${build_file_base_name}_Compiled.prg\" -vicesymbols -showmem -symbolfiledir bin"
        compileDebugCommandAdd = "-afo :afo=true :usebin=true"
        runCommand = "\"${kickass_run_path}\" -moncommands \"bin/${build_file_base_name}.vs\" \"bin/${build_file_base_name}_Compiled.prg\""
        debugCommand = "\"${kickass_debug_path}\" -logfile \"bin/${build_file_base_name}_ViceLog.txt\" -moncommands \"bin/${build_file_base_name}_MonCommands.mon\" \"bin/${build_file_base_name}_Compiled.prg\""
        useRun = 'run' in buildMode
        useDebug = 'debug' in buildMode

        command =  " ".join([compileCommand, compileDebugCommandAdd, "&&", self.createMonCommandsScript()]) if useDebug else compileCommand

        if useDebug:
            command = " ".join([command, "&&", debugCommand])
        elif useRun:
            command = " ".join([command, "&&", runCommand])

        return command

    def run(self, **kwargs):
        buildMode = kwargs.pop('buildmode')
        settings = SublimeSettings(self)

        os.makedirs("bin", exist_ok=True)

        self.window.run_command('exec', self.createExecDict(kwargs, buildMode, settings))

class SublimeSettings():
    def __init__(self, parentCommand):
        # Get the project specific settings
        project_data = parentCommand.window.project_data()
        self.__project_settings = (project_data or {}).get('settings', {})

        # Get the view specific settings
        self.__view_settings = parentCommand.window.active_view().settings()

    def getSetting(self, settingKey): 
        return self.__view_settings.get(settingKey, self.__project_settings.get(settingKey, "")) 

