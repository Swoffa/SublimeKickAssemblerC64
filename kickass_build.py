# This file is based on work from:
# https://github.com/STealthy-and-haSTy/SublimeScraps/blob/master/build_enhancements/custom_build_variables.py
#
# Huge thanks to OdatNurd!!
 
# List of variable names we want to support 
custom_var_list = ["kickass_run_path", "kickass_debug_path"] 
custom_var_list_defaults = { 
    "kickass_run_path": "x64", 
    "kickass_debug_path": "x64" 
    } 

class KickassBuildCommand(sublime_plugin.WindowCommand):
    """
    Provide custom build variables to a build system, such as a value that needs
    to be specific to a current project.
    """
    def createExecDict(self, sourceDict, additionalVariables):
        global custom_var_list

        # Get the project specific settings
        project_data = self.window.project_data ()
        project_settings = (project_data or {}).get ('settings', {})

        # Get the view specific settings
        view_settings = self.window.active_view ().settings ()

        # Variables to expand; start with defaults, then add ours.
        variables = self.window.extract_variables ()
        variables.update(additionalVariables)
        for custom_var in custom_var_list:
            variables[custom_var] = view_settings.get (custom_var,
                project_settings.get (custom_var, custom_var_list_defaults.get(custom_var,"")))
        
        # Create arguments to return by expanding variables in the
        # arguments given.
        args = sublime.expand_variables (sourceDict, variables)

        # Rename the command parameter to what exec expects.
        args['shell_cmd'] = args.pop ('command')

        return args

    def createMonCommandsScript(self):
        if platform.system()=='Windows':
            return "copy /Y \"bin\\\\${build_file_base_name}.vs\" + \"bin\\\\breakpoints.txt\" \"bin\\\\${build_file_base_name}_MonCommands.mon\")"
        else:
            return "[ -f \"bin/breakpoints.txt\" ] && cat \"bin/${build_file_base_name}.vs\" \"bin/breakpoints.txt\" > \"bin/${build_file_base_name}_MonCommands.mon\" || cat \"bin/${build_file_base_name}.vs\" > \"bin/${build_file_base_name}_MonCommands.mon\""

    def createCommand(self, sourceDict):
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

    def createAdditionalVaiables(self):
        global buildMode
        variables = self.window.extract_variables()
        useStartup = 'startup' in buildMode
        return {"build_file_base_name": "Startup" if useStartup else variables["file_base_name"]}

    def run(self, **kwargs):
        global buildMode
        buildMode = kwargs.pop('buildmode')

        os.makedirs("bin", exist_ok=True)

        kwargs['command'] = self.createCommand(kwargs)
        additionalVariables = self.createAdditionalVaiables()
        self.window.run_command('exec', self.createExecDict(kwargs, additionalVariables))