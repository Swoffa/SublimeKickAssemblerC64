SublimeKickAssemblerC64
=======================
Sublime Package for for C64 development with Kick Assembler. Support for Windows and OSX.

Requirements, OSX
-----------------
 - Download KickAssembler compiler from http://theweb.dk/KickAssembler/, extract and copy/install into folder KickAssembler in your Application folder (\*)
 - Download Vice C64 emulator from http://www.viceteam.org/#download, extract and copy/install into folder VICE in your Application folder (\*)
 
\* If you did not use the recommended paths above, edit file KickAss.sublime-build in folder ~/Library/Application Support/Sublime Text 3/Packages/ with the correct paths to KickAssembler and Vice

Requirements, Windows
---------------------
 - Ensure a fairly modern version of java is installed (download from http://www.oracle.com/technetwork/java/javase/downloads/index.htm)
 - Ensure path to java-binaries (probably %programfiles(x86)%\Java\jre7\bin) exists in the PATH environment variable on your computer
 - Download and KickAssembler compiler from http://theweb.dk/KickAssembler/, extract and copy folder to c:\C64\Tools\KickAssembler\ (or other location and ensure path to KickAss.jar is correct in %USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\KickAssembler (C64)\Build Systems\KickAssembler(C64).sublime-build)
 - Download Vice C64 emulator from http://www.viceteam.org/#download, extract and copy folder to some good location on your computer (c:\C64\Tools\Vice\ is recommended)
 - Ensure the path to Vice executable x64.exe exists in the PATH environment variable on your computer

Details, Build System
---------------------
Build (Super+b/Ctrl+b) compiles the current file.
Other build variants, accessed by pressing Super+Shift+P/Ctrl+Shift+P, or by using the associated key (after each variant below):

 - Build and Run (F7), compiles the current file and runs it using the Vice emulator
 - Build and Debug (Shift+F7), compiles the current file and runs it using the Vice emulator. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging
 - Build and Run Startup (F5), compiles a file with name Startup.asm in the same folder as the current file. Handy if you have several code files included in a main runnable file.
 - Build and Debug Startup (Shift+F5), compiles a file with name Startup.asm in the same folder as the current file. Handy if you have several code files included in a main runnable file. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging.

Details, language and syntax
----------------------------
The language bundle is downloaded and modified from https://github.com/cbmeeks/cbmeeks-6502kickass-asm-tmbundle. Thanks!
It is under improvement and will hopefully be updated.

More info
---------
See http://goatpower.org/



//Swoffa of Noice
