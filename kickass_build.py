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
custom_var_list = [ "kickass_compile_args",
                    "kickass_compile_debug_additional_args",
                    "kickass_run_command_c64debugger",
                    "kickass_debug_command_c64debugger",
                    "kickass_run_command_x64",
                    "kickass_debug_command_x64",
                    "kickass_run_path",
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

vars_to_expand_list = [ 
                        "kickass_compiled_filename",
                        "kickass_args",
                        "kickass_run_args",
                        "kickass_debug_args",
                        "kickass_compile_args",
                        "kickass_run_command_x64",
                        "kickass_debug_command_x64",
                        "kickass_run_command_c64debugger",
                        "kickass_debug_command_c64debugger",
                        ]

class KickassBuildCommand(sublime_plugin.WindowCommand):
    """
    Provide custom build variables to a build system, such as a value that needs
    to be specific to a current project.
    """
    def createExecDict(self, sourceDict, buildMode, settings):
        global custom_var_list, vars_to_expand_list

        # Save path variable from expansion
        tmpPath = sourceDict.pop('path', None)

        # Variables to expand; start with defaults, then add ours.
        variables = self.window.extract_variables()
        useStartup = 'startup' in buildMode
        variables.update({"build_file_base_name": settings.getSetting("kickass_startup_file_path") if useStartup else variables["file_base_name"]})

        # Create the command
        kickAssCommand = KickAssCommandFactory(settings).createCommand(variables, buildMode)
        sourceDict['shell_cmd'] = kickAssCommand.CommandText

        # Add pre and post variables
        extendedDict = kickAssCommand.updateEnvVars(sourceDict)

        for custom_var in custom_var_list:
            variables[custom_var] = settings.getSetting(custom_var)

        # Expand variables
        variables_to_expand = {k: v for k, v in variables.items() if k in vars_to_expand_list}
        variables = self.mergeDictionaries(variables, sublime.expand_variables (variables_to_expand, variables))

        # Create arguments to return by expanding variables in the
        # arguments given.
        args = sublime.expand_variables (extendedDict, variables)

        # Reset path to unexpanded and add path addition from settings
        args['path'] = self.getPathDelimiter().join([settings.getSetting("kickass_path"), tmpPath])

        envSetting = settings.getSetting("kickass_env")
        if envSetting:
            args['env'].update(envSetting)

        return args

    def getPathDelimiter(self):
        return ";" if platform.system()=='Windows' else ":" 

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
        if not settings.isLoaded(): 
            errorMessage = "Settings could not be loaded, please restart Sublime Text."
            sublime.error_message(errorMessage) 
            print(errorMessage)
            return

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

    def isLoaded(self):
        return self.__getSetting("kickass_output_path") != None

    def getSetting(self, settingKey):
        setting = self.__getSetting(settingKey)
        return setting if setting else ""

    def __getSetting(self, settingKey): 
        return self.__view_settings.get(settingKey, self.__project_settings.get(settingKey, None))

    def getSettingAsBool(self, settingKey): 
        return self.getSetting(settingKey).lower() == "true"

class KickAssCommand():
    def __init__(self, commandText, hasPreCommand, hasPostCommand, buildMode):
        self.__commandText = commandText
        self.__hasPreCommand = hasPreCommand
        self.__hasPostCommand = hasPostCommand
        self.__buildMode = buildMode

    @property
    def CommandText(self):
        return self.__commandText

    def updateEnvVars(self, sourceDict):
        if not self.__hasPreCommand and not self.__hasPostCommand: return sourceDict
        prePostEnvVars = {
            "kickass_buildmode": self.__buildMode,
            "kickass_file": "${build_file_base_name}.${file_extension}",
            "kickass_file_path": "${file_path}",
            "kickass_prg_file": "${file_path}/${kickass_output_path}/${kickass_compiled_filename}",
            "kickass_bin_folder": "${file_path}/${kickass_output_path}",
            }
        sourceDict.get('env').update(prePostEnvVars)
        return sourceDict

class KickAssCommandFactory():
    def __init__(self, settings):
        self.__settings = settings
 
    def createCommand(self, variables, buildMode): 
        return self.createMakeCommand(variables, buildMode) if buildMode=="make" else self.createKickassCommand(variables, buildMode)

    def createMakeCommand(self, variables, buildMode): 
        makeCommand = self.getRunScriptStatement("make", "default_make_path")
        makeCommand = makeCommand if makeCommand else "echo Make file not found. Place a file named make.%s in ${file_path}%s" % (self.getExt(), " or %s." % (self.__settings.getSetting("default_make_path")) if self.__settings.getSetting("default_make_path") else ".")
        return KickAssCommand(makeCommand, True, False, buildMode)

    def createKickassCommand(self, variables, buildMode): 
        javaCommand = "java -cp \"${kickass_jar_path}\"" if self.__settings.getSetting("kickass_jar_path") else "java"  
        compileCommand = javaCommand+" cml.kickass.KickAssembler ${kickass_compile_args} "
        compileDebugCommandAdd = "${kickass_compile_debug_additional_args}"

        runCommand = "${kickass_run_command_x64}" 
        if "c64debugger" in self.__settings.getSetting("kickass_run_path").lower():
            runCommand = "${kickass_run_command_c64debugger}" 

        debugCommand = "${kickass_debug_command_x64}"
        if "c64debugger" in self.__settings.getSetting("kickass_debug_path").lower():
            debugCommand = "${kickass_debug_command_c64debugger}" 

        useRun = 'run' in buildMode
        useDebug = 'debug' in buildMode

        command =  " ".join([compileCommand, compileDebugCommandAdd, "&&", self.createMonCommandsStatement()]) if useDebug else compileCommand

        preBuildScript = self.getRunScriptStatement("prebuild", "default_prebuild_path")
        postBuildScript = self.getRunScriptStatement("postbuild", "default_postbuild_path")

        if preBuildScript:
            command = " ".join([preBuildScript, "&&", command])
        if postBuildScript:
            command = " ".join([command, "&&", postBuildScript])
        if useDebug:
            command = " ".join([command, "&&", debugCommand])
        elif useRun:
            command = " ".join([command, "&&", runCommand])

        return KickAssCommand(command, preBuildScript != None, postBuildScript != None, buildMode)

    def getExt(self): 
        return "bat" if platform.system()=='Windows' else "sh" 

    def getRunScriptStatement(self, scriptFilename, defaultScriptPathSetting):
        defaultScriptCommand = "%s/%s.%s" % (self.__settings.getSetting(defaultScriptPathSetting), scriptFilename, self.getExt())
        hasDefaultScriptCommand = glob.glob(defaultScriptCommand)
        scriptCommand = "%s.%s" % (scriptFilename, self.getExt())
        hasScriptCommand = glob.glob(scriptCommand)
        return "%s \"%s\"" % ("call" if platform.system()=='Windows' else ".", (scriptCommand if hasScriptCommand else defaultScriptCommand)) if hasScriptCommand or hasDefaultScriptCommand else None 
 
    def createMonCommandsStatement(self):
        if platform.system()=='Windows':
            return "copy /Y \"${kickass_output_path}\\\\${build_file_base_name}.vs\" + \"${kickass_output_path}\\\\${kickass_breakpoint_filename}\" \"${kickass_output_path}\\\\${build_file_base_name}_MonCommands.mon\""
        else:
            return "[ -f \"${kickass_output_path}/${kickass_breakpoint_filename}\" ] && cat \"${kickass_output_path}/${build_file_base_name}.vs\" \"${kickass_output_path}/${kickass_breakpoint_filename}\" > \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\" || cat \"${kickass_output_path}/${build_file_base_name}.vs\" > \"${kickass_output_path}/${build_file_base_name}_MonCommands.mon\""