To compile the python extension put your 'highscore_api.h' header file in this
folder and type the following command in the terminal:

python setup.py build_ext -b .

If the compilation succeeds a new file will be created: 'pyHighscore.so'.
This extension presents four functions that call your new system calls:
1) highscore_add
2) highscore_list
2) highscore_chleague
3) highscore_leagues

You can use this functions in a python script or directly from the python
interpreter, type 'python' in the terminal and then the following commands:

>>>import pyHighscore
>>>import os
>>>pyHighscore.highscore_add('/some/board', 123)
>>>top10 = pyHighscore.highscore_list('/some/board', 10)

The syntax of the command can be found by typing the following in the python
interpreter:

>>>import pyHighscore
>>>print pyHighscore.highscore_add.__doc__

You can also use the ipython interpreter (you can find the rpm package in the
course website). After running ipython (type 'ipython' in the terminal) do:

[1] import pyHighscore
[2] pyHighscore.highscore_add?
