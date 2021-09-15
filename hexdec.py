'''
Hexdec Debugging.
Copyright (C) 2021 by Fedor Egorov <fedoregorov1@yandex.ru>
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

from tkinter import *;
from tkinter import ttk;
from tkinter.filedialog import *; # Call open file window
from pyperclip import copy; # Copy text (HEX, DEC)

def geometry(window_width, window_height):
    global window;
    screen_width = window.winfo_screenwidth();
    screen_height = window.winfo_screenheight();

    x_cordinate = int((screen_width / 2) - (window_width / 2));
    y_cordinate = int((screen_height / 2) - (window_height / 2));

    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate));
    window.resizable(width=False, height=False);

def _onKeyRelease(event): # Author: sergey.s1, Stack Overflow.
    ctrl  = (event.state & 0x4) != 0;
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>");

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>");
    
    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>");

    if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
        text_output.tag_add(SEL, "1.0", "end-1c"); # Author: Dave Brunker, Stack Overflow.
        text_output.mark_set(INSERT, "1.0");
        text_output.see(INSERT);

def select_all():
    text_output.tag_add(SEL, "1.0", "end-1c"); # Author: Dave Brunker, Stack Overflow.
    text_output.mark_set(INSERT, "1.0");
    text_output.see(INSERT);
    return 'break';

def save():
    global Hex;
    f = asksaveasfilename(defaultextension = '.txt');
    f = open(f, 'w+', encoding = 'utf-8');
    f.write(Hex);
    f.close();

def get_values():
    global Hex, dec, original;

    Hex = bytes(text_output.get('1.0', 'end-1c'), 'utf-8').hex(); # Get HEX
    dec = int(Hex, 16); # Get DEC
    original = bytes.fromhex(Hex).decode('utf-8'); # Get original for check
    values();

def get_text():
    global Hex, dec, original;
    try:
        original = bytes.fromhex(text_output.get('1.0', 'end-1c')).decode('utf-8');
        Hex = text_output.get('1.0', 'end-1c');
        dec = str(int(Hex, 16));

    except:
        Hex = hex(int(text_output.get('1.0', 'end-1c'))).split('x')[-1];
        original = bytes.fromhex(Hex).decode('utf-8');
        dec = str(int(Hex, 16));
    values();

def values():
    global window, Hex, dec, original;

    window = Tk();
    geometry(500, 300);
    window.title('Hexdec');
    window.iconbitmap('logo.ico');

    original_label = Label(window, text = 'Original text:');
    original_label.pack();

    text = Frame(window, borderwidth = 1, relief = "sunken");
    text_output1 = Text(text, height = 7, width = 50, borderwidth = 0, font = 'NotoSans-Regular.ttf');
    vscroll = Scrollbar(text, orient = VERTICAL, command = text_output1.yview);
    text_output1['yscroll'] = vscroll.set;

    text_output1.insert("1.0", original);
    text_output1.configure(state = 'disabled');
    vscroll.pack(side = "right", fill = "y");

    text_output1.pack(side = "left", fill = "both", expand = True);
    text.pack();

    copy_original = ttk.Button(window, text = 'Copy', command = lambda: copy(original));
    copy_original.place(x = 212, y = 163);

    original_label = Label(window, text = 'HEX:');
    original_label.place(x = 11, y = 200);

    text = Frame(window, borderwidth = 1, relief = "sunken");
    text_output3 = Text(text, width = 370, borderwidth = 0, wrap = NONE, font = 'NotoSans-Regular.ttf');
    text_output3.insert("1.0", Hex);
    text_output3.configure(state = 'disabled');

    text_output3.pack();
    text.place(x = 50, y = 200, width = 360, height = 25);
    text_output.bind_all("<Key>", _onKeyRelease, "+");

    copy_hex = ttk.Button(window, text = 'Copy', command = lambda: copy(Hex));
    copy_hex.place(x = 416, y = 200);

    original_label = Label(window, text = 'DEC:');
    original_label.place(x = 11, y = 230);

    text = Frame(window, borderwidth = 1, relief = "sunken");
    text_output3 = Text(text, width = 370, borderwidth = 0, wrap = NONE, font = 'NotoSans-Regular.ttf');
    text_output3.insert("1.0", dec);
    text_output3.configure(state = 'disabled');

    text_output3.pack();
    text.place(x = 50, y = 230, width = 360, height = 25);
    text_output.bind_all("<Key>", _onKeyRelease, "+");

    copy_dec = ttk.Button(window, text = 'Copy', command = lambda: copy(dec));
    copy_dec.place(x = 416, y = 230);

    save_hex = ttk.Button(window, text = 'Save in file', command = save);
    save_hex.place(x = 212, y = 265);

    window.mainloop();

Tk().withdraw();

window = Tk();
geometry(500, 275);
window.title('Hexdec');
window.iconbitmap('logo.ico');

text_label = Label(window, text = 'Input text, HEX or DEC:');
text_label.pack();

text = Frame(window, borderwidth = 1, relief = "sunken");
text_output = Text(text, height = 10, width = 50, borderwidth = 0, font = 'NotoSans-Regular.ttf');
vscroll = Scrollbar(text, orient=VERTICAL, command = text_output.yview);
text_output['yscroll'] = vscroll.set;

vscroll.pack(side = "right", fill = "y");

text_output.pack(side = "left", fill = "both", expand = True);

text.pack();
text_output.bind_all("<Control-Key-a>", lambda event: text_output.get('1.0', 'end-1c'));
text_output.bind_all("<Key>", _onKeyRelease, "+");

text_label = Label(window, text = '');
text_label.pack();

get_values_button = ttk.Button(window, text = 'Get values', command = get_values);
get_values_button.place(x = 165, y = 220);

get_text_button = ttk.Button(window, text = 'Get text', command = get_text);
get_text_button.place(x = 165 + 90, y = 220);

window.mainloop();