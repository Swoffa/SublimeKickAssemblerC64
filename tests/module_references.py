import sublime
import sys

version = sublime.version()

if version < '3000':
    # st2
    kickassbuild = sys.modules["kickass_build"]
else:
    # st3
    kickassbuild = sys.modules["SublimeKickAssemblerC64.kickass_build"]