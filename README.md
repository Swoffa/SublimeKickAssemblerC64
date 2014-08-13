SublimeKickAssemblerC64
=======================
Sublime Package for for C64 development with Kick Assembler, 
contains language configuration/syntax coloring, build system and some snippets. Support for Windows and OSX.

Installation With Package Control, OSX and Windows
-----------------
Install [Package Control](https://sublime.wbond.net/) for Sublime and install package [Kick Assembler (C64)](https://sublime.wbond.net/packages/Kick%20Assembler%20(C64))

Manual installation, OSX
-----------------
 - Download KickAssembler from http://theweb.dk/KickAssembler/, extract to folder KickAssembler in your Applications folder (\*)  
   Folder /Applications/Kick Assembler/ should now contain KickAss.jar and some other files/folders.
 - Download Vice C64 emulator from http://www.viceteam.org/#download, extract to folder Vice in your Applications folder (\**)  
   Folder /Applications/Vice/ should now contain x64 and some other files/folders.
 - Clone or download this GitHub repository into subfolder of ~/Library/Application Support/Sublime Text 3/Packages/  

\* If you did not use the recommended path for Kick Assembler in step 1, add the path to KickAss.jar to the CLASSPATH environment variable, or edit file KickAss.sublime-build in folder ~/Library/Application Support/Sublime Text 3/Packages/ with the correct path to Kick Assembler  
\*\* If you did not use the recommended path for Vice in step 2, edit file KickAss.sublime-build in folder ~/Library/Application Support/Sublime Text 3/Packages/ with the correct path to Vice

Manual installation, Windows
---------------------
 - Ensure a fairly modern version of java is installed (download from http://www.oracle.com/technetwork/java/javase/downloads/index.htm)
 - Download and KickAssembler from http://theweb.dk/KickAssembler/, extract to folder c:\C64\Tools\KickAssembler\ (\*)  
   Folder c:\C64\Tools\KickAssembler\ should now contain KickAss.jar and some other files/folders.
 - Download Vice C64 emulator from http://www.viceteam.org/#download, extract to folder c:\C64\Tools\Vice\ (\*\*)  
   Folder c:\C64\Tools\Vice\ should now contain x64.exe and some other files/folders.
 - Clone or download this GitHub repository to subfolder of %USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\  

\* If you did not use the recommended path for Kick Assembler in step 2, add the path to KickAss.jar to the CLASSPATH environment variable  
\*\* If you did not use the recommended path for Vice in step 3, add the path to the Vice folder containing x64.exe to the PATH environment variable

Develop, build and run
----------------------
 1. Open a Kick Assembler code file in Sublime text. Example code file [here](https://dl.dropbox.com/s/cl7391x5hqwk8zf/GoatPowerExample.asm?dl=1).
 2. Hit the `F7` key to start Build and Run (see below for more build options)
 3. Hopefully watch your lovely code execute! (\*)

\* IF you get error saying java is not recognized as an internal or external command, ensure java is installed and add the path to your java binaries folder to the PATH environment variable

Details, Build System
---------------------
Build (`Command+Shift+P` on OSX, `Control+Shift+P` on Windows) compiles the current file.
Other build variants, accessed by pressing `Super+Shift+P` (OSX) / `Ctrl+Shift+P` (Windows), or by using the associated key (after each variant below):

 - Build and Run (`F7`), compiles the current file and runs it using the Vice emulator
 - Build and Debug (`Shift+F7`), compiles the current file and runs it using the Vice emulator. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging
 - Build Startup (`Command+Shift+B`/`Ctrl+Shift+B`), compiles a file with name Startup.asm in the same folder as the current file. Handy if you have several code files included in a main runnable file.
 - Build and Run Startup (`F5`), compiles a file with name Startup.asm in the same folder as the current file, and runs it using the Vice emulator. Handy if you have several code files included in a main runnable file.
 - Build and Debug Startup (`Shift+F5`), compiles a file with name Startup.asm in the same folder as the current file, and runs it using the Vice emulator. Handy if you have several code files included in a main runnable file. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging.

Details, language and syntax
----------------------------
The syntax coloring and language configuration is under improvement and will hopefully be updated. 
The language bundle is downloaded and modified from https://github.com/cbmeeks/cbmeeks-6502kickass-asm-tmbundle. Thanks!

More info
---------
See http://goatpower.org/



//Swoffa of Noice
