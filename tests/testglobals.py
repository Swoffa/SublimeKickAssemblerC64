import sublime
import sys

version = sublime.version()

if version < '3000':
    # st2
    kickassbuild = sys.modules["kickass_build"]
else:
    # st3
    kickassbuild = sys.modules["SublimeKickAssemblerC64.kickass_build"]

default_settings_dict = {
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
