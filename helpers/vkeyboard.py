import tkinter as tk
import os
from helpers.colors import *
import pickle
import graphics

graph = graphics.ImaKb()


class VKeyboard:
    def __init__(self, constructor, master, width=848, height=400):

        self.constructor = constructor

        self.radius = 20

        # keyboard keys coordinates
        self.keyboar_dict = {'Q': [0, 0],
                             'W': [70, 0],
                             'E': [140, 0],
                             'R': [210, 0],
                             'T': [280, 0],
                             'Y': [350, 0],
                             'U': [420, 0],
                             'I': [490, 0],
                             'O': [560, 0],
                             'P': [630, 0],
                             'A': [14, 70],
                             'S': [84, 70],
                             'D': [154, 70],
                             'F': [224, 70],
                             'G': [294, 70],
                             'H': [364, 70],
                             'J': [434, 70],
                             'K': [504, 70],
                             'L': [574, 70],
                             'Z': [30, 140],
                             'X': [100, 140],
                             'C': [170, 140],
                             'V': [240, 140],
                             'B': [310, 140],
                             'N': [380, 140],
                             'M': [450, 140]}

        # Attributes
        self.master = master
        self.width = width
        self.height = height
        self.focus = 0

        # File IO
        with open('db', 'rb') as f:
            self.db = pickle.load(f)

        # Password attrs
        self.pw = self.db['pw']
        self.pass_inputed = ''

        # tk variables
        self.evar = tk.StringVar()

        # PhotoImage instances
        self.ima_bg = tk.PhotoImage(master=self.master, data=graph.bg)
        self.ima_cancel = tk.PhotoImage(master=self.master, data=graph.cancel)
        self.ima_cancel_push = tk.PhotoImage(master=self.master, data=graph.cancel_push)
        self.ima_insertpw = tk.PhotoImage(master=self.master, data=graph.insertpw)
        self.ima_successpw = tk.PhotoImage(master=self.master, data=graph.successpw)
        self.ima_wrongpw = tk.PhotoImage(master=self.master, data=graph.wrongpw)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_cancel = tk.Label(self.master, image=self.ima_cancel, bd=0)
        self.lbl_pwinfo = tk.Label(self.master, image=self.ima_insertpw, bd=0)

        # Canvas
        self.c_keyboard = tk.Canvas(self.master, width=704, height=200, bg=BG_COLOR, borderwidth=0, highlightthickness=0)

        # Entries
        self.ent = tk.Entry(self.master, textvariable=self.evar, width=26, font=("arial", 35,), bd=0, fg=FG_COLOR, highlightthickness=0)

        # Place
        self.lbl_bg.place(x=0, y=0)
        self.lbl_cancel.place(x=299, y=430)
        self.lbl_pwinfo.place(x=0, y=0)
        self.c_keyboard.place(x=72, y=182)
        self.ent.place(x=80, y=70)

        self.place_keys()

    def inits(self):
        print('coise')

    # Bindings
    def binds(self):
        self.lbl_cancel.bind('<Button-1>', self.cancel_call)
        self.c_keyboard.bind('<Button-1>', self.canvas_callback)

    def unbinds(self):
        self.lbl_cancel.unbind('<Button-1>')
        self.c_keyboard.unbind('<Button-1>')

    def place_keys(self, width=60, height=60):
        for k, v in self.keyboar_dict.items():
            xpos = v[0]
            ypos = v[1]
            x1pos = xpos + width
            y1pos = ypos + height
            textxpos = xpos + width / 2
            textypos = ypos + height / 2
            self.create_rounded_rec(xpos, ypos, self.radius, width, height, k)
            # self.c_keyboard.create_rectangle(xpos, ypos, x1pos, y1pos, fill='white', outline='white', tags=k)
            self.c_keyboard.create_text(textxpos, textypos, font=('Roboto', 18), text=k, fill=FG_COLOR)
        # Back
        xpos = 644
        ypos = 70
        x1pos = xpos + width
        y1pos = ypos + height
        textxpos = xpos + width / 2
        textypos = ypos + height / 2
        # self.c_keyboard.create_rectangle(xpos, ypos, x1pos, y1pos, fill=FG_COLOR, outline=FG_COLOR, tags=('BACK', ))
        self.create_rounded_rec(xpos, ypos, self.radius, width, height, 'BACK', fillcolor=FG_COLOR)
        self.c_keyboard.create_polygon(694, 102, 694, 98, 670, 98, 670, 91, 653, 100, 670, 109, 670, 102, fill='white', outline='white') # Draw arrow
        # Enter
        xpos = 520
        ypos = 140
        width = 130
        x1pos = xpos + width
        y1pos = ypos + height
        textxpos = xpos + width / 2
        textypos = ypos + height / 2
        # self.c_keyboard.create_rectangle(xpos, ypos, x1pos, y1pos, fill=LIGHT_BLUE_COLOR, outline=LIGHT_BLUE_COLOR, tags=('ENTER', ))
        self.create_rounded_rec(xpos, ypos, self.radius, width, height, 'ENTER', fillcolor=LIGHT_BLUE_COLOR)
        self.c_keyboard.create_text(textxpos, textypos, font=('Roboto', 18), text='ENTER', fill='white')

    def canvas_callback(self, event, width=60, height=60):
        if self.constructor.global_focus != 'kb':
            return
        if event.x > self.keyboar_dict['Q'][0] and event.x < self.keyboar_dict['Q'][0] + width and event.y > self.keyboar_dict['Q'][1] and event.y < self.keyboar_dict['Q'][1] + height:
            self.c_keyboard.itemconfigure('Q', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('Q'))
            self.digest_key('q')
        elif event.x > self.keyboar_dict['W'][0] and event.x < self.keyboar_dict['W'][0] + width and event.y > self.keyboar_dict['W'][1] and event.y < self.keyboar_dict['W'][1] + height:
            self.c_keyboard.itemconfigure('W', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('W'))
            self.digest_key('w')
        elif event.x > self.keyboar_dict['E'][0] and event.x < self.keyboar_dict['E'][0] + width and event.y > self.keyboar_dict['E'][1] and event.y < self.keyboar_dict['E'][1] + height:
            self.c_keyboard.itemconfigure('E', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('E'))
            self.digest_key('e')
        elif event.x > self.keyboar_dict['R'][0] and event.x < self.keyboar_dict['R'][0] + width and event.y > self.keyboar_dict['R'][1] and event.y < self.keyboar_dict['R'][1] + height:
            self.c_keyboard.itemconfigure('R', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('R'))
            self.digest_key('r')
        elif event.x > self.keyboar_dict['T'][0] and event.x < self.keyboar_dict['T'][0] + width and event.y > self.keyboar_dict['T'][1] and event.y < self.keyboar_dict['T'][1] + height:
            self.c_keyboard.itemconfigure('T', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('T'))
            self.digest_key('t')
        elif event.x > self.keyboar_dict['Y'][0] and event.x < self.keyboar_dict['Y'][0] + width and event.y > self.keyboar_dict['Y'][1] and event.y < self.keyboar_dict['Y'][1] + height:
            self.c_keyboard.itemconfigure('Y', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('Y'))
            self.digest_key('y')
        elif event.x > self.keyboar_dict['U'][0] and event.x < self.keyboar_dict['U'][0] + width and event.y > self.keyboar_dict['U'][1] and event.y < self.keyboar_dict['U'][1] + height:
            self.c_keyboard.itemconfigure('U', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('U'))
            self.digest_key('u')
        elif event.x > self.keyboar_dict['I'][0] and event.x < self.keyboar_dict['I'][0] + width and event.y > self.keyboar_dict['I'][1] and event.y < self.keyboar_dict['I'][1] + height:
            self.c_keyboard.itemconfigure('I', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('I'))
            self.digest_key('i')
        elif event.x > self.keyboar_dict['O'][0] and event.x < self.keyboar_dict['O'][0] + width and event.y > self.keyboar_dict['O'][1] and event.y < self.keyboar_dict['O'][1] + height:
            self.c_keyboard.itemconfigure('O', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('O'))
            self.digest_key('o')
        elif event.x > self.keyboar_dict['P'][0] and event.x < self.keyboar_dict['P'][0] + width and event.y > self.keyboar_dict['P'][1] and event.y < self.keyboar_dict['P'][1] + height:
            self.c_keyboard.itemconfigure('P', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('P'))
            self.digest_key('p')
        elif event.x > self.keyboar_dict['A'][0] and event.x < self.keyboar_dict['A'][0] + width and event.y > self.keyboar_dict['A'][1] and event.y < self.keyboar_dict['A'][1] + height:
            self.c_keyboard.itemconfigure('A', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('A'))
            self.digest_key('a')
        elif event.x > self.keyboar_dict['S'][0] and event.x < self.keyboar_dict['S'][0] + width and event.y > self.keyboar_dict['S'][1] and event.y < self.keyboar_dict['S'][1] + height:
            self.c_keyboard.itemconfigure('S', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('S'))
            self.digest_key('s')
        elif event.x > self.keyboar_dict['D'][0] and event.x < self.keyboar_dict['D'][0] + width and event.y > self.keyboar_dict['D'][1] and event.y < self.keyboar_dict['D'][1] + height:
            self.c_keyboard.itemconfigure('D', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('D'))
            self.digest_key('d')
        elif event.x > self.keyboar_dict['F'][0] and event.x < self.keyboar_dict['F'][0] + width and event.y > self.keyboar_dict['F'][1] and event.y < self.keyboar_dict['F'][1] + height:
            self.c_keyboard.itemconfigure('F', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('F'))
            self.digest_key('f')
        elif event.x > self.keyboar_dict['G'][0] and event.x < self.keyboar_dict['G'][0] + width and event.y > self.keyboar_dict['G'][1] and event.y < self.keyboar_dict['G'][1] + height:
            self.c_keyboard.itemconfigure('G', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('G'))
            self.digest_key('g')
        elif event.x > self.keyboar_dict['H'][0] and event.x < self.keyboar_dict['H'][0] + width and event.y > self.keyboar_dict['H'][1] and event.y < self.keyboar_dict['H'][1] + height:
            self.c_keyboard.itemconfigure('H', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('H'))
            self.digest_key('h')
        elif event.x > self.keyboar_dict['J'][0] and event.x < self.keyboar_dict['J'][0] + width and event.y > self.keyboar_dict['J'][1] and event.y < self.keyboar_dict['J'][1] + height:
            self.c_keyboard.itemconfigure('J', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('J'))
            self.digest_key('j')
        elif event.x > self.keyboar_dict['K'][0] and event.x < self.keyboar_dict['K'][0] + width and event.y > self.keyboar_dict['K'][1] and event.y < self.keyboar_dict['K'][1] + height:
            self.c_keyboard.itemconfigure('K', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('K'))
            self.digest_key('k')
        elif event.x > self.keyboar_dict['L'][0] and event.x < self.keyboar_dict['L'][0] + width and event.y > self.keyboar_dict['L'][1] and event.y < self.keyboar_dict['L'][1] + height:
            self.c_keyboard.itemconfigure('L', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('L'))
            self.digest_key('l')
        elif event.x > self.keyboar_dict['Z'][0] and event.x < self.keyboar_dict['Z'][0] + width and event.y > self.keyboar_dict['Z'][1] and event.y < self.keyboar_dict['Z'][1] + height:
            self.c_keyboard.itemconfigure('Z', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('Z'))
            self.digest_key('z')
        elif event.x > self.keyboar_dict['X'][0] and event.x < self.keyboar_dict['X'][0] + width and event.y > self.keyboar_dict['X'][1] and event.y < self.keyboar_dict['X'][1] + height:
            self.c_keyboard.itemconfigure('X', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('X'))
            self.digest_key('x')
        elif event.x > self.keyboar_dict['C'][0] and event.x < self.keyboar_dict['C'][0] + width and event.y > self.keyboar_dict['C'][1] and event.y < self.keyboar_dict['C'][1] + height:
            self.c_keyboard.itemconfigure('C', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('C'))
            self.digest_key('c')
        elif event.x > self.keyboar_dict['V'][0] and event.x < self.keyboar_dict['V'][0] + width and event.y > self.keyboar_dict['V'][1] and event.y < self.keyboar_dict['V'][1] + height:
            self.c_keyboard.itemconfigure('V', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('V'))
            self.digest_key('v')
        elif event.x > self.keyboar_dict['B'][0] and event.x < self.keyboar_dict['B'][0] + width and event.y > self.keyboar_dict['B'][1] and event.y < self.keyboar_dict['B'][1] + height:
            self.c_keyboard.itemconfigure('B', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('B'))
            self.digest_key('b')
        elif event.x > self.keyboar_dict['N'][0] and event.x < self.keyboar_dict['N'][0] + width and event.y > self.keyboar_dict['N'][1] and event.y < self.keyboar_dict['N'][1] + height:
            self.c_keyboard.itemconfigure('N', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('N'))
            self.digest_key('n')
        elif event.x > self.keyboar_dict['M'][0] and event.x < self.keyboar_dict['M'][0] + width and event.y > self.keyboar_dict['M'][1] and event.y < self.keyboar_dict['M'][1] + height:
            self.c_keyboard.itemconfigure('M', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('M'))
            self.digest_key('m')
        elif event.x > 644 and event.x < 704 + width and event.y > 70 and event.y < 130:
            self.c_keyboard.itemconfigure('BACK', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('BACK'))
            self.back_call()
        elif event.x > 517 and event.x < 647 and event.y > 140 and event.y < 200:
            self.c_keyboard.itemconfigure('ENTER', fill=DARK_BLUE_COLOR, outline=DARK_BLUE_COLOR)
            self.master.after(200, lambda: self.anim_keys('ENTER'))
            self.enter_call()

    def anim_keys(self, tag):
        if self.constructor.global_focus != 'kb':
            return
        if tag == 'ENTER':
            self.c_keyboard.itemconfigure(tag, fill=LIGHT_BLUE_COLOR, outline=LIGHT_BLUE_COLOR)
        elif tag == 'BACK':
            self.c_keyboard.itemconfigure(tag, fill=FG_COLOR, outline=FG_COLOR)
        else:
            self.c_keyboard.itemconfigure(tag, fill='white', outline='white')

    def digest_key(self, tag):
        if self.constructor.global_focus != 'kb':
            return
        if len(self.pass_inputed) < 14:
            self.ent.insert(tk.END, "\u25CF")
            self.pass_inputed += tag
        self.reset_ent_bg()

    def back_call(self):
        if self.constructor.global_focus != 'kb':
            return
        len_ent = len(self.ent.get())
        self.ent.delete(len_ent-1, tk.END)
        if len(self.pass_inputed) != 0:
            self.pass_inputed = self.pass_inputed[:-1]
        self.reset_ent_bg()

    def reset_ent_bg(self):
        self.ent['bg'] = 'white'
        self.lbl_pwinfo['image'] = self.ima_insertpw
    
    def enter_call(self):
        if self.constructor.global_focus != 'kb':
            return
        with open('db', 'rb') as f:
            self.db = pickle.load(f)
        self.pw = self.db['pw']
        if self.pass_inputed == self.pw:
            self.unbinds()
            self.lbl_pwinfo['image'] = self.ima_successpw
            self.master.after(1000, self.show_man)
        else:
            self.lbl_pwinfo['image'] = self.ima_wrongpw

    def show_man(self):
        if self.constructor.global_focus != 'kb':
            return
        flag = 'man'
        self.constructor.show_frame(0, self.constructor.manpanel, self.master, flag, self.constructor.manapp)
        self.master.after(1200, self.clean_up)

    def cancel_call(self, event):
        self.master.after(1200, self.clean_up)
        if self.constructor.global_focus != 'kb':
            return
        flag = 'home'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.homepanel, self.master, self.lbl_cancel, self.ima_cancel, self.ima_cancel_push, flag, self.constructor.homeapp)

    def clean_up(self):
        self.pass_inputed = ''
        self.ent.delete(0, tk.END)
        self.reset_ent_bg()

    def create_rounded_rec(self, x, y, r, w, h, tag, fillcolor='white'):
        self.c_keyboard.create_polygon(x+r, y,
                                       x+r, y,
                                       x+w-r, y,
                                       x+w-r, y,
                                       x+w, y,
                                       x+w, y+r,
                                       x+w, y+r,
                                       x+w, y+h-r,
                                       x+w, y+h-r,
                                       x+w, y+h,
                                       x+w-r, y+h,
                                       x+w-r, y+h,
                                       x+r, y+h,
                                       x+r, y+h,
                                       x, y+h,
                                       x, y+h-r,
                                       x, y+h-r,
                                       x, y+r,
                                       x, y+r,
                                       x, y,
                                       smooth=1,
                                       fill=fillcolor,
                                       tags=tag)