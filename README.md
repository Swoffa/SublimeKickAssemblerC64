SublimeKickAssemblerC64
=======================
Sublime Package for for C64 development with Kick Assembler (download from http://theweb.dk/KickAssembler/). 
Support for Windows and OSX.

Requirements, Windows
=====================
 - Ensure java 1.7 is installed 
 - Ensure path to java-binaries (probably %programfiles(x86)%\Java\jre7\bin) exists in the PATH environment variable on your computer.
 - Ensure path to KickAss.jar is correct in %USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\KickAssembler (C64)/Build Systems/KickAss.bat

Requirements, OSX
=====================
 - Ensure java 1.7 is installed
 - Ensure KickAss.jar is installed in folder /Applications/KickAssembler/ (or edit KickAss.sublime-build with your path)
 - Ensure VICE is installed in folder /Applications/ (or edit KickAss.sublime-build with your path)

Details, Build System
=====================
Build (command+b/ctrl+b) compiles the current file.
Other build variants, accessed by pressing Command+Shift+P/Ctrl+Shift+P, or by using the associated key (after each variant below):
 - Build and Run (F7), compiles the current file and runs it using the Vice emulator
 - Build and Debug (Shift+F7), compiles the current file and runs it using the Vice emulator. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging
 - Build and Run Startup (F5), compiles a file with name Startup.asm in the same folder as the current file. Handy if you have several code files included in a main runnable file.
 - Build and Debug Startup (Shift+F5), compiles a file with name Startup.asm in the same folder as the current file. Handy if you have several code files included in a main runnable file. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging.

Details, language and syntax
============================
The language bundle is downloaded and modified from https://github.com/cbmeeks/cbmeeks-6502kickass-asm-tmbundle. Thanks!
It is under improvement and will hopefully be updated.

//Swoffa of Noice