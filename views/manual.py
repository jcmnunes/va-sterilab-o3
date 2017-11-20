import tkinter as tk
from tkinter import font
import os
from helpers.colors import *
import math
import RPi.GPIO as GPIO
import time
import re
import graphics

graph = graphics.ImaMan()

# TODO: Counters for statistics. Maybe make some turn-on/turn-off methods.
class Winman:
    def __init__(self, constructor, master, width=848, height=480):

        # Variables
        self.constructor = constructor
        self.master = master
        self.width = width
        self.height = height
        self.toggle_feedpmp = "off"
        self.toggle_recirpmp = "off"
        self.toggle_outpmp = "off"
        self.toggle_o2 = "off"
        self.toggle_o3 = "off"
        self.toggle_uv = "off"

        # Initiate some counters for stats
        self.start_feedpmp_counter = 0
        self.stop_feedpmp_counter = 0
        self.start_recirpmp_counter = 0
        self.stop_recirpmp_counter = 0
        self.start_outpmp_counter = 0
        self.stop_feedpmp_counter = 0
        self.start_o2_counter = 0
        self.stop_o2_counter = 0
        self.start_o3_counter = 0
        self.stop_o3_counter = 0
        self.start_uv_counter = 0
        self.stop_uv_counter = 0

        # Coordinates pumps canvas
        self.t = 10 * math.pi / 180

        self.x00_feedpmp, self.y00_feedpmp = 115, 129
        self.x10_feedpmp, self.y10_feedpmp = 132, 139
        self.x20_feedpmp, self.y20_feedpmp = 115, 149
        self.x0_feedpmp, self.y0_feedpmp = self.x00_feedpmp, self.y00_feedpmp
        self.x1_feedpmp, self.y1_feedpmp = self.x10_feedpmp, self.y10_feedpmp
        self.x2_feedpmp, self.y2_feedpmp = self.x20_feedpmp, self.y20_feedpmp
        self.feedpmp_center = 121, 139


        self.x00_recirpmp, self.y00_recirpmp = 173, 11
        self.x10_recirpmp, self.y10_recirpmp = 190, 21
        self.x20_recirpmp, self.y20_recirpmp = 173, 31
        self.x0_recirpmp, self.y0_recirpmp = self.x00_recirpmp, self.y00_recirpmp
        self.x1_recirpmp, self.y1_recirpmp = self.x10_recirpmp, self.y10_recirpmp
        self.x2_recirpmp, self.y2_recirpmp = self.x20_recirpmp, self.y20_recirpmp
        self.recirpmp_center = 179, 21

        self.x00_outpmp, self.y00_outpmp = 229, 129
        self.x10_outpmp, self.y10_outpmp = 246, 139
        self.x20_outpmp, self.y20_outpmp = 229, 149
        self.x0_outpmp, self.y0_outpmp = self.x00_outpmp, self.y00_outpmp
        self.x1_outpmp, self.y1_outpmp = self.x10_outpmp, self.y10_outpmp
        self.x2_outpmp, self.y2_outpmp = self.x20_outpmp, self.y20_outpmp
        self.outpmp_center = 235, 139

        self.canvas_feedlevel_x = 43
        self.canvas_feedlevel_y = 86
        self.canvas_feedlevel_w = 42
        self.canvas_feedlevel_h = 64

        self.canvas_reactor_min_x = 183
        self.canvas_reactor_min_y = 72
        self.canvas_reactor_min_w = 8
        self.canvas_reactor_min_h = 8

        self.canvas_reactor_max_x = 183
        self.canvas_reactor_max_y = 113
        self.canvas_reactor_max_w = 8
        self.canvas_reactor_max_h = 8

        self.label_feedlevel_x = 0
        self.label_feedlevel_y = 0
        self.label_feedlevel_w = 50
        self.label_feedlevel_h = 77
        
        # PhotoImage instances
        self.ima_bg = tk.PhotoImage(master=self.master, data=graph.bg)
        self.ima_levels00 = tk.PhotoImage(master=self.master, data=graph.levels00)
        self.ima_levels01 = tk.PhotoImage(master=self.master, data=graph.levels01)
        self.ima_levels10 = tk.PhotoImage(master=self.master, data=graph.levels10)
        self.ima_levels11 = tk.PhotoImage(master=self.master, data=graph.levels11)
        self.ima_on = tk.PhotoImage(master=self.master, data=graph.on)
        self.ima_off = tk.PhotoImage(master=self.master, data=graph.off)
        self.ima_shut = tk.PhotoImage(master=self.master, data=graph.shut)
        self.ima_shut_push = tk.PhotoImage(master=self.master, data=graph.shut_push)
        self.ima_feed0 = tk.PhotoImage(master=self.master, data=graph.feed0)
        self.ima_feed1 = tk.PhotoImage(master=self.master, data=graph.feed1)
        self.ima_o30 = tk.PhotoImage(master=self.master, data=graph.o30)
        self.ima_o31 = tk.PhotoImage(master=self.master, data=graph.o31)
        self.ima_out0 = tk.PhotoImage(master=self.master, data=graph.out0)
        self.ima_out1 = tk.PhotoImage(master=self.master, data=graph.out1)
        self.ima_o2_recir00 = tk.PhotoImage(master=self.master, data=graph.o2_recir00)
        self.ima_o2_recir01 = tk.PhotoImage(master=self.master, data=graph.o2_recir01)
        self.ima_o2_recir10 = tk.PhotoImage(master=self.master, data=graph.o2_recir10)
        self.ima_o2_recir11 = tk.PhotoImage(master=self.master, data=graph.o2_recir11)
        self.ima_uv0 = tk.PhotoImage(master=self.master, data=graph.uv0)
        self.ima_uv1 = tk.PhotoImage(master=self.master, data=graph.uv1)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_shut = tk.Label(self.master, image=self.ima_shut, bd=0)
        self.lbl_feedpmp = tk.Label(self.master, image=self.ima_off, bd=0)
        self.lbl_recirpmp = tk.Label(self.master, image=self.ima_off, bd=0)
        self.lbl_outpmp = tk.Label(self.master, image=self.ima_off, bd=0)
        self.lbl_o2 = tk.Label(self.master, image=self.ima_off, bd=0)
        self.lbl_o3 = tk.Label(self.master, image=self.ima_off, bd=0)
        self.lbl_uv = tk.Label(self.master, image=self.ima_off, bd=0)
        self.lbl_rxlevels = tk.Label(self.master, image=self.ima_levels00, bd=0)
        self.lbl_level_percent = tk.Label(self.master, text='', bg='white', bd=0, fg=FG_COLOR, font=('Roboto', 10))

        # Sinotico
        self.w = tk.Canvas(self.master, width=300, height=160, bg='white', highlightthickness=0)
        self.canvas_out = self.w.create_image(198, 0, image=self.ima_out0, anchor=tk.NW)
        self.canvas_uv = self.w.create_image(224, 9, image=self.ima_uv0, anchor=tk.NW)
        self.canvas_o2_recir = self.w.create_image(0, 0, image=self.ima_o2_recir00, anchor=tk.NW)
        self.canvas_feed = self.w.create_image(-1, 118, image=self.ima_feed0, anchor=tk.NW)
        self.canvas_o3 = self.w.create_image(108, 8, image=self.ima_o30, anchor=tk.NW)

        self.feedpmp = self.w.create_polygon(self.x0_feedpmp, self.y0_feedpmp,
                                             self.x1_feedpmp, self.y1_feedpmp,
                                             self.x2_feedpmp, self.y2_feedpmp,
                                             width=2, fill='white', outline=FG_COLOR,
                                             tags=('filling_poly', ))

        self.recirpmp = self.w.create_polygon(self.x0_recirpmp, self.y0_recirpmp,
                                             self.x1_recirpmp, self.y1_recirpmp,
                                             self.x2_recirpmp, self.y2_recirpmp,
                                             width=2, fill='white', outline=FG_COLOR,
                                             tags=('recirpmp_poly', ))

        self.outpmp = self.w.create_polygon(self.x0_outpmp, self.y0_outpmp,
                                             self.x1_outpmp, self.y1_outpmp,
                                             self.x2_outpmp, self.y2_outpmp,
                                             width=2, fill='white', outline=FG_COLOR,
                                             tags='out_poly')

        self.feedlevel = self.w.create_rectangle(self.canvas_feedlevel_x,
                                                 self.canvas_feedlevel_y, 
                                                 self.canvas_feedlevel_x + self.canvas_feedlevel_w - 1,
                                                 self.canvas_feedlevel_y + self.canvas_feedlevel_h -1,
                                                 width=2, fill=GREEN_COLOR, outline=GREEN_COLOR)

        self.w.create_rectangle(self.canvas_reactor_min_x,
                                self.canvas_reactor_min_y,
                                self.canvas_reactor_min_x + self.canvas_reactor_min_w - 1,
                                self.canvas_reactor_min_y + self.canvas_reactor_min_h - 1,
                                width=1, fill=GREEN_COLOR, outline=GREEN_COLOR, tags=('reactor_max_level', ))

        self.w.create_rectangle(self.canvas_reactor_max_x,
                                self.canvas_reactor_max_y,
                                self.canvas_reactor_max_x + self.canvas_reactor_max_w - 1,
                                self.canvas_reactor_max_y + self.canvas_reactor_max_h - 1,
                                width=1, fill=GREEN_COLOR, outline=GREEN_COLOR, tags=('reactor_min_level', ))


        # Levels in label
        self.w_l1 = tk.Canvas(self.master, width=10, height=10, bg=GREEN_COLOR, highlightthickness=0)

        self.w_l2 = tk.Canvas(self.master, width=10, height=10, bg=GREEN_COLOR, highlightthickness=0)
        
        self.w_lfeed = tk.Canvas(self.master, width=50, height=77, bg=BG_COLOR, highlightthickness=0)
        
        self.w_lfeed.create_rectangle(self.canvas_reactor_max_x,
                                      self.canvas_reactor_max_y,
                                      self.canvas_reactor_max_x + self.canvas_reactor_max_w,
                                      self.canvas_reactor_max_y + self.canvas_reactor_max_h, 
                                      fill=GREEN_COLOR, outline=GREEN_COLOR, tags=('feedlevel2', ))

        # Place Labels
        self.lbl_bg.place(x=0, y=0)
        self.lbl_shut.place(x=44, y=382)
        self.lbl_feedpmp.place(x=545, y=107)
        self.lbl_recirpmp.place(x=545, y=162)
        self.lbl_outpmp.place(x=545, y=217)
        self.lbl_o2.place(x=545, y=272)
        self.lbl_o3.place(x=545, y=327)
        self.lbl_uv.place(x=545, y=382)
        self.lbl_rxlevels.place(x=680, y=242)
        self.w.place(x=44, y=217)
        self.w_l1.place(x=732, y=169)
        self.w_l2.place(x=732, y=124)
        self.w_lfeed.place(x=705, y=293)
        self.lbl_level_percent.place(x=740, y=408)

    def binds(self):
        self.lbl_feedpmp.bind("<Button-1>", self.feedpmp_call)
        self.lbl_recirpmp.bind("<Button-1>", self.recirpmp_call)
        self.lbl_outpmp.bind("<Button-1>", self.outpmp_call)
        self.lbl_o2.bind("<Button-1>", self.o2_call)
        self.lbl_o3.bind("<Button-1>", self.o3_call)
        self.lbl_uv.bind("<Button-1>", self.uv_call)
        self.lbl_shut.bind("<Button-1>", self.shut_call)

    def unbinds(self):
        self.lbl_feedpmp.unbind('<Button-1>')
        self.lbl_recirpmp.unbind('<Button-1>')
        self.lbl_outpmp.unbind('<Button-1>')
        self.lbl_o2.unbind('<Button-1>')
        self.lbl_o3.unbind('<Button-1>')
        self.lbl_uv.unbind('<Button-1>')
        self.lbl_shut.unbind('<Button-1>')

    def inits(self):
        self.winloop()

    def winloop(self):
        if self.constructor.global_focus != 'man':
            return
        # while self.constructor.queue.qsize():
        try:
            self.text = self.constructor.queue.get()
            self.constructor.queue.task_done()
            result = re.search('temp(.*)photo(.*)', self.text)
            self.feed_level_arduino = int(result.group(1))

            if self.feed_level_arduino > self.constructor.etape_max:
                self.feed_level_arduino = self.constructor.etape_max
            if self.feed_level_arduino < self.constructor.etape_min:
                self.feed_level_arduino = self.constructor.etape_min

            self.canvas_feedlevel_yduino = int((self.feed_level_arduino -
                self.constructor.etape_min) * (-self.canvas_feedlevel_h / (self.constructor.etape_max -
                self.constructor.etape_min)) + self.canvas_feedlevel_y + self.canvas_feedlevel_h)
            self.label_feedlevel_yduino = int((self.feed_level_arduino -
                self.constructor.etape_min) * (-self.label_feedlevel_h / (self.constructor.etape_max -
                self.constructor.etape_min)) + self.label_feedlevel_y + self.label_feedlevel_h)

            self.w.coords(self.feedlevel, self.canvas_feedlevel_x + 1,
                                          self.canvas_feedlevel_yduino,
                                          self.canvas_feedlevel_x + self.canvas_feedlevel_w - 1,
                                          self.canvas_feedlevel_y + self.canvas_feedlevel_h - 1)

            self.w_lfeed.coords('feedlevel2', self.label_feedlevel_x,
                                              self.label_feedlevel_yduino,
                                              self.label_feedlevel_x + self.label_feedlevel_w,
                                              self.label_feedlevel_y + self.label_feedlevel_h)

            self.level_percent = int(self.feed_level_arduino / self.constructor.etape_max * 100)
            self.lbl_level_percent['text'] = '{0} %'.format(self.level_percent)

            if self.level_percent > 90 or self.level_percent < 10:
                self.w.itemconfigure(self.feedlevel, fill=RED_COLOR, outline=RED_COLOR)
                self.w_lfeed.itemconfigure('feedlevel2', fill=RED_COLOR, outline=RED_COLOR)
                self.lbl_level_percent['fg'] = RED_COLOR
            else:
                self.w.itemconfigure(self.feedlevel, fill=GREEN_COLOR, outline=GREEN_COLOR)
                self.w_lfeed.itemconfigure('feedlevel2', fill=GREEN_COLOR, outline=GREEN_COLOR)
                self.lbl_level_percent['fg'] = GREEN_COLOR

            self.l1_open = GPIO.input(self.constructor.reactor_llow_pin)
            self.l2_open = GPIO.input(self.constructor.reactor_lhigh_pin)

            if self.l1_open:
                self.w.itemconfigure('reactor_min_level', fill=RED_COLOR, outline=RED_COLOR)
                self.w_l1.config(bg=RED_COLOR)
                if self.l2_open:
                    self.lbl_rxlevels['image'] = self.ima_levels00
                else:
                    self.lbl_rxlevels['image'] = self.ima_levels01
            else:
                self.w.itemconfigure('reactor_min_level', fill=GREEN_COLOR, outline=GREEN_COLOR)
                self.w_l1.config(bg=GREEN_COLOR)
                if self.l2_open:
                    self.lbl_rxlevels['image'] = self.ima_levels10
                else:
                    self.lbl_rxlevels['image'] = self.ima_levels11

            if self.l2_open:
                self.w.itemconfigure('reactor_max_level', fill=GREEN_COLOR, outline=GREEN_COLOR)
                self.w_l2.config(bg=GREEN_COLOR)
                if self.l1_open:
                    self.lbl_rxlevels['image'] = self.ima_levels00
                else:
                    self.lbl_rxlevels['image'] = self.ima_levels10
            else:
                self.w.itemconfigure('reactor_max_level', fill=RED_COLOR, outline=RED_COLOR)
                self.w_l2.config(bg=RED_COLOR)
                if self.l1_open:
                    self.lbl_rxlevels['image'] = self.ima_levels01
                else:
                    self.lbl_rxlevels['image'] = self.ima_levels11

        except Exception as e:
            print(e)

        self.master.after(600, self.winloop)

    def feedpmp_call(self, event):
        if self.constructor.global_focus != 'man':
            return
        if self.toggle_feedpmp == 'off':
            self.lbl_feedpmp['image'] = self.ima_on
            self.w.itemconfigure(self.canvas_feed, image=self.ima_feed1)
            self.w.itemconfigure('filling_poly', outline=WRONG_LIGHT_BLUE_COLOR)
            self.master.after(10, self.rotate_feedpmp)
            self.turn_feedpmp_on()
        else:
            self.lbl_feedpmp['image'] = self.ima_off
            self.w.itemconfigure(self.canvas_feed, image=self.ima_feed0)
            self.w.itemconfigure('filling_poly', outline=FG_COLOR)
            self.turn_feedpmp_off()

    def rotate_feedpmp(self):
        if self.toggle_feedpmp == 'on':
            self.x0_feedpmp, self.y0_feedpmp = self._rot_feedpmp(self.x0_feedpmp, self.y0_feedpmp)
            self.x1_feedpmp, self.y1_feedpmp = self._rot_feedpmp(self.x1_feedpmp, self.y1_feedpmp)
            self.x2_feedpmp, self.y2_feedpmp = self._rot_feedpmp(self.x2_feedpmp, self.y2_feedpmp)
            self.w.coords(self.feedpmp, self.x0_feedpmp, self.y0_feedpmp, self.x1_feedpmp, self.y1_feedpmp, self.x2_feedpmp, self.y2_feedpmp)
            self.master.after(30, self.rotate_feedpmp)
        else:
            self.x0_feedpmp, self.y0_feedpmp = self.x00_feedpmp, self.y00_feedpmp
            self.x1_feedpmp, self.y1_feedpmp = self.x10_feedpmp, self.y10_feedpmp
            self.x2_feedpmp, self.y2_feedpmp = self.x20_feedpmp, self.y20_feedpmp
            self.w.coords(self.feedpmp, self.x0_feedpmp, self.y0_feedpmp, self.x1_feedpmp, self.y1_feedpmp, self.x2_feedpmp, self.y2_feedpmp)

    def _rot_feedpmp(self, x, y):
        x -= self.feedpmp_center[0]
        y -= self.feedpmp_center[1]
        _x = x * math.cos(self.t) - y * math.sin(self.t)
        _y = x * math.sin(self.t) + y * math.cos(self.t)
        return _x + self.feedpmp_center[0], _y + self.feedpmp_center[1]


    def recirpmp_call(self, event):
        if self.constructor.global_focus != 'man':
            return
        if self.toggle_recirpmp == 'off':
            self.lbl_recirpmp['image'] = self.ima_on
            if self.toggle_o2 == 'on':
                self.w.itemconfigure(self.canvas_o2_recir, image=self.ima_o2_recir11)
            else:
                self.w.itemconfigure(self.canvas_o2_recir, image=self.ima_o2_recir01)
            self.w.itemconfigure('recirpmp_poly', outline=WRONG_LIGHT_BLUE_COLOR)
            self.master.after(10, self.rotate_recirpmp)
            self.turn_recirpmp_on()
        else:
            self.lbl_recirpmp['image'] = self.ima_off
            if self.toggle_o2 == 'on':
                self.w.itemconfigure(self.canvas_o2_recir, image=self.ima_o2_recir10)
            else:
                self.w.itemconfigure(self.canvas_o2_recir, image=self.ima_o2_recir00)
            self.w.itemconfigure('recirpmp_poly', outline=FG_COLOR)
            self.turn_recirpmp_off()

    def rotate_recirpmp(self):
        if self.toggle_recirpmp == 'on':
            self.x0_recirpmp, self.y0_recirpmp = self._rot_recirpmp(self.x0_recirpmp, self.y0_recirpmp)
            self.x1_recirpmp, self.y1_recirpmp = self._rot_recirpmp(self.x1_recirpmp, self.y1_recirpmp)
            self.x2_recirpmp, self.y2_recirpmp = self._rot_recirpmp(self.x2_recirpmp, self.y2_recirpmp)
            self.w.coords(self.recirpmp, self.x0_recirpmp, self.y0_recirpmp, self.x1_recirpmp, self.y1_recirpmp, self.x2_recirpmp, self.y2_recirpmp)
            self.master.after(30, self.rotate_recirpmp)
        else:
            self.x0_recirpmp, self.y0_recirpmp = self.x00_recirpmp, self.y00_recirpmp
            self.x1_recirpmp, self.y1_recirpmp = self.x10_recirpmp, self.y10_recirpmp
            self.x2_recirpmp, self.y2_recirpmp = self.x20_recirpmp, self.y20_recirpmp
            self.w.coords(self.recirpmp, self.x0_recirpmp, self.y0_recirpmp, self.x1_recirpmp, self.y1_recirpmp, self.x2_recirpmp, self.y2_recirpmp)

    def _rot_recirpmp(self, x, y):
        x -= self.recirpmp_center[0]
        y -= self.recirpmp_center[1]
        _x = x * math.cos(self.t) - y * math.sin(self.t)
        _y = x * math.sin(self.t) + y * math.cos(self.t)
        return _x + self.recirpmp_center[0], _y + self.recirpmp_center[1]


    def outpmp_call(self, event):
        if self.constructor.global_focus != 'man':
            return
        if self.toggle_outpmp == 'off':
            self.lbl_outpmp['image'] = self.ima_on
            self.w.itemconfigure(self.canvas_out, image=self.ima_out1)
            # self.w.itemconfigure('out_line', fill=WRONG_LIGHT_BLUE_COLOR)
            self.w.itemconfigure('out_poly', outline=WRONG_LIGHT_BLUE_COLOR)
            self.master.after(10, self.rotate_outpmp)
            self.turn_outpmp_on()
        else:
            self.lbl_outpmp['image'] = self.ima_off
            self.w.itemconfigure(self.canvas_out, image=self.ima_out0)
            self.w.itemconfigure('out_poly', outline=FG_COLOR)
            self.turn_outpmp_off()

    def rotate_outpmp(self):
        if self.toggle_outpmp == 'on':
            self.x0_outpmp, self.y0_outpmp = self._rot_outpmp(self.x0_outpmp, self.y0_outpmp)
            self.x1_outpmp, self.y1_outpmp = self._rot_outpmp(self.x1_outpmp, self.y1_outpmp)
            self.x2_outpmp, self.y2_outpmp = self._rot_outpmp(self.x2_outpmp, self.y2_outpmp)
            self.w.coords(self.outpmp, self.x0_outpmp, self.y0_outpmp, self.x1_outpmp, self.y1_outpmp, self.x2_outpmp, self.y2_outpmp)
            self.master.after(30, self.rotate_outpmp)
        else:
            self.x0_outpmp, self.y0_outpmp = self.x00_outpmp, self.y00_outpmp
            self.x1_outpmp, self.y1_outpmp = self.x10_outpmp, self.y10_outpmp
            self.x2_outpmp, self.y2_outpmp = self.x20_outpmp, self.y20_outpmp
            self.w.coords(self.outpmp, self.x0_outpmp, self.y0_outpmp, self.x1_outpmp, self.y1_outpmp, self.x2_outpmp, self.y2_outpmp)
    
    def _rot_outpmp(self, x, y):
        x -= self.outpmp_center[0]
        y -= self.outpmp_center[1]
        _x = x * math.cos(self.t) - y * math.sin(self.t)
        _y = x * math.sin(self.t) + y * math.cos(self.t)
        return _x + self.outpmp_center[0], _y + self.outpmp_center[1]


    def o2_call(self, event):
        if self.constructor.global_focus != 'man':
            return
        if self.toggle_o2 == 'off':
            self.lbl_o2['image'] = self.ima_on
            if self.toggle_recirpmp == 'on':
                self.w.itemconfigure(self.canvas_o2_recir, image=self.ima_o2_recir11)
            else:
                self.w.itemconfigure(self.canvas_o2_recir, image=self.ima_o2_recir10)
            self.turn_o2_on()
        else:
            self.lbl_o2['image'] = self.ima_off
            if self.toggle_recirpmp == 'on':
                self.w.itemconfigure(self.canvas_o2_recir, image=self.ima_o2_recir01)
            else:
                self.w.itemconfigure(self.canvas_o2_recir, image=self.ima_o2_recir00)
            self.turn_o2_off()


    def o3_call(self, event):
        if self.constructor.global_focus != 'man':
            return
        if self.toggle_o3 == 'off':
            self.lbl_o3['image'] = self.ima_on
            self.w.itemconfigure(self.canvas_o3, image=self.ima_o31)
            self.turn_o3_on()
        else:
            self.lbl_o3['image'] = self.ima_off
            self.w.itemconfigure(self.canvas_o3, image=self.ima_o30)
            self.turn_o3_off()


    def uv_call(self, event):
        if self.constructor.global_focus != 'man':
            return
        if self.toggle_uv == 'off':
            self.lbl_uv['image'] = self.ima_on
            self.w.itemconfigure(self.canvas_uv, image=self.ima_uv1)
            self.turn_uv_on()
        else:
            self.lbl_uv['image'] = self.ima_off
            self.w.itemconfigure(self.canvas_uv, image=self.ima_uv0)
            self.turn_uv_off()


    def shut_call(self, event):
        self.unbinds()
        if self.constructor.global_focus != 'man':
            return
        flag = 'home'
        self.constructor.anim_btn(0, self.constructor.homepanel, self.master, self.lbl_shut, self.ima_shut, self.ima_shut_push, flag, self.constructor.homeapp)
        self.master.after(1200, self.clean_up)

    def clean_up(self):
        # for pin in self.constructor.lst_pins_out:
        #     GPIO.setup(pin, GPIO.OUT, initial=1)

        self.turn_feedpmp_off()
        self.turn_recirpmp_off()
        self.turn_outpmp_off()
        self.turn_o2_off()
        self.turn_o3_off()
        self.turn_uv_off()

        self.toggle_feedpmp = "off"
        self.toggle_recirpmp = "off"
        self.toggle_outpmp = "off"
        self.toggle_o2 = "off"
        self.toggle_o3 = "off"
        self.toggle_uv = "off"

        self.start_feedpmp_counter = 0
        self.stop_feedpmp_counter = 0
        self.start_recirpmp_counter = 0
        self.stop_recirpmp_counter = 0
        self.start_outpmp_counter = 0
        self.stop_feedpmp_counter = 0
        self.start_o2_counter = 0
        self.stop_o2_counter = 0
        self.start_o3_counter = 0
        self.stop_o3_counter = 0
        self.start_uv_counter = 0
        self.stop_uv_counter = 0

        self.w.itemconfigure('filling_poly', outline=FG_COLOR)
        self.w.itemconfigure('recirpmp_poly', outline=FG_COLOR)
        self.w.itemconfigure('out_poly', outline=FG_COLOR)
        self.lbl_feedpmp['image'] = self.ima_off
        self.w.itemconfigure(self.canvas_feed, image=self.ima_feed0)
        self.lbl_recirpmp['image'] = self.ima_off
        self.w.itemconfigure(self.canvas_o2_recir, image=self.ima_o2_recir00)
        self.lbl_outpmp['image'] = self.ima_off
        self.w.itemconfigure(self.canvas_out, image=self.ima_out0)
        self.lbl_o2['image'] = self.ima_off
        self.lbl_o3['image'] = self.ima_off
        self.w.itemconfigure(self.canvas_o3, image=self.ima_o30)
        self.lbl_uv['image'] = self.ima_off
        self.w.itemconfigure(self.canvas_uv, image=self.ima_uv0)

        self.binds()


    def turn_feedpmp_on(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.feedpmp_pin) == self.constructor.db['ON']:
        #     print('Attempted to turn on the feed pump when it was already turned on.')
        if self.toggle_feedpmp == 'on':
            print('Attempted to turn on the feed pump when it was already turned on.')
        else:
            GPIO.output(self.constructor.feedpmp_pin, self.constructor.db['ON'])
            self.toggle_feedpmp = 'on'
            self.start_feedpmp_counter = time.time()

    def turn_feedpmp_off(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.feedpmp_pin) == self.constructor.db['OFF']:
        #     print('Attempted to turn off the feed pump when it was already turned off.')
        if self.toggle_feedpmp == 'off':
            print('Attempted to turn off the feed pump when it was already turned off.')
        else:
            GPIO.output(self.constructor.feedpmp_pin, self.constructor.db['OFF'])
            self.toggle_feedpmp = 'off'
            if self.start_feedpmp_counter != 0:
                self.stop_feedpmp_counter = time.time()
                elapsed_time_min = ((self.stop_feedpmp_counter - self.start_feedpmp_counter) / 60)
                elapsed_time_min = round(elapsed_time_min, 1)
                self.constructor.db['feedpmp_op_time'][0] += elapsed_time_min
                self.constructor.db['feedpmp_tubelife'][0] += elapsed_time_min
                self.constructor.save_db()
                self.start_feedpmp_counter = 0
                self.stop_feedpmp_counter = 0
                

    def turn_recirpmp_on(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.recirpmp_pin) == self.constructor.db['ON']:
        #     print('Attempted to turn on the recir pump when it was already turned on.')
        if self.toggle_recirpmp == 'on':
            print('Attempted to turn on the recir pump when it was already turned on.')
        else:
            GPIO.output(self.constructor.recirpmp_pin, self.constructor.db['ON'])
            self.toggle_recirpmp = 'on'
            self.start_recirpmp_counter = time.time()

    def turn_recirpmp_off(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.recirpmp_pin) == self.constructor.db['OFF']:
        #     print('Attempted to turn off the recir pump when it was already turned off.')
        if self.toggle_recirpmp == 'off':
            print('Attempted to turn off the recir pump when it was already turned off.')
        else:
            GPIO.output(self.constructor.recirpmp_pin, self.constructor.db['OFF'])
            self.toggle_recirpmp = 'off'
            if self.start_recirpmp_counter != 0:
                self.stop_recirpmp_counter = time.time()
                elapsed_time_min = ((self.stop_recirpmp_counter - self.start_recirpmp_counter) / 60)
                elapsed_time_min = round(elapsed_time_min, 1)
                self.constructor.db['recirpmp_op_time'][0] += elapsed_time_min
                self.constructor.save_db()
                self.start_recirpmp_counter = 0
                self.stop_recirpmp_counter = 0


    def turn_outpmp_on(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.outpmp_pin) == self.constructor.db['ON']:
        #     print('Attempted to turn on the out pump when it was already turned on.')
        if self.toggle_outpmp == 'on':
            print('Attempted to turn on the out pump when it was already turned on.')
        else:
            GPIO.output(self.constructor.outpmp_pin, self.constructor.db['ON'])
            self.toggle_outpmp = 'on'
            self.start_outpmp_counter = time.time()

    def turn_outpmp_off(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.outpmp_pin) == self.constructor.db['OFF']:
        #     print('Attempted to turn off the out pump when it was already turned off.')
        if self.toggle_outpmp == 'off':
            print('Attempted to turn off the out pump when it was already turned off.')
        else:
            GPIO.output(self.constructor.outpmp_pin, self.constructor.db['OFF'])
            self.toggle_outpmp = 'off'
            if self.start_outpmp_counter != 0:
                self.stop_outpmp_counter = time.time()
                elapsed_time_min = ((self.stop_outpmp_counter - self.start_outpmp_counter) / 60)
                elapsed_time_min = round(elapsed_time_min, 1)
                self.constructor.db['outpmp_op_time'][0] += elapsed_time_min
                self.constructor.db['outpmp_tubelife'][0] += elapsed_time_min
                self.constructor.save_db()
                self.start_outpmp_counter = 0
                self.stop_outpmp_counter = 0


    def turn_o2_on(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.o2_pin) == self.constructor.db['ON']:
        #     print('Attempted to turn on the out pump when it was already turned on.')
        if self.toggle_o2 == 'on':
            print('Attempted to open O2 valve when it was already open.')
        else:
            GPIO.output(self.constructor.o2_pin, self.constructor.db['ON'])
            self.toggle_o2 = 'on'

    def turn_o2_off(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.o2_pin) == self.constructor.db['OFF']:
        #     print('Attempted to turn off the out pump when it was already turned off.')
        if self.toggle_o2 == 'off':
            print('Attempted to close the O2 valve when it was already closed.')
        else:
            GPIO.output(self.constructor.o2_pin, self.constructor.db['OFF'])
            self.toggle_o2 = 'off'


    def turn_o3_on(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.o3_pin) == self.constructor.db['ON']:
        #     print('Attempted to turn on the out pump when it was already turned on.')
        if self.toggle_o3 == 'on':
            print('Attempted to trun on the O3 generator when it was already on.')
        else:
            GPIO.output(self.constructor.o3_pin, self.constructor.db['ON'])
            self.toggle_o3 = 'on'
            self.start_o3_counter = time.time()
            self.start_o3_dest_counter = time.time()

    def turn_o3_off(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.o3_pin) == self.constructor.db['OFF']:
        #     print('Attempted to turn off the out pump when it was already turned off.')
        if self.toggle_o3 == 'off':
            print('Attempted to shutdown the O3 generator when it was already off.')
        else:
            GPIO.output(self.constructor.o3_pin, self.constructor.db['OFF'])
            self.toggle_o3 = 'off'
            if self.start_o3_counter != 0:
                self.stop_o3_counter = time.time()
                elapsed_time_min = ((self.stop_o3_counter - self.start_o3_counter) / 60)
                elapsed_time_min = round(elapsed_time_min, 1)
                self.constructor.db['o3_op_time'][0] += elapsed_time_min
                self.constructor.db['o3_dest_op_time'][0] += elapsed_time_min
                self.constructor.save_db()
                self.start_o3_counter = 0
                self.stop_o3_counter = 0


    def turn_uv_on(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.uv_pin) == self.constructor.db['ON']:
        #     print('Attempted to turn on the out pump when it was already turned on.')
        if self.toggle_uv == 'on':
            print('Attempted to open uv lamp when it was already open.')
        else:
            GPIO.output(self.constructor.uv_pin, self.constructor.db['ON'])
            self.toggle_uv = 'on'
            self.start_uv_counter = time.time()

    def turn_uv_off(self):
        # TODO : Replace the below 2 lines
        # if GPIO.input(self.constructor.uv_pin) == self.constructor.db['OFF']:
        #     print('Attempted to turn off the out pump when it was already turned off.')
        if self.toggle_uv == 'off':
            print('Attempted to close the uv lamp when it was already closed.')
        else:
            GPIO.output(self.constructor.uv_pin, self.constructor.db['OFF'])
            self.toggle_uv = 'off'
            if self.start_uv_counter != 0:
                self.stop_uv_counter = time.time()
                elapsed_time_min = ((self.stop_uv_counter - self.start_uv_counter) / 60)
                elapsed_time_min = round(elapsed_time_min, 1)
                self.constructor.db['uv_op_time'][0] += elapsed_time_min
                self.constructor.save_db()
                self.start_uv_counter = 0
                self.stop_uv_counter = 0