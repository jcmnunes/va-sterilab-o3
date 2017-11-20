import tkinter as tk
import os
from helpers.colors import *
import pickle
import graphics

class ChangePass:
    def __init__(self, constructor, master, width=848, height=400):

        self.constructor = constructor
        self.radius = 20

        # keyboard keys coordinates
        self.keyboar_dict = {'Q': [0, 0],
                             'W': [52, 0],
                             'E': [104, 0],
                             'R': [156, 0],
                             'T': [208, 0],
                             'Y': [260, 0],
                             'U': [312, 0],
                             'I': [364, 0],
                             'O': [416, 0],
                             'P': [468, 0],
                             'A': [10, 52],
                             'S': [62, 52],
                             'D': [114, 52],
                             'F': [166, 52],
                             'G': [218, 52],
                             'H': [270, 52],
                             'J': [322, 52],
                             'K': [374, 52],
                             'L': [426, 52],
                             'Z': [22, 104],
                             'X': [74, 104],
                             'C': [126, 104],
                             'V': [178, 104],
                             'B': [230, 104],
                             'N': [282, 104],
                             'M': [334, 104]}


        # Attributes
        self.master = master
        self.width = width
        self.height = height
        self.imadir = 'imachangepass'
        self.focus = 0


        # File IO
        with open('db', 'rb') as f:
            self.db = pickle.load(f)

        # Password attrs
        self.old_pass_value = self.db['pw']
        self.old_pass = ''
        self.new_pass = ''
        self.confirm_pass = ''

        # tk variables
        self.evar_old_pass = tk.StringVar()
        self.evar_new_pass = tk.StringVar()
        self.evar_confirm_pass = tk.StringVar()

        #Image files
        self.graph = graphics.ImaChangepass()

        # PhotoImage instances
        self.ima_bg = tk.PhotoImage(master=self.master, data=self.graph.bg)
        self.ima_cancel = tk.PhotoImage(master=self.master, data=self.graph.cancel)
        self.ima_cancel_push = tk.PhotoImage(master=self.master, data=self.graph.cancel_push)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_cancel = tk.Label(self.master, image=self.ima_cancel, bd=0)

        # Canvas
        self.c_keyboard = tk.Canvas(self.master, width=523, height=149, bg=BG_COLOR, borderwidth=0, highlightthickness=0)
        self.c_textbox = tk.Canvas(self.master, width=250, height=97, bg='white', borderwidth=0, highlightthickness=0)
        self.c_textbox.create_text(125, 48.5, font=('Roboto', 12), text='Change password', fill=FG_COLOR, tags='textbox')

        # Border
        # self.old_frm = tk.Frame(self.master, width=480, height=40, bg='red')

        # Entries
        self.ent_old_pass = tk.Entry(self.master, textvariable=self.evar_old_pass, font=("arial", 23,), bd=0, fg=FG_COLOR, highlightthickness=0) # width=29,
        self.ent_old_pass.focus_set()
        self.ent_new_pass = tk.Entry(self.master, textvariable=self.evar_new_pass, font=("arial", 23,), bd=0, fg=FG_COLOR, highlightthickness=0)
        self.ent_confirm_pass = tk.Entry(self.master, textvariable=self.evar_confirm_pass, font=("arial", 23,), bd=0, fg=FG_COLOR, highlightthickness=0)

        # Place
        self.lbl_bg.place(x=0, y=0)
        self.lbl_cancel.place(x=299, y=430)
        self.c_keyboard.place(x=290, y=250)
        self.c_textbox.place(x=30, y=302)

        # self.old_frm.place(x=320, y=70)
        self.ent_old_pass.place(x=320, y=70, width=490)
        self.ent_new_pass.place(x=320, y=130, width=490)
        self.ent_confirm_pass.place(x=320, y=190, width=490)
        self.place_keys()

    def inits(self):
        self.binds()

    # Bindings
    def binds(self):
        self.lbl_cancel.bind('<Button-1>', self.cancel_call)
        self.c_keyboard.bind('<Button-1>', self.canvas_callback)
        self.ent_old_pass.bind('<FocusIn>', self.old_pass_call)
        self.ent_new_pass.bind('<FocusIn>', self.new_pass_call)
        self.ent_confirm_pass.bind('<FocusIn>', self.confirm_pass_call)

    def unbinds(self):
        self.lbl_cancel.unbind('<Button-1>')
        self.c_keyboard.unbind('<Button-1>')
        self.ent_old_pass.unbind('<FocusIn>')
        self.ent_new_pass.unbind('<FocusIn>')
        self.ent_confirm_pass.unbind('<FocusIn>')

    def old_pass_call(self, event):
        self.focus = 0
    def new_pass_call(self, event):
        self.focus = 1
    def confirm_pass_call(self, event):
        self.focus = 2

    def place_keys(self, width=45, height=45):
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
        xpos = 478
        ypos = 52
        x1pos = xpos + width
        y1pos = ypos + height
        textxpos = xpos + width / 2
        textypos = ypos + height / 2
        self.create_rounded_rec(xpos, ypos, self.radius, width, height, 'BACK', fillcolor=FG_COLOR)
        # self.c_keyboard.create_rectangle(xpos, ypos, x1pos, y1pos, fill=FG_COLOR, outline=FG_COLOR, tags=('BACK', ))
        self.c_keyboard.create_polygon(517, 71, 501, 71, 501, 64, 485, 74, 501, 84, 501, 78, 517, 78, fill='white', outline='white')
        # Enter
        xpos = 389.5
        ypos = 105
        width = 97.5
        x1pos = xpos + width
        y1pos = ypos + height
        textxpos = xpos + width / 2
        textypos = ypos + height / 2
        self.create_rounded_rec(xpos, ypos, self.radius, width, height, 'ENTER', fillcolor=LIGHT_BLUE_COLOR)
        # self.c_keyboard.create_rectangle(xpos, ypos, x1pos, y1pos, fill=LIGHT_BLUE_COLOR, outline=LIGHT_BLUE_COLOR, tags=('ENTER', ))
        self.c_keyboard.create_text(textxpos, textypos, font=('Roboto', 18), text='ENTER', fill='white')

    def canvas_callback(self, event, width=45, height=45):
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
        elif event.x > 482.5 and event.x < 482.5 + width and event.y > 52 and event.y < 52 + height:
            self.c_keyboard.itemconfigure('BACK', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('BACK'))
            self.back_call()
        elif event.x > 389.5 and event.x < 389.5 + 97.5 and event.y > 105 and event.y < 105 + height:
            self.c_keyboard.itemconfigure('ENTER', fill=DARK_BLUE_COLOR, outline=DARK_BLUE_COLOR)
            self.master.after(200, lambda: self.anim_keys('ENTER'))
            self.enter_call()

    def anim_keys(self, tag):
        if tag == 'ENTER':
            self.c_keyboard.itemconfigure(tag, fill=LIGHT_BLUE_COLOR, outline=LIGHT_BLUE_COLOR)
        elif tag == 'BACK':
            self.c_keyboard.itemconfigure(tag, fill=FG_COLOR, outline=FG_COLOR)
        else:
            self.c_keyboard.itemconfigure(tag, fill='white', outline='white')

    def digest_key(self, tag):
        if self.focus == 0:
            if len(self.old_pass) < 14:
                self.ent_old_pass.insert(tk.END, "\u25CF")
                self.old_pass += tag
        elif self.focus == 1:
            if len(self.old_pass) < 14:
                self.ent_new_pass.insert(tk.END, "\u25CF")
                self.new_pass += tag
        else:
            if len(self.old_pass) < 14:
                self.ent_confirm_pass.insert(tk.END, "\u25CF")
                self.confirm_pass += tag
        self.reset_ent_bg()

    def back_call(self):
        if self.focus == 0:
            len_ent = len(self.ent_old_pass.get())
            self.ent_old_pass.delete(len_ent-1, tk.END)
            if len(self.old_pass) != 0:
                self.old_pass = self.old_pass[:-1]
        elif self.focus == 1:
            len_ent = len(self.ent_new_pass.get())
            self.ent_new_pass.delete(len_ent-1, tk.END)
            if len(self.new_pass) != 0:
                self.new_pass = self.new_pass[:-1]
        else:
            len_ent = len(self.ent_confirm_pass.get())
            self.ent_confirm_pass.delete(len_ent-1, tk.END)
            if len(self.confirm_pass) != 0:
                self.confirm_pass = self.confirm_pass[:-1]
        self.reset_ent_bg()

    def reset_ent_bg(self):
        self.ent_old_pass['bg'] = 'white'
        self.ent_new_pass['bg'] = 'white'
        self.ent_confirm_pass['bg'] = 'white'
        self.c_textbox.itemconfigure('textbox', text='Change password', fill=FG_COLOR)
    
    def enter_call(self):
        if self.old_pass == self.old_pass_value:
            if len(self.new_pass) == 0 and len(self.confirm_pass) == 0:
                self.c_textbox.itemconfigure('textbox', text='Please specify a new password', fill=RED_COLOR)
                self.ent_new_pass['bg'] = LIGHT_RED_COLOR
                self.ent_confirm_pass['bg'] = LIGHT_RED_COLOR
            else:
                if len(self.confirm_pass) == 0:
                    self.c_textbox.itemconfigure('textbox', text='Please confirm the new password', fill=RED_COLOR)
                    self.ent_confirm_pass['bg'] = LIGHT_RED_COLOR
                elif self.new_pass == self.confirm_pass:
                    if self.new_pass == self.old_pass:
                        self.c_textbox.itemconfigure('textbox', text='Please specify a new password', fill=RED_COLOR)
                        self.ent_new_pass['bg'] = LIGHT_RED_COLOR
                        self.ent_confirm_pass['bg'] = LIGHT_RED_COLOR
                    else:
                        self.c_textbox.itemconfigure('textbox', text='Password changed', fill=GREEN_COLOR)
                        self.unbinds()
                        # self.data_lines[0] = self.new_pass + '\n'
                        self.db['pw'] = self.new_pass
                        # File IO
                        with open('db', 'wb') as f:
                            pickle.dump(self.db, f)
                        self.master.after(1500, self.close_form)
                elif self.new_pass != self.confirm_pass:
                    self.c_textbox.itemconfigure('textbox', text='Passwords do not match', fill=RED_COLOR)
                    self.ent_new_pass['bg'] = LIGHT_RED_COLOR
                    self.ent_confirm_pass['bg'] = LIGHT_RED_COLOR
                elif self.new_pass == self.old_pass:
                    self.c_textbox.itemconfigure('textbox', text='Please specify a new password', fill=RED_COLOR)
                    self.ent_new_pass['bg'] = LIGHT_RED_COLOR
                    self.ent_confirm_pass['bg'] = LIGHT_RED_COLOR
        elif self.old_pass == self.db['recovery_pw'][0]:
            if self.db['recovery_pw'][3] == 0:
                self.db['recovery_pw'][3] = 1
                # File IO
                with open('db', 'wb') as f:
                    pickle.dump(self.db, f)
                self.old_pass_value = self.db['recovery_pw'][0]
                self.enter_call()
            else:
                self.c_textbox.itemconfigure('textbox', text='Wrong password', fill=RED_COLOR)
                self.ent_old_pass['bg'] = LIGHT_RED_COLOR
        elif self.old_pass == self.db['recovery_pw'][1]:
            if self.db['recovery_pw'][4] == 0:
                self.db['recovery_pw'][4] = 1
                # File IO
                with open('db', 'wb') as f:
                    pickle.dump(self.db, f)
                self.old_pass_value = self.db['recovery_pw'][1]
                self.enter_call()
            else:
                self.c_textbox.itemconfigure('textbox', text='Wrong password', fill=RED_COLOR)
                self.ent_old_pass['bg'] = LIGHT_RED_COLOR
        elif self.old_pass == self.db['recovery_pw'][2]:
            if self.db['recovery_pw'][5] == 0:
                self.db['recovery_pw'][5] = 1
                # File IO
                with open('db', 'wb') as f:
                    pickle.dump(self.db, f)
                self.old_pass_value = self.db['recovery_pw'][2]
                self.enter_call()
            else:
                self.c_textbox.itemconfigure('textbox', text='Wrong password', fill=RED_COLOR)
                self.ent_old_pass['bg'] = LIGHT_RED_COLOR

        else:
            self.c_textbox.itemconfigure('textbox', text='Wrong password', fill=RED_COLOR)
            self.ent_old_pass['bg'] = LIGHT_RED_COLOR

    def close_form(self):
        if self.constructor.global_focus != 'changepass':
            return
        flag = 'home'
        self.constructor.show_frame(0, self.constructor.homepanel, self.master, flag, self.constructor.homeapp)
        self.master.after(1200, self.clean_up)

    def cancel_call(self, event):
        flag = 'settings'
        self.constructor.anim_btn(0, self.constructor.settingspanel, self.master, self.lbl_cancel, self.ima_cancel, self.ima_cancel_push, flag, self.constructor.settingsapp)
        self.master.after(1200, self.clean_up)

    def clean_up(self):
        # TODO: Clean-up the fields
        self.focus = 0
        # File IO
        with open('db', 'rb') as f:
            self.db = pickle.load(f)
        self.old_pass_value = self.db['pw']
        self.old_pass = ''
        self.new_pass = ''
        self.confirm_pass = ''
        self.ent_old_pass.delete(0, tk.END)
        self.ent_new_pass.delete(0, tk.END)
        self.ent_confirm_pass.delete(0, tk.END)
        self.ent_old_pass.focus_set()
        self.reset_ent_bg()
        self.binds()

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

if __name__ == '__main__':
    root = tk.Tk()
    FONT_NORMAL = font.Font(family='Roboto', size=10)
    FONT_INFO = font.Font(family='Roboto', size=12)
    FONT_INFO_KW = font.Font(family='Roboto', size=12, weight=font.BOLD)
    FONT_KB = font.Font(family='Roboto', size=18, weight=font.NORMAL)
    app = ChangePass(root, root)
    root.mainloop()