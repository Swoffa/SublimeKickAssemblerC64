import sublime, sublime_plugin 
import os 
import platform 
import glob
import shutil

# This file is based on work from:
# https://github.com/STealthy-and-haSTy/SublimeScraps/blob/master/build_enhancements/custom_build_variables.py
#
# Huge thanks to OdatNurd!!
 
# List of variable names we want to support 
custom_var_list = ["kickass_run_path", "kickass_debug_path", "kickass_jar_path", 
"kickass_args", "kickass_run_args", "kickass_debug_args", 
"kickass_startup_file_path", "kickass_breakpoint_filename"]

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
        sourceDict['shell_cmd'] = self.createCommand(sourceDict, buildMode, settings)

        # Add pre and post variables
        extendedDict = self.addPrePostVarsToDict(sourceDict, buildMode) if (hasPreCommand or hasPostCommand) else sourceDict

        # Variables to expand; start with defaults, then add ours.
        useStartup = 'startup' in buildMode
        variables = self.window.extract_variables()
        variables.update({"build_file_base_name": settings.getSetting("kickass_startup_file_path") if useStartup else variables["file_base_name"]})
        for custom_var in custom_var_list:
            variables[custom_var] = settings.getSetting(custom_var)

        # Create arguments to return by expanding variables in the
        # arguments given.
        args = sublime.expand_variables (extendedDict, variables)

        # Reset path to unexpanded add path addition from settings
        args['path'] = self.getPathDelimiter().join([settings.getSetting("kickass_path"), tmpPath])

        return args
 
    def createMonCommandsScript(self):
        if platform.system()=='Windows':
            return "copy /Y \"bin\\\\${build_file_base_name}.vs\" + \"bin\\\\${kickass_breakpoint_filename}\" \"bin\\\\${build_file_base_name}_MonCommands.mon\""
        else:
            return "[ -f \"bin/${kickass_breakpoint_filename}\" ] && cat \"bin/${build_file_base_name}.vs\" \"bin/${kickass_breakpoint_filename}\" > \"bin/${build_file_base_name}_MonCommands.mon\" || cat \"bin/${build_file_base_name}.vs\" > \"bin/${build_file_base_name}_MonCommands.mon\""
 
    def addPrePostVarsToDict(self, sourceDict, buildMode):
        prePostEnvVars = {
            "kickass_buildmode": buildMode,
            "kickass_file": "${build_file_base_name}.${file_extension}",
            "kickass_file_path": "${file_path}",
            "kickass_prg_file": "${file_path}/bin/${build_file_base_name}_Compiled.prg",
            "kickass_bin_folder": "${file_path}/bin",
            }
        sourceDict.get('env').update(prePostEnvVars)
        return sourceDict

    def getPathDelimiter(self): 
        return ";" if platform.system()=='Windows' else ":" 

    def getExt(self): 
        return "bat" if platform.system()=='Windows' else "sh" 
 
    def getRunScriptStatement(self, scriptname): 
        return "call "+scriptname if platform.system()=='Windows' else ". "+scriptname 
 
    def createCommand(self, sourceDict, buildMode, settings): 
        javaCommand = "java -cp \"${kickass_jar_path}\"" if settings.getSetting("kickass_jar_path") else "java"  
        compileCommand = javaCommand+" cml.kickass.KickAssembler \"${build_file_base_name}.${file_extension}\" -log \"bin/${build_file_base_name}_BuildLog.txt\" -o \"bin/${build_file_base_name}_Compiled.prg\" -vicesymbols -showmem -symbolfiledir bin ${kickass_args}"
        compileDebugCommandAdd = "-afo :afo=true :usebin=true"
        runCommand = "\"${kickass_run_path}\" ${kickass_run_args} -logfile \"bin/${build_file_base_name}_ViceLog.txt\" -moncommands \"bin/${build_file_base_name}.vs\" \"bin/${build_file_base_name}_Compiled.prg\""
        debugCommand = "\"${kickass_debug_path}\" ${kickass_debug_args} -logfile \"bin/${build_file_base_name}_ViceLog.txt\" -moncommands \"bin/${build_file_base_name}_MonCommands.mon\" \"bin/${build_file_base_name}_Compiled.prg\""
        useRun = 'run' in buildMode
        useDebug = 'debug' in buildMode

        command =  " ".join([compileCommand, compileDebugCommandAdd, "&&", self.createMonCommandsScript()]) if useDebug else compileCommand

        if hasPreCommand:
            command = " ".join([self.getRunScriptStatement(preCommand), "&&", command])
        if hasPostCommand:
            command = " ".join([command, "&&", self.getRunScriptStatement(postCommand)])
        if useDebug:
            command = " ".join([command, "&&", debugCommand])
        elif useRun:
            command = " ".join([command, "&&", runCommand])

        return command

    def emptyFolder(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def run(self, **kwargs):
        global preCommand, postCommand, hasPreCommand, hasPostCommand
        buildMode = kwargs.pop('buildmode')
        settings = SublimeSettings(self)
        preCommand = "prebuild."+self.getExt()
        postCommand = "postbuild."+self.getExt()
        hasPreCommand = glob.glob(preCommand)
        hasPostCommand =  glob.glob(postCommand)

        # os.makedirs() caused trouble with Python versions < 3.4.1 (see https://docs.python.org/3/library/os.html#os.makedirs);
        # to avoid abortion (on UNIX-systems) here, we simply wrap the call with a try-except
        # (the "bin"-directory will be generated anyway via the output-parameter in the compile-command)
        try:
            os.makedirs("bin", exist_ok=True)
        except:
            pass

        if settings.getSettingAsBool("kickass_empty_bin_folder_before_build") and os.path.isdir("bin"):
            self.emptyFolder("bin")

        self.window.run_command('exec', self.createExecDict(kwargs, buildMode, settings))

class SublimeSettings():
    def __init__(self, parentCommand):
        # Get the project specific settings
        project_data = parentCommand.window.project_data()
        self.__project_settings = (project_data or {}).get('settings', {})

        # Get the view specific settings
        self.__view_settings = parentCommand.window.active_view().settings()

        self.__default_settings = sublime.load_settings("KickAssembler (C64).sublime-settings")

    def getSetting(self, settingKey): 
        return self.__view_settings.get(settingKey, self.__project_settings.get(settingKey, self.__default_settings.get(settingKey, "")))

    def getSettingAsBool(self, settingKey): 
        return self.getSetting(settingKey).lower() == "true"
