Sublime KickAssembler (C64)
===========================
Sublime Package for C64 development with Kick Assembler, 
contains language configuration/syntax coloring, build system and some snippets. Support for OSX, Windows and Linux.
Requires Sublime Text, version 3 is supported. Both the [Vice](http://www.viceteam.org) C64 emulator and the [C64Debugger](https://sourceforge.net/projects/c64-debugger/) C64 emulator/debugger is supported for running/debugging.

Below is a quick start guide, full documentation here: http://goatpower.wordpress.com/projects-releases/sublime-package-kick-assembler-c64/


Installation, OSX
-----------------
 - Ensure a fairly modern version of java is installed (download from http://www.oracle.com/technetwork/java/javase/downloads/index.htm)
 - Download KickAssembler from http://theweb.dk/KickAssembler/, extract to folder `KickAssembler` in your Applications folder (\*)  
   Folder `/Applications/Kick Assembler/` should now contain KickAss.jar and some other files/folders.
 - Download Vice C64 emulator from http://www.viceteam.org/#download, extract to folder `Vice` in your Applications folder (\**)  
   Folder `/Applications/Vice/` should now contain x64 and some other files/folders.
 - Install [Package Control](https://sublime.wbond.net/) for Sublime and install package [Kick Assembler (C64)](https://packagecontrol.io/packages/Kick%20Assembler%20(C64) ), or clone/download this GitHub repository into subfolder of `~/Library/Application Support/Sublime Text 3/Packages/`  

\* If you want a custom path for Kick Assembler, add the full path to KickAss.jar to the CLASSPATH environment variable  
\*\* If you want a custom path for Vice, add the path to the Vice folder containing x64 to the PATH environment variable

Installation, Windows
---------------------
 - Ensure a fairly modern version of java is installed (download from http://www.oracle.com/technetwork/java/javase/downloads/index.htm)
 - Download KickAssembler from http://theweb.dk/KickAssembler/, extract to folder `c:\C64\Tools\KickAssembler\` (\*)  
   Folder `c:\C64\Tools\KickAssembler\` should now contain KickAss.jar and some other files/folders.
 - Download Vice C64 emulator from http://www.viceteam.org/#download, extract to folder `c:\C64\Tools\Vice\` (\*\*)  
   Folder `c:\C64\Tools\Vice\` should now contain x64.exe and some other files/folders.
 - Install [Package Control](https://sublime.wbond.net/) for Sublime and install package [Kick Assembler (C64)](https://packagecontrol.io/packages/Kick%20Assembler%20(C64) ), or clone/download this GitHub repository to subfolder of `%USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\`  

\* If you want a custom path for Kick Assembler, add the full path to KickAss.jar to the CLASSPATH environment variable  
\*\* If you want a custom path for Vice, add the path to the Vice folder containing x64.exe to the PATH environment variable

Installation, Linux
-------------------
I am a complete lamer when it comes to linux, which might or might not make this guide lame. Anyways, it is successfully tested on Ubuntu 14.

- Ensure Java Runtime Environment is installed on your system, if not, look [here](http://www.oracle.com/technetwork/java/javase/downloads/index.htm), or install via ppa using this [guide](http://tecadmin.net/install-oracle-java-8-jdk-8-ubuntu-via-ppa/)
- Download Kick Assembler from http://theweb.dk/KickAssembler/, extract anywhere and ensure the full path to KickAss.jar exist in your CLASSPATH environment variable
- Download/build/install Vice C64 emulator, i followed this [guide](http://askubuntu.com/questions/357331/how-can-i-get-the-vice-c64-commodore-64-emulator-to-work). Ensure the path to the Vice folder (containing x64) exist in your PATH environment variable
- Install [Package Control](https://sublime.wbond.net/) for Sublime and install package [Kick Assembler (C64)](https://packagecontrol.io/packages/Kick%20Assembler%20(C64) ), or clone/download this GitHub repository into subfolder of `~/.config/sublime-text-3/Packages/`  

Develop, build and run
----------------------
 1. Open a Kick Assembler code file in Sublime text. Example code file [here](https://dl.dropbox.com/s/cl7391x5hqwk8zf/GoatPowerExample.asm?dl=1)
 2. Hit the `F7` key to start Build and Run (see below for more build options)
 3. Hopefully watch your lovely code execute! (\*)

\* If you get error saying java is not recognized as an internal or external command, ensure java is installed and add the path to your java binaries folder to the PATH environment variable

Details, Build System
---------------------

Action&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Shortcut macOS | Shortcut Windows | Description
:--|:--|:--|:--
Other build variants (listed below) | `Super+Shift+P` | `Ctrl+Shift+P` | Shows the list of the following variants
Build | `Command+Shift+P`  | `Control+Shift+P` | Compiles the __current__ file.
Build and Run | `F7` | `F7` | Compiles the __current file__ and runs it using the Vice emulator.
Build and Debug | `Shift+F7` | `Shift+F7` | Compiles the __current file__ and runs it using the Vice emulator. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging.
Build Startup | `Command+Shift+B` | `Ctrl+Shift+B` | Compiles __a file with name Startup.asm__ in the same folder as the current file. Handy if you have several code files included in a main runnable file. The filename can be configured via `kickass_startup_file_path` setting.
Build and Run Startup | `F5` | `F5` | Compiles __a file with name Startup.asm__ in the same folder as the current file, and runs it using the Vice emulator. Handy if you have several code files included in a main runnable file. The filename can be configured via `kickass_startup_file_path` setting.
Build and Debug Startup | `Shift+F5` | `Shift+F5` | Compiles __a file with name Startup.asm__ in the same folder as the current file, and runs it using the Vice emulator. Handy if you have several code files included in a main runnable file. __This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging.__ The filename can be configured via `kickass_startup_file_path` setting.
Make | `F8` | `F8` | Invokes a script called `make.bat` for Windows, `make.sh` for macOS (configurable through the `default_make_path` setting).


The following (relevant?) environment variables will be available in the make script:

Variable | Info
:--|:--
`kickass_file` | Filename of active file when command was triggered
`kickass_file_path` | Full path active file when command was triggered
`kickass_prg_file` | Full path for suggested prg file name, for active file when command was triggered
`kickass_bin_folder` | Path to current output folder (`bin` by default or specified by `kickass_output_path` setting)

Pre/post-build
--------------

There's a way to execute custom scripts before/after the build.

Variable | Info
:--|:--
`default_prebuild_path` | Full path to the `.bat` or `.sh` script file that will be executed __before__ the build.
`default_postbuild_path` | Full path to the `.bat` or `.sh` script file that will be executed __after__ the build. Useful for file compression etc.


KickassTooltips
===============

This plugin makes working with Kick Assembler easier by displaying various helpful tooltip information. Tooltips database can be extended to provide more c64 related info. So far rudimentary help files with Kick Assembler directives, illegal opcodes, VIC registers and SID registers are ready. This plugin was added by Roman Dobosz (Gryf/Elysium) and Krzysztof Dabrowski (Brush/Elysium)

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

