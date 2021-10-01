'''
Hexdec.
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

try:
    from tkinter import *;
    from tkinter import ttk;
    from tkinter.filedialog import *; # Call open file window
    import sys;
    import ctypes;
    from os import path;
    from subprocess import call;
    from webbrowser import open_new;
    try:
        from pyperclip import copy, paste; # Copy text (HEX, DEC)
    except:
        path.insert(0, path.dirname(sys.executable) + "\\pyperclip");
        from pyperclip import copy, paste;
    try:
        from PIL import ImageTk, Image;
    except:
        path.insert(0, path.dirname(sys.executable) + "\\PIL");
        from PIL import ImageTk, Image;

    myappid = 'fedoregorov.hexdec.1.6' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    call('taskkill /f /im hexdec.exe', shell = True);

    def open_site(url):
        open_new(url);

    def geometry(window_width, window_height):
        global window;
        screen_width = window.winfo_screenwidth();
        screen_height = window.winfo_screenheight();

        x_cordinate = int((screen_width / 2) - (window_width / 2));
        y_cordinate = int((screen_height / 2) - (window_height / 2));

        window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate));
        window.resizable(width=False, height=False);

    def on_close():
        sys.exit();
        # subprocess.call('taskkill /f /im hexdec.exe & taskkill /f /im python.exe & taskkill /f /im pythonw.exe', shell=True);

    def _onKeyRelease(event): # Author: sergey.s1, Stack Overflow.
        ctrl  = (event.state & 0x4) != 0;
        if event.keycode == 88 and ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>");

        if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>");
        
        if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>");

        if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
            text_input.tag_add(SEL, "1.0", "end-1c"); # Author: Dave Brunker, Stack Overflow.
            text_input.mark_set(INSERT, "1.0");
            text_input.see(INSERT);

    def select_all():
        text_input.tag_add(SEL, "1.0", "end-1c"); # Author: Dave Brunker, Stack Overflow.
        text_input.mark_set(INSERT, "1.0");
        text_input.see(INSERT);
        return 'break';

    def save_hex():
        global Hex;
        f = asksaveasfilename(defaultextension = '.txt');
        f = open(f, 'w+', encoding = 'utf-8');
        f.write(Hex);
        f.close();

    def save_dec():
        global dec;
        f = asksaveasfilename(defaultextension = '.txt');
        f = open(f, 'w+', encoding = 'utf-8');
        f.write(str(dec));
        f.close();

    def get_values():
        global Hex, dec, original;

        Hex = bytes(text_input.get('1.0', 'end-1c'), 'utf-8').hex(); # Get HEX
        dec = int(Hex, 16); # Get DEC
        original = bytes.fromhex(Hex).decode('utf-8'); # Get original for check
        values();

    def get_text():
        global Hex, dec, original;
        try:
            original = bytes.fromhex(text_input.get('1.0', 'end-1c')).decode('utf-8');
            Hex = text_input.get('1.0', 'end-1c');
            dec = str(int(Hex, 16));

        except:
            Hex = hex(int(text_input.get('1.0', 'end-1c'))).split('x')[-1];
            original = bytes.fromhex(Hex).decode('utf-8');
            dec = str(int(Hex, 16));
        values();

    def values():
        global window, Hex, dec, original;

        window = Tk();
        geometry(500, 350);
        window.title('Hexdec');
        try:
            window.iconbitmap(path.dirname(sys.executable) + '\\logo.ico');
        except:
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
        # text_output.bind_all("<Key>", _onKeyRelease, "+");

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
        # text_output.bind_all("<Key>", _onKeyRelease, "+");

        copy_dec = ttk.Button(window, text = 'Copy', command = lambda: copy(dec));
        copy_dec.place(x = 416, y = 230);

        save_hex_button = ttk.Button(window, text = 'Save HEX in file', command = save_hex);
        save_hex_button.place(x = 11, y = 265);

        save_dec_button = ttk.Button(window, text = 'Save DEC in file', command = save_dec);
        save_dec_button.place(x = 11, y = 295);

        len_hex_label = Label(window, text = 'Number of characters in HEX: ' + str(len(Hex)));
        len_hex_label.place(x = 105, y = 266.5);

        len_dec_label = Label(window, text = 'Number of characters in DEC: ' + str(len(str(dec))));
        len_dec_label.place(x = 105, y = 296.5);

        window.mainloop();

    Tk().withdraw();

    window = Toplevel();
    geometry(500, 300);
    window.title('Hexdec');
    try:
        window.iconbitmap(path.dirname(sys.executable) + '\\logo.ico');
    except:
        window.iconbitmap('logo.ico');

    nb = ttk.Notebook(window);
    f1 = Frame(window);
    f2 = Frame(window);
    nb.add(f1, text='Main');
    nb.add(f2, text = 'About');
    nb.pack(fill='both', expand='yes');

    text_label = Label(f1, text = 'Input text, HEX or DEC:');
    text_label.pack();

    text = Frame(f1, borderwidth = 1, relief = "sunken");
    text_input = Text(text, height = 10, width = 50, borderwidth = 0, font = 'NotoSans-Regular.ttf');
    vscroll = Scrollbar(text, orient=VERTICAL, command = text_input.yview);
    text_input['yscroll'] = vscroll.set;

    vscroll.pack(side = "right", fill = "y");

    text_input.pack(side = "left", fill = "both", expand = True);

    text.pack();
    text_input.bind_all("<Control-Key-a>", lambda event: text_input.get('1.0', 'end-1c'));
    text_input.bind_all("<Key>", _onKeyRelease, "+");

    text_label = Label(f1, text = '');
    text_label.pack();

    get_values_button = ttk.Button(f1, text = 'Get values', command = get_values);
    get_values_button.place(x = 165, y = 220);

    get_text_button = ttk.Button(f1, text = 'Get text', command = get_text);
    get_text_button.place(x = 165 + 90, y = 220);

    window.protocol('WM_DELETE_WINDOW', on_close);

    iy = 60;

    try:
        img = Image.open(path.dirname(sys.executable) + 'logo.png');
    except:
        img = Image.open('logo.png');
    (w, h) = img.size;
    img = img.resize((w // 5, h // 5), Image.ANTIALIAS);

    img = ImageTk.PhotoImage(img);
    panel = Label(f2, image = img);
    panel.place(x = 25, y = 80 - iy + 60);

    program_name = Label(f2, text = 'Hexdec', font = 'Arial 15');
    program_name.place(x = 140, y = 80 - iy);

    version = Label(f2, text = 'Version 1.16', font = 'Arial 10');
    version.place(x = 140, y = 110 - iy);

    author = Label(f2, text = 'Author: Fedor Egorov (FatlessComb1168)', font = 'Arial 10');
    author.place(x = 140, y = 130 - iy);

    author_github = Label(f2, text = '(GitHub)', font = 'Arial 10', fg = "blue", cursor = "hand2");
    author_github.place(x = 383, y = 130 - iy);
    author_github.configure(underline = True);
    author_github.bind("<Button-1>", lambda e: open_site("https://github.com/FatlessComb1168"));

    licensed = Label(f2, text = 'The program is distributed under the GNU Public License,', font = 'Arial 10');
    licensed.place(x = 140, y = 160 - iy);

    licensed = Label(f2, text = 'version 3. You can read more about the license here:', font = 'Arial 10');
    licensed.place(x = 140, y = 180 - iy);

    licensed3 = Label(f2, text = 'https://www.gnu.org/licenses/gpl-3.0.en.html', fg = "blue", cursor = "hand2", font = 'Arial 10');
    licensed3.place(x = 140, y = 200 - iy);   
    licensed3.configure(underline = True); 
    licensed3.bind("<Button-1>", lambda e: open_site("https://www.gnu.org/licenses/gpl-3.0.en.html"));

    github = Label(f2, text = 'See project on GitHub: ', font = 'Arial 10');
    github.place(x = 140, y = 230 - iy);

    licensed3 = Label(f2, text = 'https://github.com/FatlessComb1168/hexdec', fg = "blue", cursor = "hand2", font = 'Arial 10');
    licensed3.place(x = 140, y = 250 - iy);   
    licensed3.configure(underline = True); 
    licensed3.bind("<Button-1>", lambda e: open_site("https://github.com/FatlessComb1168/hexdec"));

    window.mainloop();
except Exception as e:
    input(e);