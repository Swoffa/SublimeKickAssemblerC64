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
custom_var_list = ["kickass_run_path",
                   "kickass_debug_path",
                   "kickass_jar_path",
                   "kickass_args",
                   "kickass_run_args",
                   "kickass_debug_args",
                   "kickass_startup_file_path",
                   "kickass_breakpoint_filename",
                   "kickass_compiled_filename",
                   "kickass_output_path",
                   "default_prebuild_path",
                   "default_postbuild_path"]

vars_to_expand_list = ["kickass_compiled_filename"]

class KickassBuildCommand(sublime_plugin.WindowCommand):
    """
    Provide custom build variables to a build system, such as a value that needs
    to be specific to a current project.
    """
    def createExecDict(self, sourceDict, buildMode, settings):
        global custom_var_list, vars_to_expand_list
        global hasDefaultPreCommand, hasPreCommand
        global hasDefaultPostCommand, hasPostCommand

        # Save path variable from expansion
        tmpPath = sourceDict.pop('path', None)

        # Create the command
        sourceDict['shell_cmd'] = self.createCommand(sourceDict, buildMode, settings)

        # Add pre and post variables
        extendedDict = self.addPrePostVarsToDict(sourceDict, buildMode) if (hasPreCommand or hasPostCommand or hasDefaultPreCommand or hasDefaultPostCommand) else sourceDict

        # Variables to expand; start with defaults, then add ours.
        useStartup = 'startup' in buildMode
        variables = self.window.extract_variables()
        variables.update({"build_file_base_name": settings.getSetting("kickass_startup_file_path") if useStartup else variables["file_base_name"]})
        for custom_var in custom_var_list:
            variables[custom_var] = settings.getSetting(custom_var)

        # Expand variables
        variables_to_expand = {k: v for k, v in variables.items() if k in vars_to_expand_list}
        variables = self.mergeDictionaries(variables, sublime.expand_variables (variables_to_expand, variables))

        # Create arguments to return by expanding variables in the
        # arguments given.
        args = sublime.expand_variables (extendedDict, variables)

        # Reset path to unexpanded add path addition from settings
        args['path'] = self.getPathDelimiter().join([settings.getSetting("kickass_path"), tmpPath])

        return args
 
    def createMonCommandsScript(self):
        if platform.system()=='Windows':
            return "copy /Y \"${kickass_output_path}\\\\${build_file_base_name}.vs\" + \"${kickass_output_path}\\\\${kickass_breakpoint_filename}\" \"${kickass_output_path}\\\\${build_file_base_name}_MonCommands.mon\""
        else:
            return "[ -f \"${kickass_output_path}/${kickass_breakpoint_filename}\" ] && cat \"${kickass_output_path}/${build_file_base_name}.vs\" \"${kickass_output_path}/${kickass_breakpoint_filename}\" > \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\" || cat \"${kickass_output_path}/${build_file_base_name}.vs\" > \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\""
 
    def addPrePostVarsToDict(self, sourceDict, buildMode):
        prePostEnvVars = {
            "kickass_buildmode": buildMode,
            "kickass_file": "${build_file_base_name}.${file_extension}",
            "kickass_file_path": "${file_path}",
            "kickass_prg_file": "${file_path}/${kickass_output_path}/${kickass_compiled_filename}",
            "kickass_bin_folder": "${file_path}/${kickass_output_path}",
            }
        sourceDict.get('env').update(prePostEnvVars)
        return sourceDict

    def evaluatePrePostCommands(self, settings):
        global defaultPreCommand, preCommand
        global hasDefaultPreCommand, hasPreCommand
        preCommandFilename = "prebuild"
        defaultPreCommand = "%s/%s.%s" % (settings.getSetting("default_prebuild_path"), preCommandFilename, self.getExt())
        hasDefaultPreCommand = glob.glob(defaultPreCommand)
        preCommand = "%s.%s" % (preCommandFilename, self.getExt())
        hasPreCommand = glob.glob(preCommand)

        global defaultPostCommand, postCommand
        global hasDefaultPostCommand, hasPostCommand
        postCommandFilename = "postbuild"
        defaultPostCommand = "%s/%s.%s" % (settings.getSetting("default_postbuild_path"), postCommandFilename, self.getExt())
        hasDefaultPostCommand = glob.glob(defaultPostCommand)
        postCommand = "%s.%s" % (postCommandFilename, self.getExt())
        hasPostCommand = glob.glob(postCommand)

    def getPathDelimiter(self):
        return ";" if platform.system()=='Windows' else ":" 

    def getExt(self): 
        return "bat" if platform.system()=='Windows' else "sh" 
 
    def getRunScriptStatement(self, scriptname): 
        return "call "+scriptname if platform.system()=='Windows' else ". "+scriptname 
 
    def createCommand(self, sourceDict, buildMode, settings): 
        javaCommand = "java -cp \"${kickass_jar_path}\"" if settings.getSetting("kickass_jar_path") else "java"  
        compileCommand = javaCommand+" cml.kickass.KickAssembler \"${build_file_base_name}.${file_extension}\" -log \"${kickass_output_path}/${build_file_base_name}_BuildLog.txt\" -o \"${kickass_output_path}/${kickass_compiled_filename}\" -vicesymbols -showmem -symbolfiledir ${kickass_output_path} ${kickass_args}"
        compileDebugCommandAdd = "-afo :afo=true :use${kickass_output_path}=true"
        runCommand = "\"${kickass_run_path}\" ${kickass_run_args} -logfile \"${kickass_output_path}/${build_file_base_name}_ViceLog.txt\" -moncommands \"${kickass_output_path}/${build_file_base_name}.vs\" \"${kickass_output_path}/${kickass_compiled_filename}\""
        debugCommand = "\"${kickass_debug_path}\" ${kickass_debug_args} -logfile \"${kickass_output_path}/${build_file_base_name}_ViceLog.txt\" -moncommands \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\" \"${kickass_output_path}/${kickass_compiled_filename}\""
        useRun = 'run' in buildMode
        useDebug = 'debug' in buildMode

        command =  " ".join([compileCommand, compileDebugCommandAdd, "&&", self.createMonCommandsScript()]) if useDebug else compileCommand

        self.evaluatePrePostCommands(settings)

        if hasPreCommand or hasDefaultPreCommand:
            command = " ".join([self.getRunScriptStatement(preCommand if hasPreCommand else defaultPreCommand), "&&", command])
        if hasPostCommand or hasDefaultPostCommand:
            command = " ".join([command, "&&", self.getRunScriptStatement(postCommand if hasPostCommand else defaultPostCommand)])
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

    def mergeDictionaries(self, x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z

    def run(self, **kwargs):
        settings = SublimeSettings(self)
        outputFolder = settings.getSetting("kickass_output_path")

        # os.makedirs() caused trouble with Python versions < 3.4.1 (see https://docs.python.org/3/library/os.html#os.makedirs);
        # to avoid abortion (on UNIX-systems) here, we simply wrap the call with a try-except
        # (the output-directory will be generated anyway via the output-parameter in the compile-command)
        try:
            os.makedirs(outputFolder, exist_ok=True)
        except:
            pass

        if settings.getSettingAsBool("kickass_empty_bin_folder_before_build") and os.path.isdir(outputFolder):
            self.emptyFolder(outputFolder)

        self.window.run_command('exec', self.createExecDict(kwargs, kwargs.pop('buildmode'), settings))

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
