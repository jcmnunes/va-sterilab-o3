import tkinter as tk
import os
from helpers.colors import *
import pickle
import graphics

graph = graphics.ImaParams()

class Winparams:
    def __init__(self, constructor, master, width=848, height=480):

        self.constructor = constructor

        # Attributes
        self.master = master
        self.width = width
        self.height = height
        self.focus = 0
        self.radius = 20

        # keyboard keys coordinates
        self.keypad_dict = {'k1': [0, 104],
                             'k2': [52, 104],
                             'k3': [104, 104],
                             'k4': [0, 52],
                             'k5': [52, 52],
                             'k6': [104, 52],
                             'k7': [0, 0],
                             'k8': [52, 0],
                             'k9': [104, 0],
                             'k.': [104, 156]}

        # PhotoImage instances
        self.ima_bg = tk.PhotoImage(master=self.master, data=graph.bg)
        self.ima_back = tk.PhotoImage(master=self.master, data=graph.back)
        self.ima_back_push = tk.PhotoImage(master=self.master, data=graph.back_push)
        self.ima_labels = tk.PhotoImage(master=self.master, data=graph.labels)
        self.ima_on = tk.PhotoImage(master=self.master, data=graph.on)
        self.ima_off = tk.PhotoImage(master=self.master, data=graph.off)
        self.ima_tab = tk.PhotoImage(master=self.master, data=graph.tab)
        self.ima_tab_push = tk.PhotoImage(master=self.master, data=graph.tab_push)
        self.ima_back_kp = tk.PhotoImage(master=self.master, data=graph.back_kp)
        self.ima_back_kp_push = tk.PhotoImage(master=self.master, data=graph.back_kp_push)
        self.ima_enter = tk.PhotoImage(master=self.master, data=graph.enter)
        self.ima_enter_push = tk.PhotoImage(master=self.master, data=graph.enter_push)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_back = tk.Label(self.master, image=self.ima_back, bd=0)
        self.lbl_labels = tk.Label(self.master, image=self.ima_labels, bd=0)
        # Enable semi-auto mode
        self.lbl_par1 = tk.Label(self.master, image=self.ima_off, bd=0)
        # Disable stats
        self.lbl_par2 = tk.Label(self.master, image=self.ima_off, bd=0)
        # # Disable stats
        # self.lbl_par3 = tk.Label(self.master, image=self.ima_off, bd=0)
        # self.lbl_par4 = tk.Label(self.master, image=self.ima_on, bd=0)
        # self.lbl_par5 = tk.Label(self.master, image=self.ima_off, bd=0)
        # self.lbl_par6 = tk.Label(self.master, image=self.ima_on, bd=0)
        # self.lbl_par7 = tk.Label(self.master, image=self.ima_off, bd=0)
        # self.lbl_par8 = tk.Label(self.master, image=self.ima_on, bd=0)
        self.lbl_tab = tk.Label(self.master, image=self.ima_tab, bd=0)
        self.lbl_back_kp = tk.Label(self.master, image=self.ima_back_kp, bd=0)
        self.lbl_enter = tk.Label(self.master, image=self.ima_enter, bd=0)


        # Canvas
        self.c_keypad = tk.Canvas(self.master, width=149, height=201, bg=BG_COLOR, borderwidth=0, highlightthickness=0)

        # Entries
        self.evar_opt_feedtk_level = tk.StringVar()
        self.evar_steri_time = tk.StringVar()
        self.evar_warmup_time = tk.StringVar()
        self.evar_settle_time = tk.StringVar()


        self.ent_opt_feedtk_level = tk.Entry(self.master, textvariable=self.evar_opt_feedtk_level, font=("Roboto", 14,), bd=0,
                                       fg=FG_COLOR, highlightthickness=0, bg='white',
                                       justify=tk.RIGHT,
                                       insertwidth=0)
        self.ent_steri_time = tk.Entry(self.master, textvariable=self.evar_steri_time, font=("Roboto", 14,), bd=0,
                                       fg=FG_COLOR, highlightthickness=0, bg='white',
                                       justify=tk.RIGHT,
                                       insertwidth=0)
        self.ent_warmup_time = tk.Entry(self.master, textvariable=self.evar_warmup_time, font=("Roboto", 14,), bd=0,
                                       fg=FG_COLOR, highlightthickness=0, bg='white',
                                       justify=tk.RIGHT,
                                       insertwidth=0)
        self.ent_settle_time = tk.Entry(self.master, textvariable=self.evar_settle_time, font=("Roboto", 14,), bd=0,
                                       fg=FG_COLOR, highlightthickness=0, bg='white',
                                       justify=tk.RIGHT,
                                       insertwidth=0)

        self.ent_opt_feedtk_level.focus_set()

        # Place
        self.lbl_bg.place(x=0, y=0)
        self.lbl_back.place(x=299, y=430)
        self.lbl_labels.place(x=50, y=62)
        self.lbl_par1.place(x=440, y=62)
        self.lbl_par2.place(x=440, y=103)
        # self.lbl_par3.place(x=440, y=144)
        # self.lbl_par4.place(x=440, y=185)
        # self.lbl_par5.place(x=440, y=226)
        # self.lbl_par6.place(x=440, y=267)
        # self.lbl_par7.place(x=440, y=308)
        # self.lbl_par8.place(x=440, y=349)
        self.lbl_tab.place(x=736, y=188)
        self.lbl_back_kp.place(x=736, y=240)
        self.lbl_enter.place(x=736, y=292)

        self.c_keypad.place(x=580, y=188)

        self.ent_opt_feedtk_level.place(x=360, y = 152, width=140)
        self.ent_steri_time.place(x=360, y=192, width=140)
        self.ent_warmup_time.place(x=360, y=232, width=140)
        self.ent_settle_time.place(x=360, y=272, width=140)

        self.place_keys()
        self.inits()


    def inits(self):
        if self.constructor.db['enable_semi_auto'][1]:
            self.lbl_par1['image'] = self.ima_on
        else:
            self.lbl_par1['image'] = self.ima_off

        # Disable stats switch always starts off
        self.lbl_par2['image'] = self.ima_off

        self.evar_opt_feedtk_level.set(self.constructor.db['opt_feedtk_level'][3])
        self.evar_steri_time.set(self.constructor.db['steri_time'][3])
        self.evar_warmup_time.set(self.constructor.db['warmup_time'][3])
        self.evar_settle_time.set(self.constructor.db['settle_time'][3])


    def endit(self):
        with open('db', 'wb') as f:
            pickle.dump(self.constructor.db, f)


    # Bindings
    def binds(self):
        self.lbl_back.bind('<Button-1>', self.back_call)
        self.lbl_par1.bind('<Button-1>', self.par1_call)
        self.lbl_par2.bind('<Button-1>', self.par2_call)
        self.c_keypad.bind('<Button-1>', self.canvas_callback)
        self.lbl_back_kp.bind('<Button-1>', self.back_kp_call)
        self.lbl_enter.bind('<Button-1>', self.enter_call)
        self.lbl_tab.bind('<Button-1>', self.tab_call)
        self.ent_opt_feedtk_level.bind('<FocusIn>', self.set_focus_opt_feedtk_level)
        self.ent_steri_time.bind('<FocusIn>', self.set_focus_steri_time)
        self.ent_warmup_time.bind('<FocusIn>', self.set_focus_warmup_time)
        self.ent_settle_time.bind('<FocusIn>', self.set_focus_settle_time)
        self.ent_opt_feedtk_level.bind('<FocusOut>', self.dummy_focus_out_fn)
        self.ent_steri_time.bind('<FocusOut>', self.dummy_focus_out_fn)
        self.ent_warmup_time.bind('<FocusOut>', self.dummy_focus_out_fn)
        self.ent_settle_time.bind('<FocusOut>', self.dummy_focus_out_fn)

    # FocusOut passes a variable to the callback (here represented by the event variable)
    def dummy_focus_out_fn(self, event):
        self.validate_entries()

    def unbinds(self):
        self.lbl_back.unbind('<Button-1>')
        self.lbl_par1.unbind('<Button-1>')
        self.lbl_par2.unbind('<Button-1>')
        self.c_keypad.unbind('<Button-1>')
        self.lbl_back_kp.unbind('<Button-1>')
        self.lbl_enter.unbind('<Button-1>')
        self.lbl_tab.unbind('<Button-1>')
        self.ent_opt_feedtk_level.unbind('<FocusIn>')
        self.ent_steri_time.unbind('<FocusIn>')
        self.ent_warmup_time.unbind('<FocusIn>')
        self.ent_settle_time.unbind('<FocusIn>')

    def set_focus_opt_feedtk_level(self, event):
        self.focus = 0

    def set_focus_steri_time(self, event):
        self.focus = 1

    def set_focus_warmup_time(self, event):
        self.focus = 2

    def set_focus_settle_time(self, event):
        self.focus = 3


    def back_call(self, event):
        if self.constructor.global_focus != 'params':
            return
        flag = 'settings'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.settingspanel, self.master, self.lbl_back, self.ima_back, self.ima_back_push, flag, self.constructor.settingsapp)
        self.master.after(1200, self.clean_up)

    def par1_call(self, event):
        if self.constructor.global_focus != 'params':
            return
        if self.constructor.db['enable_semi_auto'][1]:
            self.constructor.db['enable_semi_auto'][1] = False
        else:
            self.constructor.db['enable_semi_auto'][1] = True
        self.inits()
        self.endit()

    # Disable stats
    def par2_call(self, event):
        self.lbl_par2['image'] = self.ima_on

        self.constructor.db['feedpmp_tubelife'][0] = 0
        self.constructor.db['outpmp_tubelife'][0] = 0
        self.constructor.db['feedpmp_op_time'][0] = 0
        self.constructor.db['recirpmp_op_time'][0] = 0
        self.constructor.db['outpmp_op_time'][0] = 0
        self.constructor.db['o3_op_time'][0] = 0
        self.constructor.db['uv_op_time'][0] = 0
        self.constructor.db['o3_dest_op_time'][0] = 0
        self.constructor.db['steri_cycles'][0] = 0

        self.constructor.anim_pop(event, self.constructor.pop_resetstatspanel, self.master, self)
        # TODO: The ideal situation would be the label turning off only after the user dismisses
        # the pop-up
        self.master.after(500, self.inits)
        self.endit()


    def place_keys(self, width=45, height=45):
        for k, v in self.keypad_dict.items():
            xpos = v[0]
            ypos = v[1]
            x1pos = xpos + width
            y1pos = ypos + height
            textxpos = xpos + width / 2
            textypos = ypos + height / 2
            self.create_rounded_rec(xpos, ypos, self.radius, width, height, k)
            tag = k[1:]
            self.c_keypad.create_text(textxpos, textypos, font=('Roboto', 18), text=tag, fill=FG_COLOR)
        # Zero key
        xpos = 0
        ypos = 156
        x1pos = xpos + width * 2 + 7
        y1pos = ypos + height
        textxpos = xpos + width + 3.5
        textypos = ypos + height / 2
        self.create_rounded_rec(xpos, ypos, self.radius, width*2+7, height, 'k0', fillcolor='white')
        self.c_keypad.create_text(textxpos, textypos, font=('Roboto', 18), text='0', fill=FG_COLOR)

    def canvas_callback(self, event, width=45, height=45):
        if event.x > self.keypad_dict['k1'][0] and event.x < self.keypad_dict['k1'][0] + width and event.y > self.keypad_dict['k1'][1] and event.y < self.keypad_dict['k1'][1] + height:
            self.c_keypad.itemconfigure('k1', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k1'))
            self.digest_key('k1')
        elif event.x > self.keypad_dict['k2'][0] and event.x < self.keypad_dict['k2'][0] + width and event.y > self.keypad_dict['k2'][1] and event.y < self.keypad_dict['k2'][1] + height:
            self.c_keypad.itemconfigure('k2', fill=LIGHT_GRAY_COLOR)#, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k2'))
            self.digest_key('k2')
        elif event.x > self.keypad_dict['k3'][0] and event.x < self.keypad_dict['k3'][0] + width and event.y > self.keypad_dict['k3'][1] and event.y < self.keypad_dict['k3'][1] + height:
            self.c_keypad.itemconfigure('k3', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k3'))
            self.digest_key('k3')
        elif event.x > self.keypad_dict['k4'][0] and event.x < self.keypad_dict['k4'][0] + width and event.y > self.keypad_dict['k4'][1] and event.y < self.keypad_dict['k4'][1] + height:
            self.c_keypad.itemconfigure('k4', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k4'))
            self.digest_key('k4')
        elif event.x > self.keypad_dict['k5'][0] and event.x < self.keypad_dict['k5'][0] + width and event.y > self.keypad_dict['k5'][1] and event.y < self.keypad_dict['k5'][1] + height:
            self.c_keypad.itemconfigure('k5', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k5'))
            self.digest_key('k5')
        elif event.x > self.keypad_dict['k6'][0] and event.x < self.keypad_dict['k6'][0] + width and event.y > self.keypad_dict['k6'][1] and event.y < self.keypad_dict['k6'][1] + height:
            self.c_keypad.itemconfigure('k6', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k6'))
            self.digest_key('k6')
        elif event.x > self.keypad_dict['k7'][0] and event.x < self.keypad_dict['k7'][0] + width and event.y > self.keypad_dict['k7'][1] and event.y < self.keypad_dict['k7'][1] + height:
            self.c_keypad.itemconfigure('k7', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k7'))
            self.digest_key('k7')
        elif event.x > self.keypad_dict['k8'][0] and event.x < self.keypad_dict['k8'][0] + width and event.y > self.keypad_dict['k8'][1] and event.y < self.keypad_dict['k8'][1] + height:
            self.c_keypad.itemconfigure('k8', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k8'))
            self.digest_key('k8')
        elif event.x > self.keypad_dict['k9'][0] and event.x < self.keypad_dict['k9'][0] + width and event.y > self.keypad_dict['k9'][1] and event.y < self.keypad_dict['k9'][1] + height:
            self.c_keypad.itemconfigure('k9', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k9'))
            self.digest_key('k9')
        elif event.x > self.keypad_dict['k.'][0] and event.x < self.keypad_dict['k.'][0] + width and event.y > self.keypad_dict['k.'][1] and event.y < self.keypad_dict['k.'][1] + height:
            self.c_keypad.itemconfigure('k.', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k.'))
            self.digest_key('k.')
        elif event.x > 0 and event.x < 97 and event.y > 156 and event.y < 156 + height:
            self.c_keypad.itemconfigure('k0', fill=LIGHT_GRAY_COLOR, outline=LIGHT_GRAY_COLOR)
            self.master.after(200, lambda: self.anim_keys('k0'))
            self.digest_key('k0')

    def back_kp_call(self, event):
        if self.constructor.global_focus != 'params':
            return
        self.lbl_back_kp['image'] = self.ima_back_kp_push
        self.master.after(200, lambda: self.anim_keys('back_kp'))
        self.back_kp_call_after()

    def back_kp_call_after(self):
        if self.focus == 0:
            if self.evar_opt_feedtk_level.get() == '0.0':
                return
            len_ent = len(self.ent_opt_feedtk_level.get())
            if len_ent > 1:
                self.ent_opt_feedtk_level.delete(len_ent-1, tk.END)
            elif len_ent == 1:
                self.ent_opt_feedtk_level.delete(len_ent-1, tk.END)
                self.ent_opt_feedtk_level.insert(tk.END, '0.0')
        elif self.focus == 1:
            if self.evar_steri_time.get() == '0.0':
                return
            len_ent = len(self.ent_steri_time.get())
            if len_ent > 1:
                self.ent_steri_time.delete(len_ent-1, tk.END)
            elif len_ent == 1:
                self.ent_steri_time.delete(len_ent-1, tk.END)
                self.ent_steri_time.insert(tk.END, '0.0')
        elif self.focus == 2:
            if self.evar_warmup_time.get() == '0.0':
                return
            len_ent = len(self.ent_warmup_time.get())
            if len_ent > 1:
                self.ent_warmup_time.delete(len_ent-1, tk.END)
            elif len_ent == 1:
                self.ent_warmup_time.delete(len_ent-1, tk.END)
                self.ent_warmup_time.insert(tk.END, '0.0')
        elif self.focus == 3:
            if self.evar_settle_time.get() == '0.0':
                return
            len_ent = len(self.ent_settle_time.get())
            if len_ent > 1:
                self.ent_settle_time.delete(len_ent-1, tk.END)
            elif len_ent == 1:
                self.ent_settle_time.delete(len_ent-1, tk.END)
                self.ent_settle_time.insert(tk.END, '0.0')

    def enter_call(self, event):
        if self.constructor.global_focus != 'params':
            return
        self.lbl_enter['image'] = self.ima_enter_push
        self.master.after(200, lambda: self.anim_keys('enter'))
        self.validate_entries()

    def validate_entries(self):
        try:
            opt_feedtk_level = float(self.evar_opt_feedtk_level.get())
            opt_feedtk_level = round(opt_feedtk_level, 1)
            steri_time = float(self.evar_steri_time.get())
            steri_time = round(steri_time, 1)
            warmup_time = float(self.evar_warmup_time.get())
            warmup_time = round(warmup_time, 1)
            settle_time = float(self.evar_settle_time.get())
            settle_time = round(settle_time, 1)

            if opt_feedtk_level > self.constructor.db['opt_feedtk_level'][1] and opt_feedtk_level < self.constructor.db['opt_feedtk_level'][2]:
                self.evar_opt_feedtk_level.set(str(opt_feedtk_level))
                self.constructor.db['opt_feedtk_level'][3] = opt_feedtk_level
            elif opt_feedtk_level < self.constructor.db['opt_feedtk_level'][1] or opt_feedtk_level > self.constructor.db['opt_feedtk_level'][2]:
                self.evar_opt_feedtk_level.set(self.constructor.db['opt_feedtk_level'][0])

            if steri_time > self.constructor.db['steri_time'][1] and steri_time < self.constructor.db['steri_time'][2]:
                self.evar_steri_time.set(str(steri_time))
                self.constructor.db['steri_time'][3] = steri_time
            elif steri_time < self.constructor.db['steri_time'][1] or steri_time > self.constructor.db['steri_time'][2]:
                self.evar_steri_time.set(self.constructor.db['steri_time'][0])

            if warmup_time > self.constructor.db['warmup_time'][1] and warmup_time < self.constructor.db['warmup_time'][2]:
                self.evar_warmup_time.set(str(warmup_time))
                self.constructor.db['warmup_time'][3] = warmup_time
            elif warmup_time < self.constructor.db['warmup_time'][1] or warmup_time > self.constructor.db['warmup_time'][2]:
                self.evar_warmup_time.set(self.constructor.db['warmup_time'][0])

            if settle_time > self.constructor.db['settle_time'][1] and settle_time < self.constructor.db['settle_time'][2]:
                self.evar_settle_time.set(str(settle_time))
                self.constructor.db['settle_time'][3] = settle_time
            elif settle_time < self.constructor.db['settle_time'][1] or settle_time > self.constructor.db['settle_time'][2]:
                self.evar_settle_time.set(self.constructor.db['settle_time'][0])



        except ValueError:
            self.evar_opt_feedtk_level.set(self.constructor.db['opt_feedtk_level'][0])
            self.evar_steri_time.set(self.constructor.db['steri_time'][0])
            self.evar_warmup_time.set(self.constructor.db['warmup_time'][0])
            self.evar_settle_time.set(self.constructor.db['settle_time'][0])

        self.inits()
        self.endit()
        
    def tab_call(self, event):
        if self.constructor.global_focus != 'params':
            return
        self.lbl_tab['image'] = self.ima_tab_push
        self.master.after(200, lambda: self.anim_keys('tab'))
        self.tab_call_after()

    def tab_call_after(self):
        if self.focus == 0:
            self.focus = 1
            self.ent_steri_time.focus_set()
        elif self.focus == 1:
            self.focus = 2
            self.ent_warmup_time.focus_set()
        elif self.focus == 2:
            self.focus = 3
            self.ent_settle_time.focus_set()
        elif self.focus == 3:
            self.focus = 0
            self.ent_opt_feedtk_level.focus_set()

        self.validate_entries()
        

    def anim_keys(self, tag):
        if tag == 'back_kp':
            self.lbl_back_kp['image'] = self.ima_back_kp
        elif tag == 'tab':
            self.lbl_tab['image'] = self.ima_tab
        elif tag == 'enter':
            self.lbl_enter['image'] = self.ima_enter
        else:
            self.c_keypad.itemconfigure(tag, fill='white', outline='white')

    def digest_key(self, tag):
        if self.constructor.global_focus != 'params':
            return
        string = tag[1:]

        if self.focus == 0:
            content = self.evar_opt_feedtk_level.get()
            if content == '0.0':
                self.ent_opt_feedtk_level.delete(0, tk.END)
            if len(str(self.evar_warmup_time.get())) < 6:
                if tag == 'k.':
                    if '.' in content:
                        return
                self.ent_opt_feedtk_level.insert(tk.END, string)

        elif self.focus == 1:
            content = self.evar_steri_time.get()
            if content == '0.0':
                self.ent_steri_time.delete(0, tk.END)
            if len(str(self.evar_steri_time.get())) < 6:
                if tag == 'k.':
                    if '.' in content:
                        return
                self.ent_steri_time.insert(tk.END, string)

        elif self.focus == 2:
            content = self.evar_warmup_time.get()
            if content == '0.0':
                self.ent_warmup_time.delete(0, tk.END)
            if len(str(self.evar_warmup_time.get())) < 6:
                if tag == 'k.':
                    if '.' in content:
                        return
                self.ent_warmup_time.insert(tk.END, string)

        elif self.focus == 3:
            content = self.evar_settle_time.get()
            if content == '0.0':
                self.ent_settle_time.delete(0, tk.END)
            if len(str(self.evar_settle_time.get())) < 6:
                if tag == 'k.':
                    if '.' in content:
                        return
                self.ent_settle_time.insert(tk.END, string)



    def create_rounded_rec(self, x, y, r, w, h, tag, fillcolor='white'):
        self.c_keypad.create_polygon(x+r, y,
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


    def clean_up(self):
        self.endit()