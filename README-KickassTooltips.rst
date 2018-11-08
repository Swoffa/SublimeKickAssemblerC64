KickassTooltips
============

This is plugin for Sublime Text editor to make working with Kick Assembler (http://www.theweb.dk/KickAssembler/) easier by displaying various helpful tooltip information. The tooltips database can be extended to provide more c64 related info. So far rudimentary help files with Kick Assembler directives, illegal opcodes, VIC registers and SID registers are ready. This plugin was programmed by Roman Dobosz (Gryf/Elysium) and Krzysztof Dabrowski (Brush/Elysium)

Installation
------------

Install it via Package Control or extract the downloaded .zip to your packages directory.

Configuration
-------------

Navigate to Preferences/Package Settings/KickassTooltips and select the configuration file to edit. Currently you can configure:

"css_file": "KickassTooltips/css/default.css"

This is a file that has the css file used to style the tooltips.

    "help_directories": ["KickassTooltips/helpdb"],

This defines the directory where json formatted help files are. Feel free to drop in your own.

    "scopes": ["source.assembly.kickassembler"],

This definies in which scopes the plugin should work. So far it will fire up only in Kick Assembler scope.

    "log_level": "warning"

For the debuggin purposes you can increase the log level to info or debug, open Python console (ctrl-`) and observe what is going on and what problems the plugin has. If you report a bug, please use "debug" level and make sure you copy paset the whole output.

License
-------

It's free to use and modify by anyone provided that we are credited.

