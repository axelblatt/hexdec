'''
Hexdec Console.
Copyright (C) 2021 by Fedor Egorov
This file is part of Hexdec.

Hexdec is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Hexdec is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Hexdec. If not, see <https://www.gnu.org/licenses/>.
'''

from os import system; # Import os.system() to clean console
from tkinter.filedialog import *; # Call open file window
from tkinter import Tk;
from pyperclip import copy; # Copy text (HEX, DEC)

Tk().withdraw();

def hex_get(): # hex_get() function
        system('cls'); # Clear console
        print('Original: ' + str(original) + '\n'); # Print original text/file bytes
        print('HEX: ' + Hex + '\n'); # Print HEX version of text/file bytes
        print('DEC: ' + str(dec) + '\n'); # Print DEC version of text/file bytes

        # print('Array: ' + str(array) + '\n'); # EXPERIMENTAL: array version of text/file bytes.
                                                # Clear '#' from all strings where comment has 'EXPERIMENTAL' word
                                                # to get bytes array of text or files.

        print('len() of HEX: ' + str(len(Hex)) + '\n'); # Count symbols
        print('len() of DEC: ' + str(len(str(dec))) + '\n');

        # print('len() of array: ' + str(len(str(array))) + '\n'); # EXPERIMENTAL: array version of text/file bytes.
                                                                   # Remove the first '#' from all strings where comment has 'EXPERIMENTAL' word
                                                                   # to get bytes array of text or files.

        input('<Enter> to continue.\n');
    
_exit = True;
while _exit:
    try:
        print('0 - Encode text\n1 - Encode file\n2 - Decode text\n3 - Decode file\n4 - Exit'); # Menu
        a = input(); # User input

        if a == '0':
            system('cls');
            text = input('Enter any text: ');

            Hex = bytes(text, 'utf-8').hex(); # Get HEX
            dec = int(Hex, 16); # Get DEC
            original = bytes.fromhex(Hex).decode('utf-8'); # Get original for check

            # array = list(bytes(text, 'utf-8')); # EXPERIMENTAL: array version of text/file bytes.
                                                  # Remove the first '#' from all strings where comment has 'EXPERIMENTAL' word
                                                  # to get bytes array of text or files.
            
            hex_get(); # Get text with hex and dec

        if a == '1':
            system('cls');
            file = askopenfilename(); # Call open file window
            file = open(file, 'rb'); # Open file in binary read mode
            file = file.read(); 

            Hex = file.hex(); # Get HEX
            dec = int(Hex, 16); # Get DEC

            # array = list(file); # EXPERIMENTAL: array version of text/file bytes.
                                  # Remove the first '#' from all strings where comment has 'EXPERIMENTAL' word
                                  # to get bytes array of text or files.

            print('HEX: ' + Hex + '\n'); # Print HEX version of text/file bytes
            print('DEC: ' + str(dec) + '\n'); # Print DEC version of text/file bytes

            print('len() of HEX: ' + str(len(Hex)) + '\n'); # Count symbols
            print('len() of DEC: ' + str(len(str(dec))) + '\n');

            input('<Enter> to continue.\n');

        if a == '2':
            system('cls');
            text = input('Enter HEX or DEC: ');
            
            try:
                original = bytes.fromhex(text).decode('utf-8');
                Hex = text;
                dec = str(int(Hex, 16));

            except:
                Hex = hex(int(text)).split('x')[-1];
                original = bytes.fromhex(Hex).decode('utf-8');
                dec = str(int(Hex, 16));

            system('cls');
            print('Original: ' + original);
            print('\nHEX: ' + Hex);
            print('\nDEC: ' + dec);

            input('\n<Enter> to continue.\n');
        
        if a == '3':
            system('cls');
            text = input('Enter HEX or DEC: ');
            
            try:
                original = bytes.fromhex(text);
                Hex = text;

            except:
                Hex = hex(int(text)).split('x')[-1];
                original = bytes.fromhex(Hex);

            f = asksaveasfilename();
            f = open(f, 'wb');
            f.write();
            f.close();

        if a == '4':
            _exit = False;

        system('cls');
    except Exception as e: # Prevent crash
        input('ERROR: ' + str(e) + '\n<Enter> to continue');
        system('cls');