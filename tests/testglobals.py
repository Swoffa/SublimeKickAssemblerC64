import sublime
import sys
import io
from unittest.mock import MagicMock, mock_open, file_spec, DEFAULT

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


#Support for readline in mock_open, implemented inb puthon 3.4, sublime uses python 3.3
#Copied from source: https://github.com/python/cpython/blob/master/Lib/unittest/mock.py
#Probably there is a smarter way to extend mock_open, than to copy the whole thing, but I dont know...
def _to_stream(read_data):
    if isinstance(read_data, bytes):
        return io.BytesIO(read_data)
    else:
        return io.StringIO(read_data)
def mock_open34(mock=None, read_data=''):
    """
    A helper function to create a mock to replace the use of `open`. It works
    for `open` called directly or used as a context manager.
    The `mock` argument is the mock object to configure. If `None` (the
    default) then a `MagicMock` will be created for you, with the API limited
    to methods or attributes available on standard file handles.
    `read_data` is a string for the `read`, `readline` and `readlines` of the
    file handle to return.  This is an empty string by default.
    """
    _read_data = _to_stream(read_data)
    _state = [_read_data, None]

    def _readlines_side_effect(*args, **kwargs):
        if handle.readlines.return_value is not None:
            return handle.readlines.return_value
        return _state[0].readlines(*args, **kwargs)

    def _read_side_effect(*args, **kwargs):
        if handle.read.return_value is not None:
            return handle.read.return_value
        return _state[0].read(*args, **kwargs)

    def _readline_side_effect(*args, **kwargs):
        yield from _iter_side_effect()
        while True:
            yield _state[0].readline(*args, **kwargs)

    def _iter_side_effect():
        if handle.readline.return_value is not None:
            while True:
                yield handle.readline.return_value
        for line in _state[0]:
            yield line

    global file_spec
    if file_spec is None:
        import _io
        file_spec = list(set(dir(_io.TextIOWrapper)).union(set(dir(_io.BytesIO))))

    if mock is None:
        mock = MagicMock(name='open', spec=open)

    handle = MagicMock(spec=file_spec)
    handle.__enter__.return_value = handle

    handle.write.return_value = None
    handle.read.return_value = None
    handle.readline.return_value = None
    handle.readlines.return_value = None

    handle.read.side_effect = _read_side_effect
    _state[1] = _readline_side_effect()
    handle.readline.side_effect = _state[1]
    handle.readlines.side_effect = _readlines_side_effect
    handle.__iter__.side_effect = _iter_side_effect

    def reset_data(*args, **kwargs):
        _state[0] = _to_stream(read_data)
        if handle.readline.side_effect == _state[1]:
            # Only reset the side effect if the user hasn't overridden it.
            _state[1] = _readline_side_effect()
            handle.readline.side_effect = _state[1]
        return DEFAULT

    mock.side_effect = reset_data
    mock.return_value = handle
    return mock