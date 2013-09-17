SublimeKickAssemblerC64
=======================
Sublime Package for for C64 development with Kick Assembler.  
Support for Windows and OSX.

Requirements, OSX
-----------------
 - Download KickAssembler from http://theweb.dk/KickAssembler/ and extract to folder KickAssembler in your Application folder (\*)
 - Download Vice C64 emulator from http://www.viceteam.org/#download and extract to folder VICE in your Application folder (\*)
 
\* If you did not use the recommended paths above, edit file KickAss.sublime-build in folder ~/Library/Application Support/Sublime Text 3/Packages/ with the correct paths to KickAssembler and Vice

Requirements, Windows
---------------------
 - Ensure a fairly modern version of java is installed (download from http://www.oracle.com/technetwork/java/javase/downloads/index.htm)
 - Download and KickAssembler from http://theweb.dk/KickAssembler/and extract to folder c:\C64\Tools\KickAssembler\ (\*)  
   Folder c:\C64\Tools\KickAssembler\ should now contain KickAss.jar and some other files/folders.
 - Download Vice C64 emulator from http://www.viceteam.org/#downloaand extract to folder c:\C64\Tools\Vice\ (\*\*)  
   Folder c:\C64\Tools\Vice\ should now contain x64.exe and some other files/folders.

\* If you did not use the recommended path for Kick Assembler in step 2, edit file %USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\KickAssembler (C64)\Build Systems\KickAssembler(C64).sublime-build with the correct path to KickAss.jar  
\*\* If you did not use the recommended path for Vice in step 3, add the path to the Vice folder containing x64.exe to the PATH environment variable

Details, Build System
---------------------
Build (`Command+Shift+P` on OSX, `Control+Shift+P` on Windows) compiles the current file.
Other build variants, accessed by pressing `Super+Shift+P` (OSX) / `Ctrl+Shift+P` (Windows), or by using the associated key (after each variant below):

 - Build and Run (`F7`), compiles the current file and runs it using the Vice emulator
 - Build and Debug (`Shift+F7`), compiles the current file and runs it using the Vice emulator. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging
 - Build and Run Startup (`F5`), compiles a file with name Startup.asm in the same folder as the current file. Handy if you have several code files included in a main runnable file.
 - Build and Debug Startup (`Shift+F5`), compiles a file with name Startup.asm in the same folder as the current file. Handy if you have several code files included in a main runnable file. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging.

Details, language and syntax
----------------------------
The language bundle is downloaded and modified from https://github.com/cbmeeks/cbmeeks-6502kickass-asm-tmbundle. Thanks!
It is under improvement and will hopefully be updated.

More info
---------
See http://goatpower.org/



//Swoffa of Noice
