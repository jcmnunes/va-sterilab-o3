"""Automatic mode view module."""
import tkinter as tk
from helpers import colors
import math
import RPi.GPIO as GPIO
import time
import re
import graphics

graph = graphics.ImaAuto()


class AutoView:
    """Automatic mode view class."""

    def __init__(self, constructor, master, width=848, height=400):
        """Constructor."""
        # Variables
        self.constructor = constructor
        self.master = master
        self.width = width
        self.height = height
        self.imadir = 'imaauto'

        # Initiate the pop running flag. This flag is used to make
        # the ui more fluid by preventing the adcloop function from executing
        self.pop_running = False

        # Initiate a couple of strings to display upon entering auto mode
        self.LINFO_ISTRING = 'Welcome to automatic mode!'
        self.LINFO_KW_ISTRING = 'LOADING...'

        # Initiate some toggles to identify the state of the power relays
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

        # Constant holding the desired loading time before
        # running the first system check by using the inits_fn() [ms]
        self.LOADING_TIME = 2000

        # Constant holding the ADC loop time interval [ms]
        self.ADC_LOOP_TIME = 600

        # Feed level variables
        # Used for the interrupt algorithm in adcloop()
        self.feed_level_state = self.constructor.db['feed_level_state']

        # This list stores the last 4 values of feed_level_percent.
        # The idea is to switch the feed level state if these
        # four values are equal and different from the current state.
        # In this way, oscillation is prevented (at least minimized).
        self.feed_level_lst = self.constructor.db['feed_level_lst']

        # Proceed flags: Used in semi-auto mode when it is asked
        # to the user if he/she wants to proceed despite some undesired
        # state of the system
        self.proceed_id = 1
        self.proceed_1 = False
        self.proceed_2 = False

        # -- GUI LAYOUT -- #
        # Coordinates pumps canvas
        self.t = 10 * math.pi / 180

        self.x00_feedpmp, self.y00_feedpmp = 144, 230
        self.x10_feedpmp, self.y10_feedpmp = 174, 247
        self.x20_feedpmp, self.y20_feedpmp = 144, 265
        self.x0_feedpmp, self.y0_feedpmp = self.x00_feedpmp, self.y00_feedpmp
        self.x1_feedpmp, self.y1_feedpmp = self.x10_feedpmp, self.y10_feedpmp
        self.x2_feedpmp, self.y2_feedpmp = self.x20_feedpmp, self.y20_feedpmp
        self.feedpmp_center = 154, 247

        self.x00_recirpmp, self.y00_recirpmp = 248, 15
        self.x10_recirpmp, self.y10_recirpmp = 278, 32
        self.x20_recirpmp, self.y20_recirpmp = 248, 49
        self.x0_recirpmp = self.x00_recirpmp
        self.y0_recirpmp = self.y00_recirpmp
        self.x1_recirpmp = self.x10_recirpmp
        self.y1_recirpmp = self.y10_recirpmp
        self.x2_recirpmp = self.x20_recirpmp
        self.y2_recirpmp = self.y20_recirpmp
        self.recirpmp_center = 258, 32

        self.x00_outpmp, self.y00_outpmp = 352, 230
        self.x10_outpmp, self.y10_outpmp = 382, 247
        self.x20_outpmp, self.y20_outpmp = 352, 265
        self.x0_outpmp, self.y0_outpmp = self.x00_outpmp, self.y00_outpmp
        self.x1_outpmp, self.y1_outpmp = self.x10_outpmp, self.y10_outpmp
        self.x2_outpmp, self.y2_outpmp = self.x20_outpmp, self.y20_outpmp
        self.outpmp_center = 362, 247

        # PhotoImage instances
        self.ima_bg = tk.PhotoImage(master=self.master, data=graph.bg)
        self.ima_feedpmp_off = tk.PhotoImage(
            master=self.master,
            data=graph.feedpmp_off
        )
        self.ima_feedpmp_on = tk.PhotoImage(
            master=self.master,
            data=graph.feedpmp_on
        )
        self.ima_feedtk = tk.PhotoImage(master=self.master, data=graph.feedtk)
        self.ima_o2_off = tk.PhotoImage(master=self.master, data=graph.o2_off)
        self.ima_o2_on = tk.PhotoImage(master=self.master, data=graph.o2_on)
        self.ima_o3_off = tk.PhotoImage(master=self.master, data=graph.o3_off)
        self.ima_o3_on = tk.PhotoImage(master=self.master, data=graph.o3_on)
        self.ima_outpmp_off = tk.PhotoImage(
            master=self.master,
            data=graph.outpmp_off
        )
        self.ima_outpmp_on = tk.PhotoImage(
            master=self.master,
            data=graph.outpmp_on
        )
        self.ima_reactor00 = tk.PhotoImage(
            master=self.master,
            data=graph.reactor00
        )
        self.ima_reactor01 = tk.PhotoImage(
            master=self.master,
            data=graph.reactor01
        )
        self.ima_reactor10 = tk.PhotoImage(
            master=self.master,
            data=graph.reactor10
        )
        self.ima_reactor11 = tk.PhotoImage(
            master=self.master,
            data=graph.reactor11
        )
        self.ima_recirpmp_off = tk.PhotoImage(
            master=self.master,
            data=graph.recirpmp_off
        )
        self.ima_recirpmp_on = tk.PhotoImage(
            master=self.master,
            data=graph.recirpmp_on
        )
        self.ima_shut = tk.PhotoImage(master=self.master, data=graph.shut)
        self.ima_shut_push = tk.PhotoImage(
            master=self.master,
            data=graph.shut_push
        )
        self.ima_uv_off = tk.PhotoImage(master=self.master, data=graph.uv_off)
        self.ima_uv_on = tk.PhotoImage(master=self.master, data=graph.uv_on)
        self.ima_feed0 = tk.PhotoImage(
            master=self.master,
            data=graph.ima_feed0
        )
        self.ima_feed1 = tk.PhotoImage(
            master=self.master,
            data=graph.ima_feed1
        )
        self.ima_o2_recir00 = tk.PhotoImage(
            master=self.master,
            data=graph.ima_o2_recir00
        )
        self.ima_o2_recir01 = tk.PhotoImage(
            master=self.master,
            data=graph.ima_o2_recir01
        )
        self.ima_o2_recir10 = tk.PhotoImage(
            master=self.master,
            data=graph.ima_o2_recir10
        )
        self.ima_o2_recir11 = tk.PhotoImage(
            master=self.master,
            data=graph.ima_o2_recir11
        )
        self.ima_o30 = tk.PhotoImage(master=self.master, data=graph.ima_o30)
        self.ima_o31 = tk.PhotoImage(master=self.master, data=graph.ima_o31)
        self.ima_out0 = tk.PhotoImage(master=self.master, data=graph.ima_out0)
        self.ima_out1 = tk.PhotoImage(master=self.master, data=graph.ima_out1)
        self.ima_uv0 = tk.PhotoImage(master=self.master, data=graph.ima_uv0)
        self.ima_uv1 = tk.PhotoImage(master=self.master, data=graph.ima_uv1)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_feedpmp = tk.Label(
            self.master,
            image=self.ima_feedpmp_off,
            bd=0
        )
        self.lbl_feedtk = tk.Label(self.master, image=self.ima_feedtk, bd=0)
        self.lbl_o2 = tk.Label(self.master, image=self.ima_o2_off, bd=0)
        self.lbl_o3 = tk.Label(self.master, image=self.ima_o3_off, bd=0)
        self.lbl_outpmp = tk.Label(
            self.master,
            image=self.ima_outpmp_off,
            bd=0
        )
        self.lbl_reactor = tk.Label(
            self.master,
            image=self.ima_reactor00,
            bd=0
        )
        self.lbl_recirpmp = tk.Label(
            self.master,
            image=self.ima_recirpmp_off,
            bd=0
        )
        self.lbl_uv = tk.Label(self.master, image=self.ima_uv_off, bd=0)
        self.lbl_shut = tk.Label(self.master, image=self.ima_shut, bd=0)
        self.lbl_level_percent = tk.Label(
            self.master,
            text='',
            bg='white',
            bd=0,
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )

        # Info textbox
        self.finfo = tk.Frame(self.master, width=300, height=90)
        self.finfo.pack_propagate(0)  # Don't shrink
        self.finfo.place(x=44, y=247)
        self.linfo = tk.Message(
            self.finfo,
            bg='white',
            text=self.LINFO_ISTRING,
            bd=0,
            fg=colors.FG_COLOR,
            anchor=tk.N,
            font=('Roboto', 12),
            justify=tk.CENTER,
            width=250
        )
        self.linfo.pack(fill=tk.BOTH, expand=1)
        self.finfo_kw = tk.Frame(self.master, width=300, height=30)
        self.finfo_kw.pack_propagate(0)  # Don't shrink
        self.finfo_kw.place(x=44, y=217)
        self.linfo_kw = tk.Label(
            self.finfo_kw,
            bg='white',
            text=self.LINFO_KW_ISTRING,
            bd=0,
            fg=colors.FG_COLOR,
            anchor=tk.S,
            font=('Roboto', 12, 'bold')
        )
        self.linfo_kw.pack(fill=tk.BOTH, expand=1)
        self.finfo_lblbtn = tk.Frame(
            self.master,
            width=300,
            height=40,
            bg='white'
        )
        self.finfo_lblbtn.pack_propagate(0)  # Don't shrink
        self.finfo_lblbtn.place(x=44, y=337)
        self.btn_start_steri = tk.Label(
            self.finfo_lblbtn,
            text='START STERI.',
            fg='white',
            bg=colors.LIGHT_BLUE_COLOR,
            font=('Roboto', 11)
        )
        self.btn_start_steri.pack(ipady=5, ipadx=5, pady=3)
        self.btn_start_steri.pack_forget()
        self.btn_proceed = tk.Label(
            self.finfo_lblbtn,
            text='PROCEED',
            fg='white',
            bg=colors.LIGHT_BLUE_COLOR,
            font=('Roboto', 11)
        )
        self.btn_proceed.pack(ipady=5, ipadx=5, pady=3)
        self.btn_proceed.pack_forget()

        # Canvas
        self.canvas_feedlevel_x = 12
        self.canvas_feedlevel_y = 151
        self.canvas_feedlevel_w = 76
        self.canvas_feedlevel_h = 117

        self.canvas_reactor_min_x = 266
        self.canvas_reactor_min_y = 200
        self.canvas_reactor_min_w = 14
        self.canvas_reactor_min_h = 14

        self.canvas_reactor_max_x = 266
        self.canvas_reactor_max_y = 126
        self.canvas_reactor_max_w = 14
        self.canvas_reactor_max_h = 14

        self.w = tk.Canvas(
            self.master,
            width=412,
            height=280,
            bg=colors.BG_COLOR,
            highlightthickness=0
        )
        self.w.place(x=392, y=102)

        self.canvas_out = self.w.create_image(
            295,
            0,
            image=self.ima_out0,
            anchor=tk.NW
        )
        self.canvas_uv = self.w.create_image(
            341,
            10,
            image=self.ima_uv0,
            anchor=tk.NW
        )
        self.canvas_o2_recir = self.w.create_image(
            0,
            0,
            image=self.ima_o2_recir00,
            anchor=tk.NW
        )
        self.canvas_feed = self.w.create_image(
            0,
            210,
            image=self.ima_feed0,
            anchor=tk.NW
        )
        self.canvas_o3 = self.w.create_image(
            130,
            10,
            image=self.ima_o30,
            anchor=tk.NW
        )

        self.feedpmp = self.w.create_polygon(
            self.x0_feedpmp, self.y0_feedpmp,
            self.x1_feedpmp, self.y1_feedpmp,
            self.x2_feedpmp, self.y2_feedpmp,
            width=3,
            fill=colors.BG_COLOR,
            outline=colors.FG_COLOR,
            tags=('filling_poly', )
        )

        self.recirpmp = self.w.create_polygon(
            self.x0_recirpmp,
            self.y0_recirpmp,
            self.x1_recirpmp,
            self.y1_recirpmp,
            self.x2_recirpmp,
            self.y2_recirpmp,
            width=3,
            fill=colors.BG_COLOR,
            outline=colors.FG_COLOR,
            tags=('recirpmp_poly', )
        )

        self.outpmp = self.w.create_polygon(
            self.x0_outpmp,
            self.y0_outpmp,
            self.x1_outpmp,
            self.y1_outpmp,
            self.x2_outpmp,
            self.y2_outpmp,
            width=3,
            fill=colors.BG_COLOR,
            outline=colors.FG_COLOR,
            tags='out_poly'
        )

        self.feedlevel = self.w.create_rectangle(
            self.canvas_feedlevel_x + 1,
            self.canvas_feedlevel_y + 1,
            self.canvas_feedlevel_x + self.canvas_feedlevel_w - 1,
            self.canvas_feedlevel_y + self.canvas_feedlevel_h - 1,
            width=2,
            fill=colors.GREEN_COLOR,
            outline=colors.GREEN_COLOR
        )

        self.reactorlevel_low = self.w.create_rectangle(
            self.canvas_reactor_min_x,
            self.canvas_reactor_min_y,
            self.canvas_reactor_max_x + self.canvas_reactor_min_w - 1,
            self.canvas_reactor_min_y + self.canvas_reactor_min_h - 1,
            width=1,
            fill=colors.GREEN_COLOR,
            outline=colors.GREEN_COLOR
        )

        self.reactorlevel_high = self.w.create_rectangle(
            self.canvas_reactor_max_x,
            self.canvas_reactor_max_y,
            self.canvas_reactor_max_x + self.canvas_reactor_max_w - 1,
            self.canvas_reactor_max_y + self.canvas_reactor_max_h - 1,
            width=1,
            fill=colors.GREEN_COLOR,
            outline=colors.GREEN_COLOR
        )

        # Place Labels
        self.lbl_bg.place(x=0, y=0)
        self.lbl_feedpmp.place(x=496, y=382)
        self.lbl_feedtk.place(x=392, y=382)
        self.lbl_o2.place(x=392, y=52)
        self.lbl_o3.place(x=496, y=52)
        self.lbl_outpmp.place(x=704, y=382)
        self.lbl_reactor.place(x=600, y=382)
        self.lbl_recirpmp.place(x=600, y=52)
        self.lbl_uv.place(x=704, y=52)
        self.lbl_shut.place(x=44, y=382)
        self.w.place(x=392, y=102)
        self.lbl_level_percent.place(x=452, y=408)

        # -- (END) GUI LAYOUT -- #

    # METHODS
    def inits(self):
        """
        Initialize function.

        This init function is called by the winhome auto button callback.
        It sets the interrupts for the reactor levels
        and starts the adcloop function.
        After some time (loading time), the control algorithm
        main function (init_fn) is called also
        """
        self.first_run = True
        self.iserror = False
        GPIO.add_event_detect(
            self.constructor.reactor_llow_pin,
            GPIO.BOTH,
            callback=self.l1_call,
            bouncetime=100
        )
        GPIO.add_event_detect(
            self.constructor.reactor_lhigh_pin,
            GPIO.BOTH,
            callback=self.l2_call,
            bouncetime=100
        )
        self.adcloop()
        self.master.after(self.LOADING_TIME, self.inits_fn)

        # Initiate the status flag. This flag is responsible for
        # identifying the current system status.
        # Possible states are:
        #   - idle (entered upon emptying stage completion)
        #   - steri (during sterilization stage)
        #   - filling (during the filling of the reactor)
        #   - emptying (during the reactor emptying stage)
        #   - error (may be optional) [the system is in an error state]
        # self.status_flag = 'idle'
        self.init_status_flag = self.constructor.db['status_flag']

    def adcloop(self):
        """
        ADC Loop.

        This method runs as a loop by using the .after method.
        Its main purpose is to read the buffer from the ADC converter.
        Additionally tasks are done such as updating the GUI and
        implementing an interrupt algorithm to respond to feed tk level
        changes.
        """
        # This check assures that the ADC loop only runs
        # when we are in the auto mode.
        if self.constructor.global_focus != 'auto':
            return
        # This check assures we only run the algorithm when there is
        # no pop-up transition happening. This is to smooth out the
        # pop transition (purely a cosmetic aspect).
        if not self.pop_running:
            # Get the string from ADC using a queue
            self.text = self.constructor.queue.get()
            # Notify queue the string was received
            self.constructor.queue.task_done()
            # Split the result using some keywords.
            result = re.search('temp(.*)photo(.*)', self.text)
            # Pass the extracted information to object variables
            self.feed_level_arduino = int(result.group(1))

            # Adjust etape reading values
            if self.feed_level_arduino > self.constructor.etape_max:
                self.feed_level_arduino = self.constructor.etape_max
            if self.feed_level_arduino < self.constructor.etape_min:
                self.feed_level_arduino = self.constructor.etape_min

            # Convert the reading from eTape to canvas coordinates
            # for displaying feed tk level
            self.canvas_feedlevel_yduino = int(
                (self.feed_level_arduino - self.constructor.etape_min) *
                (-self.canvas_feedlevel_h /
                    (self.constructor.etape_max - self.constructor.etape_min))
                + self.canvas_feedlevel_y + self.canvas_feedlevel_h
            )

            self.w.coords(
                self.feedlevel,
                self.canvas_feedlevel_x + 1,
                self.canvas_feedlevel_yduino,
                self.canvas_feedlevel_x + self.canvas_feedlevel_w - 1,
                self.canvas_feedlevel_y + self.canvas_feedlevel_h - 1
            )

            # Convert reading from eTape to a percent value
            # and display on label
            self.level_percent = int(
                self.feed_level_arduino / self.constructor.etape_max * 100
            )
            self.lbl_level_percent['text'] = '{0} %'.format(self.level_percent)

            # Update feed_level_lst to detect interrupts
            self.feed_level_lst.pop(0)  # Pop the first value from the list
            # Append the new value
            self.feed_level_lst.append(self.level_percent)

            # Developing the interrupt algorithm. The algorithm has 2 steps:
            # 1. Check to see if all values in the list are in the same group
            # 2. Check if the previous state is different from the new state

            # If all values are larger than the high high level alarm
            if all(
                ii > (
                    100 - self.constructor.db['feed_tk_level_params'][4]
                ) for ii in self.feed_level_lst
            ):
                if self.constructor.db['feed_level_state'] != 'highhigh':
                    self.constructor.db['feed_level_state'] = 'highhigh'
                    self.constructor.save_db()
                    self.inits_fn()

            # If all values are larger than the high level alarm
            elif all((
                ii > self.constructor.db['feed_tk_level_params'][3]
            ) for ii in self.feed_level_lst):
                if self.constructor.db['feed_level_state'] != 'high':
                    self.constructor.db['feed_level_state'] = 'high'
                    self.constructor.save_db()
                    self.inits_fn()

            # If all values are lower than the low low level alarm
            elif all((
                ii < self.constructor.db['feed_tk_level_params'][4]
            ) for ii in self.feed_level_lst):
                if self.constructor.db['feed_level_state'] != 'lowlow':
                    self.constructor.db['feed_level_state'] = 'lowlow'
                    self.constructor.save_db()
                    self.inits_fn()

            # If all values are lower than the low level alarm
            elif all((
                ii < self.constructor.db['feed_tk_level_params'][2]
            ) for ii in self.feed_level_lst):
                if self.constructor.db['feed_level_state'] != 'low':
                    self.constructor.db['feed_level_state'] = 'low'
                    self.constructor.save_db()
                    self.inits_fn()

            # If all values are between the opt value and the high level alarm
            elif all((
                ii > self.constructor.db['opt_feedtk_level'][3]
            ) and (
                ii < self.constructor.db['feed_tk_level_params'][3]
            ) for ii in self.feed_level_lst):
                if self.constructor.db['feed_level_state'] != 'normal':
                    self.constructor.db['feed_level_state'] = 'normal'
                    self.constructor.save_db()
                    self.inits_fn()

            # If all values are between the low level and the opt level
            elif all((
                ii > self.constructor.db['feed_tk_level_params'][2]
            ) and (
                ii < self.constructor.db['opt_feedtk_level'][3]
            ) for ii in self.feed_level_lst):
                if self.constructor.db['feed_level_state'] != 'semilow':
                    self.constructor.db['feed_level_state'] = 'semilow'
                    self.constructor.save_db()
                    self.inits_fn()

            # -- UPDATE the GUI -- #

            if (
                self.level_percent
                > self.constructor.db['feed_tk_level_params'][3]
                or self.level_percent
                < self.constructor.db['feed_tk_level_params'][2]
            ):
                self.w.itemconfigure(
                    self.feedlevel,
                    fill=colors.RED_COLOR,
                    outline=colors.RED_COLOR
                )
                self.lbl_level_percent['fg'] = colors.RED_COLOR
            else:
                self.w.itemconfigure(
                    self.feedlevel,
                    fill=colors.GREEN_COLOR,
                    outline=colors.GREEN_COLOR
                )
                self.lbl_level_percent['fg'] = colors.GREEN_COLOR

            self.l1_open = GPIO.input(self.constructor.reactor_llow_pin)
            self.l2_open = GPIO.input(self.constructor.reactor_lhigh_pin)

            if self.l1_open:
                self.w.itemconfigure(
                    self.reactorlevel_low,
                    fill=colors.RED_COLOR,
                    outline=colors.RED_COLOR
                )
                if self.l2_open:
                    self.lbl_reactor['image'] = self.ima_reactor00
                else:
                    self.lbl_reactor['image'] = self.ima_reactor01
            else:
                self.w.itemconfigure(
                    self.reactorlevel_low,
                    fill=colors.GREEN_COLOR,
                    outline=colors.GREEN_COLOR
                )
                if self.l2_open:
                    self.lbl_reactor['image'] = self.ima_reactor10
                else:
                    self.lbl_reactor['image'] = self.ima_reactor11

            if self.l2_open:
                self.w.itemconfigure(
                    self.reactorlevel_high,
                    fill=colors.GREEN_COLOR,
                    outline=colors.GREEN_COLOR
                )
                if self.l1_open:
                    self.lbl_reactor['image'] = self.ima_reactor00
                else:
                    self.lbl_reactor['image'] = self.ima_reactor10
            else:
                self.w.itemconfigure(
                    self.reactorlevel_high,
                    fill=colors.RED_COLOR,
                    outline=colors.RED_COLOR
                )
                if self.l1_open:
                    self.lbl_reactor['image'] = self.ima_reactor01
                else:
                    self.lbl_reactor['image'] = self.ima_reactor11

        self.master.after(self.ADC_LOOP_TIME, self.adcloop)

    def inits_fn(self):
        """
        Control algorithm function.

        This method is responsible for all the automatic control
        """
        # If we are not on the auto panel screen
        if self.constructor.global_focus != 'auto':
            return

        # If the system is at error
        if self.iserror:
            return

        # Setting the levels states
        l1_open = GPIO.input(self.constructor.reactor_llow_pin)
        l2_open = GPIO.input(self.constructor.reactor_lhigh_pin)
        lfeed = self.level_percent

        # -- IDLE -- #
        # If status is IDLE - Idle state is entered upon
        # emptying stage completion
        if self.constructor.db['status_flag'] == 'idle':

            # First, test the lfeed value (a percent value).
            # If the value is not good return from the function
            # and issue an error message (TODO: This may not be needed)
            if lfeed < 0 or lfeed > 100:
                lbl = 'ERROR-101'
                txt = (
                    'The feed tank level sensor may' +
                    ' not be working properly. Cannot proceed.'
                )
                self.etape_error(lbl, txt)

            # If feed tank has a low low alarm
            elif lfeed <= self.constructor.db['feed_tk_level_params'][4]:

                # If the reactor is empty (NORMAL CONDITION)
                if l1_open and l2_open:
                    lbl = 'WARNING-101'
                    txt = (
                        'Feed tank has an unexpected low-low level alarm.' +
                        ' Waiting for level to start sterilization.'
                    )
                    self.update_info_box(lbl, txt)
                    self._hide_transient_buttons()

                # Reactor is not empty
                elif not l1_open and l2_open:
                    # If semi-auto mode is enabled
                    if self.constructor.db['enable_semi_auto'][1]:
                        if self.proceed_1:
                            self._hide_transient_buttons()
                            lbl = 'WARNING-102'
                            txt = (
                                'Attempted to start filling reactor. ' +
                                'Feed tank has a low-low level alarm. ' +
                                'Reactor should be empty. ' +
                                'User chose to proceed.'
                            )
                            self.update_info_box(lbl, txt)
                            self._hide_transient_buttons()
                        else:
                            self._hide_transient_buttons()
                            lbl = 'WARNING-102'
                            txt = (
                                'Attempted to start filling reactor. ' +
                                'Feed tank has a low-low level alarm. ' +
                                'Reactor should be empty. Proceed anyway?'
                            )
                            self.update_info_box(lbl, txt)
                            self.proceed_id = 1
                            self._show_proceed_button()
                    # If semi-auto mode is disabled
                    else:
                        lbl = 'ERROR-102'
                        self.idle_rx_not_empty(lbl)

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-103'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    lbl1 = 'WARNING-103'
                    lbl2 = 'ERROR-104'
                    self.idle_rx_full(lbl1, lbl2)

            # If feed tank has a low alarm
            elif lfeed <= self.constructor.db['feed_tk_level_params'][2]:
                self._hide_transient_buttons()

                # If the reactor is empty (NORMAL CONDITION)
                if l1_open and l2_open:
                    lbl = 'WARNING-104'
                    txt = (
                        'Feed tank has a low level alarm. ' +
                        'Waiting for level to start sterilization.'
                    )
                    self.update_info_box(lbl, txt)

                # Reactor is not empty
                elif not l1_open and l2_open:
                    # If semi-auto mode is enabled
                    if self.constructor.db['enable_semi_auto'][1]:
                        if self.proceed_2:
                            lbl = 'WARNING-105'
                            txt = (
                                'Attempted to start filling reactor. ' +
                                'Feed tank has a low level alarm. ' +
                                'Reactor should be empty. ' +
                                'User chose to proceed.'
                            )
                            self.update_info_box(lbl, txt)
                        else:
                            lbl = 'WARNING-105'
                            txt = (
                                'Attempted to start filling reactor. ' +
                                'Feed tank has a low level alarm. ' +
                                'Reactor should be empty. ' +
                                'Proceed anyway?'
                            )
                            self.update_info_box(lbl, txt)
                            self.proceed_id = 2
                            self._show_proceed_button()
                    # If semi-auto mode is disabled
                    else:
                        lbl = 'ERROR-105'
                        self.idle_rx_not_empty(lbl)

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-106'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    lbl1 = 'WARNING-106'
                    lbl2 = 'ERROR-107'
                    self.idle_rx_full(lbl1, lbl2)

            # If feed tank level is between llow and lopt
            elif (
                lfeed > self.constructor.db['feed_tk_level_params'][2]
                and lfeed <= self.constructor.db['opt_feedtk_level'][3]
            ):
                self._hide_transient_buttons()

                # If the reactor is empty (NORMAL CONDITION)
                if l1_open and l2_open:
                    lbl = 'NOTE'
                    txt = (
                        'Not enough level in the feed tank to ' +
                        'start sterilization. ' +
                        'Minimum level is defined as {0:.1f}%. ' +
                        'Waiting for level to start sterilization.'
                    ).format(self.constructor.db['opt_feedtk_level'][3])
                    self.update_info_box(lbl, txt)
                    self._hide_transient_buttons()

                # Reactor is not empty
                elif not l1_open and l2_open:
                    # If semi-auto mode is enabled
                    if self.constructor.db['enable_semi_auto'][1]:
                        lbl = 'WARNING-107'
                        txt = (
                            'The feed tank level is less than the ' +
                            'defined minimum level ({0:.1f}%). ' +
                            'The reactor is not empty. ' +
                            'Proceed to sterilization anyway?'
                        ).format(self.constructor.db['opt_feedtk_level'][3])
                        self.update_info_box(lbl, txt)
                        self._show_steri_button()
                    # If semi-auto mode is disabled
                    else:
                        lbl = 'ERROR-108'
                        self.idle_rx_not_empty(lbl)

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-109'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    print('I am in error-110')
                    lbl1 = 'WARNING-108'
                    lbl2 = 'ERROR-110'
                    self.idle_rx_full(lbl1, lbl2)

            # If feed level is between lopt and lhigh (NORMAL CONDITION):
            elif (
                lfeed > self.constructor.db['opt_feedtk_level'][3]
                and lfeed <= self.constructor.db['feed_tk_level_params'][3]
            ):
                self._hide_transient_buttons()

                # If the reactor is empty (NORMAL CONDITION)
                if l1_open and l2_open:
                    lbl = 'NOTE'
                    txt = (
                        'Filling reactor. Sterilization will start ' +
                        'after filling. Please do not power-off.'
                    )
                    self.update_info_box(lbl, txt)
                    # GPIO
                    self.turn_feedpmp_on()
                    self.constructor.db['status_flag'] = 'filling'
                    self.constructor.save_db()

                # Reactor is not empty
                elif not l1_open and l2_open:
                    # If semi-auto mode is enabled
                    if self.constructor.db['enable_semi_auto'][1]:
                        lbl = 'WARNING-109'
                        txt = (
                            'Attempted to start filling reactor. ' +
                            'The reactor is not empty as it should be. ' +
                            'Proceed to sterilization anyway?'
                        )
                        self.update_info_box(lbl, txt)
                        # TODO: Proceed btn callback
                        self._show_steri_button()
                    # If semi-auto mode is disabled
                    else:
                        lbl = 'ERROR-111'
                        self.idle_rx_not_empty(lbl)

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-112'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    lbl1 = 'WARNING-110'
                    lbl2 = 'ERROR-113'
                    self.idle_rx_full(lbl1, lbl2)

            # If feedtk has an high-high alarm
            elif lfeed >= 100 - self.constructor.db['feed_tk_level_params'][4]:
                self._hide_transient_buttons()

                lbl = 'ERROR-114'
                txt = (
                    'Feed tank has a high-high level alarm. ' +
                    'Cannot proceed. Please make sure no more ' +
                    'liquid enters the machine.'
                )
                self.update_info_box(lbl, txt)
                self.error_procedure()

            # If feedtk has an high alarm
            elif lfeed > self.constructor.db['feed_tk_level_params'][3]:
                self._hide_transient_buttons()

                # If the reactor is empty (NORMAL CONDITION)
                if l1_open and l2_open:
                    lbl = 'WARNING-111'
                    txt = (
                        'The feed tank has a high level alarm. ' +
                        'The feed flowrate to the machine may be too high. ' +
                        'Starting filling reactor.'
                    )
                    self.update_info_box(lbl, txt)
                    # GPIO
                    self.turn_feedpmp_on()
                    self.constructor.db['status_flag'] = 'filling'
                    self.constructor.save_db()

                # Reactor is not empty
                elif not l1_open and l2_open:
                    # If semi-auto mode is enabled
                    if self.constructor.db['enable_semi_auto'][1]:
                        lbl = 'WARNING-112'
                        txt = (
                            'Attempted to start filling reactor. ' +
                            'The reactor is not empty. ' +
                            'Feed tank has a high level alarm. ' +
                            'Do you want to proceed anyway?'
                        )
                        self.update_info_box(lbl, txt)
                        self._show_proceed_button()
                    # If semi-auto mode is disabled
                    else:
                        lbl = 'ERROR-113'
                        self.idle_rx_not_empty(lbl)

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-114'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    lbl1 = 'WARNING-113'
                    lbl2 = 'ERROR-115'
                    self.idle_rx_full(lbl1, lbl2)

        # If status is FILLING
        elif self.constructor.db['status_flag'] == 'filling':

            # First, test the lfeed value (a percent value).
            # If the value is not good return from the function
            # and issue an error message
            if lfeed < 0 or lfeed > 100:
                lbl = 'ERROR-200'
                txt = (
                    'The feed tank level sensor may not be ' +
                    'working properly. Cannot proceed.'
                )
                self.etape_error(lbl, txt)

            # If feed tank has a low low alarm
            elif lfeed <= self.constructor.db['feed_tk_level_params'][4]:
                self._hide_transient_buttons()
                lbl = 'ERROR-201'
                txt = (
                    'Unexpected system state detected. ' +
                    'Feed tank has a low-low level alarm. Cannot proceed.'
                )
                self.update_info_box(lbl, txt)
                self.error_procedure()

            # If feed tank has a low alarm (NORMAL - stop filling)
            elif lfeed <= self.constructor.db['feed_tk_level_params'][2]:
                self._hide_transient_buttons()

                # The reactor is empty - At this stage the reactor
                # and the feed tk should not be both empty
                if l1_open and l2_open:
                    lbl = 'ERROR-202'
                    txt = (
                        'Unexpected system state detected. ' +
                        'Please check for leakages. Cannot continue.'
                    )
                    self.update_info_box(lbl, txt)
                    self.error_procedure()

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    self.steri_procedure()
                    self.turn_feedpmp_off()

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-203'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                # TODO: Semi-auto mode??
                elif not l1_open and not l2_open:
                    lbl1 = 'WARNING-201'
                    lbl2 = 'ERROR-204'
                    self.filling_rx_full(lbl1, lbl2)

            # If feed tank level is between llow and lopt
            elif (
                lfeed > self.constructor.db['feed_tk_level_params'][2]
                and lfeed <= self.constructor.db['opt_feedtk_level'][3]
            ):
                self._hide_transient_buttons()

                # The reactor is empty
                if l1_open and l2_open:
                    if self.first_run:
                        lbl = 'NOTE'
                        txt = (
                            'Filling reactor. Sterilization will ' +
                            'start after filling. Please do not power-off.'
                        )
                        self.update_info_box(lbl, txt)
                        # GPIO
                        self.turn_feedpmp_on()
                        # self.constructor.save_db()
                        # self.constructor.update_db()
                    else:
                        lbl = 'NOTE'
                        txt = (
                            'Filling reactor. Sterilization will ' +
                            'start after filling. Please do not power-off.'
                        )
                        self.update_info_box(lbl, txt)

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    if self.first_run:
                        lbl = 'NOTE'
                        txt = (
                            'Filling reactor. Sterilization will ' +
                            'start after filling. Please do not power-off.'
                        )
                        self.update_info_box(lbl, txt)
                        # GPIO
                        self.turn_feedpmp_on()
                    else:
                        lbl = 'NOTE'
                        txt = (
                            'Filling reactor. Sterilization will start ' +
                            'after filling. Please do not power-off.'
                        )
                        self.update_info_box(lbl, txt)

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-205'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    lbl1 = 'WARNING-202'
                    lbl2 = 'ERROR-206'
                    self.filling_rx_full(lbl1, lbl2)

            # If feed level is between lopt and lhigh:
            elif (
                lfeed > self.constructor.db['opt_feedtk_level'][3]
                and lfeed <= self.constructor.db['feed_tk_level_params'][3]
            ):
                self._hide_transient_buttons()

                # The reactor is empty
                if l1_open and l2_open:
                    if self.first_run:
                        lbl = 'NOTE'
                        txt = (
                            'Filling reactor. Sterilization will ' +
                            'start after filling. Please do not power-off.'
                        )
                        self.update_info_box(lbl, txt)
                        # GPIO
                        self.turn_feedpmp_on()
                        # self.constructor.save_db()
                        # self.constructor.update_db()
                    else:
                        lbl = 'NOTE'
                        txt = (
                            'Filling reactor. Sterilization will ' +
                            'start after filling. Please do not power-off.'
                        )
                        self.update_info_box(lbl, txt)

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    if self.first_run:
                        lbl = 'NOTE'
                        txt = (
                            'Filling reactor. Sterilization will ' +
                            'start after filling. Please do not power-off.'
                        )
                        self.update_info_box(lbl, txt)
                        # GPIO
                        self.turn_feedpmp_on()
                    else:
                        lbl = 'NOTE'
                        txt = (
                            'Filling reactor. Sterilization will ' +
                            'start after filling. Please do not power-off.'
                        )
                        self.update_info_box(lbl, txt)

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-207'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    lbl1 = 'WARNING-203'
                    lbl2 = 'ERROR-208'
                    self.filling_rx_full(lbl1, lbl2)

            # If feedtk has an high-high alarm
            elif lfeed >= (
                100 - self.constructor.db['feed_tk_level_params'][4]
            ):
                self._hide_transient_buttons()
                lbl = 'ERROR-209'
                txt = (
                    'Feed tank has a high-high level alarm. ' +
                    'Cannot proceed. Please make sure no more ' +
                    'liquid enters the machine.'
                )
                self.update_info_box(lbl, txt)
                self.error_procedure()

            # If feedtk has a high level alarm
            elif lfeed > self.constructor.db['feed_tk_level_params'][3]:
                self._hide_transient_buttons()

                # The reactor is empty
                if l1_open and l2_open:
                    if self.first_run:
                        lbl = 'WARNING-204'
                        txt = (
                            'Feed tank has a high level alarm. ' +
                            'The feed flowrate to the machine may be too high.'
                        )
                        self.update_info_box(lbl, txt)
                        # GPIO
                        self.turn_feedpmp_on()
                        # self.constructor.save_db()
                        # self.constructor.update_db()
                    else:
                        lbl = 'WARNING-204.1'
                        txt = (
                            'Feed tank has a high level alarm. ' +
                            'The feed flowrate to the machine may be too high.'
                        )
                        self.update_info_box(lbl, txt)

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    if self.first_run:
                        lbl = 'WARNING-205'
                        txt = (
                            'Feed tank has a high level alarm. ' +
                            'The feed flowrate to the machine may be too high.'
                        )
                        self.update_info_box(lbl, txt)
                        # GPIO
                        self.turn_feedpmp_on()
                        self.constructor.save_db()
                        self.constructor.update_db()
                    else:
                        lbl = 'WARNING-205.1'
                        txt = (
                            'Feed tank has a high level alarm. ' +
                            'The feed flowrate to the machine may be too high.'
                        )
                        self.update_info_box(lbl, txt)

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-210'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    # self.clean_GPIO()
                    lbl1 = 'WARNING-206'
                    lbl2 = 'ERROR-211'
                    self.filling_rx_full(lbl1, lbl2)

        # If status is STERI
        elif self.constructor.db['status_flag'] == 'steri':

            # First, test the lfeed value (a percent value).
            # If the value is not good return from the function
            # and issue an error message
            # TODO: Deal with errors
            if lfeed < 0 or lfeed > 100:
                lbl = 'ERROR-300'
                txt = (
                    'The feed tank level sensor may not ' +
                    'be working properly. Cannot proceed.'
                )
                self.etape_error(lbl, txt)

            # If feed tank has a low low alarm
            # TODO: This condition may cause problems
            elif lfeed <= self.constructor.db['feed_tk_level_params'][4]:
                self._hide_transient_buttons()
                lbl = 'ERROR-301'
                txt = (
                    'Unexpected system state detected. ' +
                    'Feed tank has a low-low level alarm. Cannot proceed.'
                )
                self.update_info_box(lbl, txt)
                self.error_procedure()

            # If feed tank has a low alarm
            elif lfeed <= self.constructor.db['feed_tk_level_params'][2]:
                self._hide_transient_buttons()

                # The reactor is empty
                if l1_open and l2_open:
                    lbl = 'ERROR-302'
                    txt = (
                        'Unexpected system state detected. ' +
                        'Reactor seems to be empty. Cannot continue.'
                    )
                    self.update_info_box(lbl, txt)
                    self.error_procedure()

                # # Reactor is not empty (NORMAL CONDITION)
                if not l1_open and l2_open:
                    pass

                # # Reactor has no low level but has a high level (IMPOSSIBLE)
                if l1_open and not l2_open:
                    lbl = 'ERROR-303'
                    self.rx_levels_error(lbl)

                # # Reactor is full with a high level alarm
                if not l1_open and not l2_open:
                    self.clean_GPIO()
                    lbl1 = 'WARNING-301'
                    lbl2 = 'ERROR-304'
                    self.steri_rx_full(lbl1, lbl2)

            # If feed tank level is between llow and lopt
            elif (
                lfeed > self.constructor.db['feed_tk_level_params'][2]
                and lfeed <= self.constructor.db['opt_feedtk_level'][3]
            ):
                self._hide_transient_buttons()

                # The reactor is empty - May indicate leakage
                if l1_open and l2_open:
                    lbl = 'ERROR-305'
                    txt = (
                        'Unexpected system state detected. ' +
                        'Reactor seems to be empty. Cannot continue.'
                    )
                    self.update_info_box(lbl, txt)
                    self.error_procedure()

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    # Letting the steri cycle handle the control
                    pass

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-306'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    self.clean_GPIO()
                    lbl1 = 'WARNING-301'
                    lbl2 = 'ERROR-304'
                    self.steri_rx_full(lbl1, lbl2)

            # If feed level is between lopt and lhigh:
            elif (
                lfeed > self.constructor.db['opt_feedtk_level'][3]
                and lfeed <= self.constructor.db['feed_tk_level_params'][3]
            ):
                self._hide_transient_buttons()

                # The reactor is empty - May indicate leakage - Give warning
                if l1_open and l2_open:
                    lbl = 'ERROR-305'
                    txt = (
                        'Unexpected system state detected. ' +
                        'Reactor seems to be empty. Cannot continue.'
                    )
                    self.update_info_box(lbl, txt)
                    self.error_procedure()

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    pass

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-306'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    self.clean_GPIO()
                    lbl1 = 'WARNING-302'
                    lbl2 = 'ERROR-307'
                    self.steri_rx_full(lbl1, lbl2)

            # If feedtk has an high-high alarm
            elif lfeed >= 100 - self.constructor.db['feed_tk_level_params'][4]:
                self._hide_transient_buttons()
                lbl = 'ERROR-308'
                txt = (
                    'Feed tank has a high-high level alarm. ' +
                    'Cannot proceed. Please make sure no more ' +
                    'liquid enters the machine.'
                )
                self.update_info_box(lbl, txt)
                self.error_procedure()

            # If feedtk has a high level alarm
            elif lfeed > self.constructor.db['feed_tk_level_params'][3]:
                self._hide_transient_buttons()

                # The reactor is empty - May indicate leakage
                if l1_open and l2_open:
                    lbl = 'ERROR-309'
                    txt = (
                        'Unexpected system state detected. ' +
                        'Reactor seems to be empty. Cannot continue.'
                    )
                    self.update_info_box(lbl, txt)
                    self.error_procedure()

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    lbl = 'WARNING-303'
                    txt = (
                        'Feed tank has a high level alarm. ' +
                        'The feed flowrate to the machine may be too high.'
                    )
                    self.update_info_box(lbl, txt)

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-310'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    self.clean_GPIO()
                    lbl1 = 'WARNING-304'
                    lbl2 = 'ERROR-311'
                    self.steri_rx_full(lbl1, lbl2)

        # If status is EMPTYING
        elif self.constructor.db['status_flag'] == 'emptying':

            # First, test the lfeed value (a percent value).
            # If the value is not goo from the function
            # and issue an error message
            if lfeed < 0 or lfeed > 100:
                lbl = 'ERROR-400'
                txt = (
                    'The feed tank level sensor may not be ' +
                    'working properly. Cannot proceed.'
                )
                self.etape_error(lbl, txt)

            # If feed tank has a low low alarm
            elif lfeed <= self.constructor.db['feed_tk_level_params'][4]:
                self._hide_transient_buttons()
                lbl = 'ERROR-401'
                txt = (
                    'Unexpected system state detected. ' +
                    'Feed tank has a low-low level alarm. Cannot proceed.'
                )
                self.update_info_box(lbl, txt)
                self.error_procedure()

            # If feed tank has a low alarm
            elif lfeed <= self.constructor.db['feed_tk_level_params'][2]:
                self._hide_transient_buttons()

                # The reactor is empty - Finish emptying stage
                if l1_open and l2_open:
                    self.constructor.db['status_flag'] = 'idle'
                    self.clean_GPIO()
                    # Run itself to see if we have enough liquid
                    # volume in feedtk to start over
                    self.inits_fn()

                # # Reactor is not empty (NORMAL CONDITION)
                if not l1_open and l2_open:
                    lbl = 'NOTE'
                    txt = (
                        'Sterilization completed. Emptying reactor. ' +
                        'Please do not power-off.'
                    )
                    self.update_info_box(lbl, txt)
                    # GPIO
                    self.turn_outpmp_on()
                    self.turn_uv_on()

                # # Reactor has no low level but has a high level (IMPOSSIBLE)
                if l1_open and not l2_open:
                    lbl = 'ERROR-402'
                    self.rx_levels_error(lbl)

                # # Reactor is full with a high level alarm
                if not l1_open and not l2_open:
                    self.clean_GPIO()
                    lbl1 = 'WARNING-401'
                    lbl2 = 'ERROR-403'
                    self.emptying_rx_full(lbl1, lbl2)

            # If feed tank level is between llow and lopt
            elif (
                lfeed > self.constructor.db['feed_tk_level_params'][2]
                and lfeed <= self.constructor.db['opt_feedtk_level'][3]
            ):
                self._hide_transient_buttons()

                # The reactor is empty - Finish emptying stage
                if l1_open and l2_open:
                    self.constructor.db['status_flag'] = 'idle'
                    self.clean_GPIO()
                    self.inits_fn()

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    lbl = 'NOTE'
                    txt = (
                        'Sterilization completed. Emptying reactor. ' +
                        'Please do not power-off.'
                    )
                    self.update_info_box(lbl, txt)
                    # GPIO
                    self.turn_outpmp_on()
                    self.turn_uv_on()

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-404'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    self.clean_GPIO()
                    lbl1 = 'WARNING-402'
                    lbl2 = 'ERROR-405'
                    self.emptying_rx_full(lbl1, lbl2)

            # If feed level is between lopt and lhigh:
            elif (
                lfeed > self.constructor.db['opt_feedtk_level'][3]
                and lfeed <= self.constructor.db['feed_tk_level_params'][3]
            ):
                self._hide_transient_buttons()

                # The reactor is empty - Finish emptying stage
                if l1_open and l2_open:
                    self.constructor.db['status_flag'] = 'idle'
                    self.clean_GPIO()
                    self.inits_fn()

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    pass

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-406'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    self.clean_GPIO()
                    lbl1 = 'WARNING-403'
                    lbl2 = 'ERROR-407'
                    self.emptying_rx_full(lbl1, lbl2)

            # If feedtk has an high-high alarm
            elif lfeed >= 100 - self.constructor.db['feed_tk_level_params'][4]:
                self._hide_transient_buttons()
                lbl = 'ERROR-408'
                txt = (
                    'Feed tank has a high-high level alarm. ' +
                    'Cannot proceed. Please make sure no more liquid ' +
                    'enters the machine.'
                )
                self.update_info_box(lbl, txt)
                self.error_procedure()

            # If feedtk has a high level alarm
            elif lfeed > self.constructor.db['feed_tk_level_params'][3]:
                self._hide_transient_buttons()

                # The reactor is empty
                if l1_open and l2_open:
                    self.constructor.db['status_flag'] = 'idle'
                    self.clean_GPIO()
                    self.inits_fn()

                # Reactor is not empty (NORMAL CONDITION)
                elif not l1_open and l2_open:
                    lbl = 'WARNING-404'
                    txt = (
                        'Feed tank has a high level alarm. ' +
                        'The feed flowrate to the machine may be too high.'
                    )
                    self.update_info_box(lbl, txt)
                    self.error_procedure()

                # Reactor has no low level but has a high level (IMPOSSIBLE)
                elif l1_open and not l2_open:
                    lbl = 'ERROR-409'
                    self.rx_levels_error(lbl)

                # Reactor is full with a high level alarm
                elif not l1_open and not l2_open:
                    self.clean_GPIO()
                    lbl1 = 'WARNING-403'
                    lbl2 = 'ERROR-407'
                    self.emptying_rx_full(lbl1, lbl2)

        self.first_run = False

    def steri_procedure(self):
        """Sterilization procedure."""
        if self.constructor.global_focus != 'auto':
            self.clean_GPIO()
            return

        if self.constructor.db['status_flag'] == 'steri':
            print('Attempted to start steri when steri was already running.')
            return

        self._hide_transient_buttons()
        lbl = 'NOTE'
        txt = (
            'Performing sterilization. ' +
            'Stage 1: Warming ozone generator. Please do not power-off.'
        )
        self.update_info_box(lbl, txt)

        self.constructor.db['status_flag'] = 'steri'

        # Warm-up ozone generator
        self.clean_GPIO()
        self.turn_o3_on()

        self.steri_start_time = time.time()

        self.steri_stage = 'loop1'
        self.steri_loop1()

    def steri_loop1(self):
        """Sterilization loop - First stage."""
        if self.constructor.global_focus != 'auto':
            self.clean_GPIO()
            return

        if (
            self.constructor.db['status_flag'] == 'steri'
            and self.steri_stage == 'loop1'
        ):
            now = time.time()
            time_passed = (now - self.steri_start_time) / 60
            if time_passed > self.constructor.db['warmup_time'][3]:
                GPIO.output(self.constructor.o2_pin, self.constructor.ON)
                GPIO.output(self.constructor.recirpmp_pin, self.constructor.ON)
                self.turn_o2_on()
                self.turn_recirpmp_on()
                self.steri_stage = 'loop2'
                self.steri_start_time = time.time()
                print('loop1')
                self.steri_loop2()

                lbl = 'NOTE'
                txt = (
                    'Performing sterilization. Stage 2: Sterilization ' +
                    'time is defined as {0:.1f}min. Please do not power-off.'
                ).format(self.constructor.db['steri_time'][3])
                self.update_info_box(lbl, txt)

            self.master.after(2000, self.steri_loop1)
        else:
            return

    def steri_loop2(self):
        """Sterilization loop - Second stage."""
        if self.constructor.global_focus != 'auto':
            self.clean_GPIO()
            return

        if (
            self.constructor.db['status_flag'] == 'steri'
            and self.steri_stage == 'loop2'
        ):
            now = time.time()
            time_passed = (now - self.steri_start_time) / 60
            if time_passed >= self.constructor.db['steri_time'][3]:
                self.turn_o3_off()
                self.turn_o2_off()
                self.turn_recirpmp_off()
                self.clean_GPIO()  # Make sure all equipments are off
                self.steri_stage = 'loop3'
                self.steri_start_time = time.time()
                self.steri_loop3()

                lbl = 'NOTE'
                txt = (
                    'Performing sterilization. Stage 3: Settling. ' +
                    'Please do not power-off.'
                )
                self.update_info_box(lbl, txt)

            self.master.after(5000, self.steri_loop2)
        else:
            return

    def steri_loop3(self):
        """Sterilization loop - Third stage."""
        if self.constructor.global_focus != 'auto':
            self.clean_GPIO()
            return

        if (
            self.constructor.db['status_flag'] == 'steri'
            and self.steri_stage == 'loop3'
        ):
            now = time.time()
            time_passed = (now - self.steri_start_time) / 60
            if time_passed >= self.constructor.db['settle_time'][3]:
                self.steri_stage = 'loop1'
                self.constructor.db['status_flag'] = 'emptying'
                self.constructor.save_db()
                self.inits_fn()
            self.master.after(2000, self.steri_loop3)
        else:
            return

    # Shut-down all equipments
    def clean_GPIO(self):
        """Clean RPi GPIO."""
        self.turn_feedpmp_off()
        self.turn_recirpmp_off()
        self.turn_outpmp_off()
        self.turn_o2_off()
        self.turn_o3_off()
        self.turn_uv_off()

    def update_ui(self):
        """
        Update the UI.

        This method updates the ui in respect to the toggle flags
        """
        # Update O2 label
        if self.toggle_o2 == 'on':
            self.lbl_o2['image'] = self.ima_o2_on
            if self.toggle_recirpmp == 'off':
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir10
                )
            else:
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir11
                )
        else:
            self.lbl_o2['image'] = self.ima_o2_off
            if self.toggle_recirpmp == 'off':
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir00
                )
            else:
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir01
                )

        # Update O3 label
        if self.toggle_o3 == 'on':
            self.lbl_o3['image'] = self.ima_o3_on
            self.w.itemconfigure(self.canvas_o3, image=self.ima_o31)
        else:
            self.lbl_o3['image'] = self.ima_o3_off
            self.w.itemconfigure(self.canvas_o3, image=self.ima_o30)

        # Update UV label
        if self.toggle_uv == 'on':
            self.lbl_uv['image'] = self.ima_uv_on
            self.w.itemconfigure(self.canvas_uv, image=self.ima_uv1)
        else:
            self.lbl_uv['image'] = self.ima_uv_off
            self.w.itemconfigure(self.canvas_uv, image=self.ima_uv0)

        # Update FeedPmp label
        if self.toggle_feedpmp == 'on':
            self.lbl_feedpmp['image'] = self.ima_feedpmp_on
            self.w.itemconfigure(self.canvas_feed, image=self.ima_feed1)
            self.w.itemconfigure(
                'filling_poly',
                outline=colors.LIGHT_BLUE_COLOR
            )
        else:
            self.lbl_feedpmp['image'] = self.ima_feedpmp_off
            self.w.itemconfigure(self.canvas_feed, image=self.ima_feed0)
            self.w.itemconfigure('filling_poly', outline=colors.FG_COLOR)

        # Update RecirPmp label
        if self.toggle_recirpmp == 'on':
            self.lbl_recirpmp['image'] = self.ima_recirpmp_on
            if self.toggle_o2 == 'on':
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir11
                )
            else:
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir01
                )
            self.w.itemconfigure(
                'recirpmp_poly',
                outline=colors.LIGHT_BLUE_COLOR
            )
        else:
            self.lbl_recirpmp['image'] = self.ima_recirpmp_off
            if self.toggle_o2 == 'on':
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir10
                )
            else:
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir00
                )
            self.w.itemconfigure('recirpmp_poly', outline=colors.FG_COLOR)

        # Update OutPmp label
        if self.toggle_outpmp == 'on':
            self.lbl_outpmp['image'] = self.ima_outpmp_on
            self.w.itemconfigure(self.canvas_out, image=self.ima_out1)
            self.w.itemconfigure('out_poly', outline=colors.LIGHT_BLUE_COLOR)
        else:
            self.lbl_outpmp['image'] = self.ima_outpmp_off
            self.w.itemconfigure(self.canvas_out, image=self.ima_out0)
            self.w.itemconfigure('out_poly', outline=colors.FG_COLOR)

    def update_info_box(self, lbl, txt):
        """Update the info box."""
        if lbl[0:4] == 'NOTE':
            color = colors.GREEN_COLOR
        elif lbl[0:7] == 'WARNING':
            color = colors.YELLOW_COLOR
        elif lbl[0:5] == 'ERROR':
            color = colors.RED_COLOR
        else:
            print('Error: update_info_box()')
        self.linfo_kw.config(text=lbl, fg=color)
        self.linfo['text'] = txt

    def l1_call(self, event):
        """Level 1 callback."""
        self.inits_fn()

    def l2_call(self, event):
        """Level 2 callback."""
        self.inits_fn()

    def binds(self):
        """Touch bindings."""
        self.w.bind('<Button-1>', self.canvasbind)
        self.lbl_shut.bind('<Button-1>', self.shut_call)
        self.lbl_feedpmp.bind('<Button-1>', self.lbl_feedpmp_call)
        self.lbl_feedtk.bind('<Button-1>', self.lbl_feedtk_call)
        self.lbl_o2.bind('<Button-1>', self.lbl_o2_call)
        self.lbl_o3.bind('<Button-1>', self.lbl_o3_call)
        self.lbl_outpmp.bind('<Button-1>', self.lbl_outpmp_call)
        self.lbl_reactor.bind('<Button-1>', self.lbl_reactor_call)
        self.lbl_recirpmp.bind('<Button-1>', self.lbl_recirpmp_call)
        self.lbl_uv.bind('<Button-1>', self.lbl_uv_call)
        self.btn_start_steri.bind('<Button-1>', self.btn_start_steri_call)
        self.btn_proceed.bind('<Button-1>', self.btn_proceed_call)

    def unbinds(self):
        """Unbind."""
        self.w.unbind('<Button-1>')
        self.lbl_shut.unbind('<Button-1>')
        self.lbl_feedpmp.unbind('<Button-1>')
        self.lbl_feedtk.unbind('<Button-1>')
        self.lbl_o2.unbind('<Button-1>')
        self.lbl_o3.unbind('<Button-1>')
        self.lbl_outpmp.unbind('<Button-1>')
        self.lbl_reactor.unbind('<Button-1>')
        self.lbl_recirpmp.unbind('<Button-1>')
        self.lbl_uv.unbind('<Button-1>')
        self.btn_start_steri.unbind('<Button-1>')
        self.btn_proceed.unbind('<Button-1>')

    def btn_start_steri_call(self, event):
        """Start sterilization button callback."""
        self.clean_GPIO()
        self.steri_procedure()

    def btn_proceed_call(self, event):
        """
        Proceed button callback.

        This method changes the proceed flags in order to
        update the ui in case the user chooses to proceed
        when facing a warning.

        For instance, after the user chooses to proceed the
        proceed button must be unpacked and the info string
        changed to reflect the user option to proceed
        """
        if self.proceed_id == 1:
            if not self.proceed_1:
                self.proceed_1 = True
                self.inits_fn()
        if self.proceed_id == 2:
            if not self.proceed_2:
                self.proceed_2 = True
                self.inits_fn()

    def lbl_feedpmp_call(self, event):
        """Feed pump label callback."""
        self.pop_feedpmp(event)

    def set_pop_flag(self):
        """End of popup running."""
        if self.pop_running:
            self.pop_running = False

    def lbl_feedtk_call(self, event):
        """Feed tank label callback."""
        if self.constructor.global_focus != 'auto':
            return
        self.pop_feedtk(event)

    def lbl_o2_call(self, event):
        """Oxygen valve label callback."""
        if self.constructor.global_focus != 'auto':
            return
        self.pop_o2(event)

    def lbl_o3_call(self, event):
        """Ozone generator label callback."""
        if self.constructor.global_focus != 'auto':
            return
        self.pop_o3(event)

    def lbl_outpmp_call(self, event):
        """Outlet pump label callback."""
        if self.constructor.global_focus != 'auto':
            return
        self.pop_outpmp(event)

    def lbl_reactor_call(self, event):
        """Reactor label callback."""
        if self.constructor.global_focus != 'auto':
            return
        self.pop_reactor(event)

    def lbl_recirpmp_call(self, event):
        """Recirculation pump label callback."""
        if self.constructor.global_focus != 'auto':
            return
        self.pop_recirpmp(event)

    def lbl_uv_call(self, event):
        """UV label callback."""
        if self.constructor.global_focus != 'auto':
            return
        self.pop_uv(event)

    def canvasbind(self, event):
        """Binding for the canvas."""
        if event.x > 28 and event.x < 73 and event.y > 4 and event.y < 60:
            self.pop_o2(event)
        elif event.x > 131 and event.x < 177 and event.y > 12 and event.y < 72:
            self.pop_o3(event)
        elif event.x > 237 and event.x < 279 and event.y > 10 and event.y < 54:
            self.pop_recirpmp(event)
        elif (
            event.x > 343
            and event.x < 381
            and event.y > 12
            and event.y < 100
        ):
            self.pop_uv(event)
        elif (
            event.x > 132
            and event.x < 176
            and event.y > 226
            and event.y < 269
        ):
            self.pop_feedpmp(event)
        elif (
            event.x > 223
            and event.x < 295
            and event.y > 96
            and event.y < 269
        ):
            self.pop_reactor(event)
        elif (
            event.x > 340
            and event.x < 385
            and event.y > 226
            and event.y < 269
        ):
            self.pop_outpmp(event)
        elif event.x > 12 and event.x < 88 and event.y > 151 and event.y < 268:
            self.pop_feedtk(event)
        else:
            pass

    def pop_o2(self, event):
        """Oxygen valve popup."""
        if self.constructor.global_focus != 'auto':
            return
        self.constructor.pop_o2app.update_pop()
        self.constructor.anim_pop(
            event,
            self.constructor.pop_o2panel,
            self.master,
            self
        )

    def pop_o3(self, event):
        """Ozone generator popup."""
        if self.constructor.global_focus != 'auto':
            return
        self.constructor.pop_o3app.update_pop()
        self.constructor.anim_pop(
            event,
            self.constructor.pop_o3panel,
            self.master,
            self
        )

    def pop_feedpmp(self, event):
        """Feed pump popup."""
        if self.constructor.global_focus != 'auto':
            return
        self.constructor.pop_feedpmpapp.update_pop()
        self.constructor.anim_pop(
            event,
            self.constructor.pop_feedpmppanel,
            self.master,
            self
        )

    def pop_recirpmp(self, event):
        """Recirculation pump popup."""
        if self.constructor.global_focus != 'auto':
            return
        self.constructor.pop_recirpmpapp.update_pop()
        self.constructor.anim_pop(
            event,
            self.constructor.pop_recirpmppanel,
            self.master,
            self
        )

    def pop_uv(self, event):
        """UV lamp popup."""
        if self.constructor.global_focus != 'auto':
            return
        self.constructor.pop_uvapp.update_pop()
        self.constructor.anim_pop(
            event,
            self.constructor.pop_uvpanel,
            self.master,
            self
        )

    def pop_reactor(self, event):
        """Reactor popup."""
        if self.constructor.global_focus != 'auto':
            return
        self.constructor.pop_reactorapp.update_pop()
        self.constructor.anim_pop(
            event,
            self.constructor.pop_reactorpanel,
            self.master,
            self
        )

    def pop_outpmp(self, event):
        """Outlet pump popup."""
        if self.constructor.global_focus != 'auto':
            return
        self.constructor.pop_outpmpapp.update_pop()
        self.constructor.anim_pop(
            event,
            self.constructor.pop_outpmppanel,
            self.master,
            self
        )

    def pop_feedtk(self, event):
        """Feed tank popup."""
        if self.constructor.global_focus != 'auto':
            return
        self.constructor.pop_feedtkapp.update_pop(self)
        self.constructor.anim_pop(
            event,
            self.constructor.pop_feedtkpanel,
            self.master,
            self
        )

    def o2_call(self):
        """Oxygen valve callback."""
        if self.constructor.global_focus != 'auto':
            return
        if self.toggle_o2 == 'on':
            self.lbl_o2['image'] = self.ima_o2_on
            if self.toggle_recirpmp == 'off':
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir10
                )
            else:
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir11
                )
        else:
            self.lbl_o2['image'] = self.ima_o2_off
            if self.toggle_recirpmp == 'off':
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir00
                )
            else:
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir01
                )

    def o3_call(self):
        """Ozone generator callback."""
        if self.constructor.global_focus != 'auto':
            return
        if self.toggle_o3 == 'on':
            self.lbl_o3['image'] = self.ima_o3_on
            self.w.itemconfigure(self.canvas_o3, image=self.ima_o31)
        else:
            self.lbl_o3['image'] = self.ima_o3_off
            self.w.itemconfigure(self.canvas_o3, image=self.ima_o30)

    def uv_call(self):
        """UV callback."""
        if self.constructor.global_focus != 'auto':
            return
        if self.toggle_uv == 'on':
            self.lbl_uv['image'] = self.ima_uv_on
            self.w.itemconfigure(self.canvas_uv, image=self.ima_uv1)
        else:
            self.lbl_uv['image'] = self.ima_uv_off
            self.w.itemconfigure(self.canvas_uv, image=self.ima_uv0)

    def feedpmp_call(self):
        """Feed pump callback."""
        if self.constructor.global_focus != 'auto':
            return
        if self.toggle_feedpmp == 'on':
            self.lbl_feedpmp['image'] = self.ima_feedpmp_on
            self.w.itemconfigure(self.canvas_feed, image=self.ima_feed1)
            self.w.itemconfigure(
                'filling_poly',
                outline=colors.LIGHT_BLUE_COLOR
            )
            self.master.after(10, self.rotate_feedpmp)
        else:
            self.lbl_feedpmp['image'] = self.ima_feedpmp_off
            self.w.itemconfigure(self.canvas_feed, image=self.ima_feed0)
            self.w.itemconfigure('filling_poly', outline=colors.FG_COLOR)

    def rotate_feedpmp(self):
        """Rotate feed pump."""
        if self.toggle_feedpmp == 'on':
            self.x0_feedpmp, self.y0_feedpmp = self._rot_feedpmp(
                self.x0_feedpmp,
                self.y0_feedpmp
            )
            self.x1_feedpmp, self.y1_feedpmp = self._rot_feedpmp(
                self.x1_feedpmp,
                self.y1_feedpmp
            )
            self.x2_feedpmp, self.y2_feedpmp = self._rot_feedpmp(
                self.x2_feedpmp,
                self.y2_feedpmp
            )
            self.w.coords(
                self.feedpmp,
                self.x0_feedpmp,
                self.y0_feedpmp,
                self.x1_feedpmp,
                self.y1_feedpmp,
                self.x2_feedpmp,
                self.y2_feedpmp
            )
            self.master.after(30, self.rotate_feedpmp)
        else:
            self.x0_feedpmp = self.x00_feedpmp
            self.y0_feedpmp = self.y00_feedpmp
            self.x1_feedpmp = self.x10_feedpmp
            self.y1_feedpmp = self.y10_feedpmp
            self.x2_feedpmp = self.x20_feedpmp
            self.y2_feedpmp = self.y20_feedpmp
            self.w.coords(
                self.feedpmp,
                self.x0_feedpmp,
                self.y0_feedpmp,
                self.x1_feedpmp,
                self.y1_feedpmp,
                self.x2_feedpmp,
                self.y2_feedpmp
            )
            self.lbl_feedpmp['image'] = self.ima_feedpmp_off
            self.w.itemconfigure(self.canvas_feed, image=self.ima_feed0)
            self.w.itemconfigure('filling_poly', outline=colors.FG_COLOR)

    def _rot_feedpmp(self, x, y):
        x -= self.feedpmp_center[0]
        y -= self.feedpmp_center[1]
        _x = x * math.cos(self.t) - y * math.sin(self.t)
        _y = x * math.sin(self.t) + y * math.cos(self.t)
        return _x + self.feedpmp_center[0], _y + self.feedpmp_center[1]

    def recirpmp_call(self):
        """Recirculation pump callback."""
        if self.constructor.global_focus != 'auto':
            return
        if self.toggle_recirpmp == 'on':
            self.lbl_recirpmp['image'] = self.ima_recirpmp_on
            if self.toggle_o2 == 'on':
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir11
                )
            else:
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir01
                )
            self.w.itemconfigure(
                'recirpmp_poly',
                outline=colors.LIGHT_BLUE_COLOR
            )
            self.master.after(10, self.rotate_recirpmp)
        else:
            self.lbl_recirpmp['image'] = self.ima_recirpmp_off
            if self.toggle_o2 == 'on':
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir10
                )
            else:
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir00
                )
            self.w.itemconfigure('recirpmp_poly', outline=colors.FG_COLOR)

    def rotate_recirpmp(self):
        """Rotate recirculation pump."""
        if self.toggle_recirpmp == 'on':
            self.x0_recirpmp, self.y0_recirpmp = self._rot_recirpmp(
                self.x0_recirpmp,
                self.y0_recirpmp
            )
            self.x1_recirpmp, self.y1_recirpmp = self._rot_recirpmp(
                self.x1_recirpmp,
                self.y1_recirpmp
            )
            self.x2_recirpmp, self.y2_recirpmp = self._rot_recirpmp(
                self.x2_recirpmp,
                self.y2_recirpmp
            )
            self.w.coords(
                self.recirpmp,
                self.x0_recirpmp,
                self.y0_recirpmp,
                self.x1_recirpmp,
                self.y1_recirpmp,
                self.x2_recirpmp,
                self.y2_recirpmp
            )
            self.master.after(30, self.rotate_recirpmp)
        else:
            self.x0_recirpmp = self.x00_recirpmp
            self.y0_recirpmp = self.y00_recirpmp
            self.x1_recirpmp = self.x10_recirpmp
            self.y1_recirpmp = self.y10_recirpmp
            self.x2_recirpmp = self.x20_recirpmp
            self.y2_recirpmp = self.y20_recirpmp
            self.w.coords(
                self.recirpmp,
                self.x0_recirpmp,
                self.y0_recirpmp,
                self.x1_recirpmp,
                self.y1_recirpmp,
                self.x2_recirpmp,
                self.y2_recirpmp
            )
            self.lbl_recirpmp['image'] = self.ima_recirpmp_off
            if self.toggle_o2 == 'on':
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir10
                )
            else:
                self.w.itemconfigure(
                    self.canvas_o2_recir,
                    image=self.ima_o2_recir00
                )
            self.w.itemconfigure('recirpmp_poly', outline=colors.FG_COLOR)

    def _rot_recirpmp(self, x, y):
        x -= self.recirpmp_center[0]
        y -= self.recirpmp_center[1]
        _x = x * math.cos(self.t) - y * math.sin(self.t)
        _y = x * math.sin(self.t) + y * math.cos(self.t)
        return _x + self.recirpmp_center[0], _y + self.recirpmp_center[1]

    def outpmp_call(self):
        """Outlet pump callback."""
        if self.constructor.global_focus != 'auto':
            return
        if self.toggle_outpmp == 'on':
            self.lbl_outpmp['image'] = self.ima_outpmp_on
            self.w.itemconfigure(self.canvas_out, image=self.ima_out1)
            self.w.itemconfigure('out_poly', outline=colors.LIGHT_BLUE_COLOR)
            self.master.after(10, self.rotate_outpmp)
        else:
            self.lbl_outpmp['image'] = self.ima_outpmp_off
            self.w.itemconfigure(self.canvas_out, image=self.ima_out0)
            self.w.itemconfigure('out_poly', outline=colors.FG_COLOR)

    def rotate_outpmp(self):
        """Rotate outlet pump."""
        if self.toggle_outpmp == 'on':
            self.x0_outpmp, self.y0_outpmp = self._rot_outpmp(
                self.x0_outpmp,
                self.y0_outpmp
            )
            self.x1_outpmp, self.y1_outpmp = self._rot_outpmp(
                self.x1_outpmp,
                self.y1_outpmp
            )
            self.x2_outpmp, self.y2_outpmp = self._rot_outpmp(
                self.x2_outpmp,
                self.y2_outpmp
            )
            self.w.coords(
                self.outpmp,
                self.x0_outpmp,
                self.y0_outpmp,
                self.x1_outpmp,
                self.y1_outpmp,
                self.x2_outpmp,
                self.y2_outpmp
            )
            self.master.after(30, self.rotate_outpmp)
        else:
            self.x0_outpmp, self.y0_outpmp = self.x00_outpmp, self.y00_outpmp
            self.x1_outpmp, self.y1_outpmp = self.x10_outpmp, self.y10_outpmp
            self.x2_outpmp, self.y2_outpmp = self.x20_outpmp, self.y20_outpmp
            self.w.coords(
                self.outpmp,
                self.x0_outpmp,
                self.y0_outpmp,
                self.x1_outpmp,
                self.y1_outpmp,
                self.x2_outpmp,
                self.y2_outpmp
            )

    def _rot_outpmp(self, x, y):
        x -= self.outpmp_center[0]
        y -= self.outpmp_center[1]
        _x = x * math.cos(self.t) - y * math.sin(self.t)
        _y = x * math.sin(self.t) + y * math.cos(self.t)
        return _x + self.outpmp_center[0], _y + self.outpmp_center[1]

    def shut_call(self, event):
        """Shutdown callback."""
        if self.constructor.global_focus != 'auto':
            return
        self.unbinds()
        self._hide_transient_buttons()
        flag = 'home'
        self.constructor.anim_btn(
            0,
            self.constructor.homepanel,
            self.master,
            self.lbl_shut,
            self.ima_shut,
            self.ima_shut_push,
            flag,
            self.constructor.homeapp
        )
        self.master.after(1200, self.clean_up)

    def clean_up(self):
        """Clean up GPIO and UI."""
        for pin in self.constructor.lst_pins_out:
            GPIO.setup(pin, GPIO.OUT, initial=1)

        self.toggle_feedpmp = "off"
        self.toggle_recirpmp = "off"
        self.toggle_outpmp = "off"
        self.toggle_o2 = "off"
        self.toggle_o3 = "off"
        self.toggle_uv = "off"

        GPIO.remove_event_detect(self.constructor.reactor_llow_pin)
        GPIO.remove_event_detect(self.constructor.reactor_lhigh_pin)

        self.linfo_kw.config(text=self.LINFO_KW_ISTRING, fg=colors.FG_COLOR)
        self.linfo.config(text=self.LINFO_ISTRING)

        self.proceed_1 = False
        self.proceed_2 = False

    def _show_steri_button(self):
        if self.btn_start_steri.winfo_ismapped():
            return
        else:
            self.btn_start_steri.pack(ipady=5, ipadx=5, pady=3)

    def _hide_steri_button(self):
        if self.btn_start_steri.winfo_ismapped():
            self.btn_start_steri.pack_forget()
        else:
            return

    def _show_proceed_button(self):
        if self.btn_proceed.winfo_ismapped():
            return
        else:
            self.btn_proceed.pack(ipady=5, ipadx=5, pady=3)

    def _hide_proceed_button(self):
        if self.btn_proceed.winfo_ismapped():
            self.btn_proceed.pack_forget()
        else:
            return

    def _hide_transient_buttons(self):
        self._hide_steri_button()
        self._hide_proceed_button()

    def etape_error(self, lbl, error):
        """E-tape error."""
        self.update_info_box(lbl, error)
        self.error_procedure()

    def idle_rx_not_empty(self, lbl):
        """Handle Reactor not empty."""
        self.clean_GPIO()
        txt = (
            'Unexpected system state detected. ' +
            'Reactor is not empty as it should be at this point. ' +
            'Cannot proceed.'
        )
        self.update_info_box(lbl, txt)
        self.error_procedure()

    def idle_rx_full(self, lbl1, lbl2):
        """Handle Reactor full."""
        # If semi-auto mode is enabled
        print('I am in idle_rx_full')
        self.clean_GPIO()
        if self.constructor.db['enable_semi_auto'][1]:
            lbl = lbl1
            txt = (
                'Unexpected system state detected. ' +
                'The reactor should not be full at this stage. ' +
                'Proceed to sterilization anyway?'
            )
            self._show_steri_button()
        else:
            lbl = lbl2
            txt = (
                'Unexpected state detected during idle. ' +
                'The reactor should not be full at this stage. ' +
                'Cannot proceed.'
            )
            self.error_procedure()
        self.update_info_box(lbl, txt)

    def rx_levels_error(self, lbl):
        """Handle Reactor levels error."""
        self.clean_GPIO()
        txt = (
            'Reactor level sensors are not working properly. ' +
            'Cannot proceed. Please check the sensors and try again.'
        )
        self.update_info_box(lbl, txt)
        self.error_procedure()

    def filling_rx_full(self, lbl1, lbl2):
        """Handle Reactor full during filling stage."""
        self.clean_GPIO()
        # If semi-auto mode is enabled
        if self.constructor.db['enable_semi_auto'][1]:
            lbl = lbl1
            txt = (
                'Unexpected system state detected. ' +
                'The reactor should not be full at this stage. ' +
                'Proceed to sterilization anyway?'
            )
            self.update_info_box(lbl, txt)
            self._show_steri_button()
        else:
            lbl = lbl2
            txt = (
                'Unexpected state detected during filling. ' +
                'The reactor should not be full at this stage. ' +
                'Cannot proceed.'
            )
            self.update_info_box(lbl, txt)
            self.error_procedure()

    def steri_rx_full(self, lbl1, lbl2):
        """Handle Reactor full during sterilization stage."""
        # If semi-auto mode is enabled TODO
        if self.constructor.db['enable_semi_auto'][1]:
            lbl = lbl1
            txt = (
                'Unexpected system state detected. ' +
                'The reactor should not be full at this stage. ' +
                'Cannot proceed.'
            )
            self.update_info_box(lbl, txt)
            self.error_procedure()
        else:
            lbl = lbl2
            txt = (
                'Unexpected state detected during sterilization. ' +
                'The reactor should not be full at this stage. ' +
                'Cannot proceed.'
            )
            self.update_info_box(lbl, txt)
            self.error_procedure()

    def emptying_rx_full(self, lbl1, lbl2):
        """Handle Reactor full during emptying stage."""
        # If semi-auto mode is enabled TODO
        self.clean_GPIO()
        if self.constructor.db['enable_semi_auto'][1]:
            lbl = lbl1
            txt = (
                'Unexpected system state detected. ' +
                'The reactor should not be full at this stage. ' +
                'Cannot proceed.'
            )
            self.update_info_box(lbl, txt)
            self.error_procedure()
        else:
            lbl = lbl2
            txt = (
                'Unexpected state detected during sterilization. ' +
                'The reactor should not be full at this stage. ' +
                'Cannot proceed.'
            )
            self.update_info_box(lbl, txt)
            self.error_procedure()

    def turn_feedpmp_on(self):
        """Switch feed pump on."""
        if (
            GPIO.input(self.constructor.feedpmp_pin)
            == self.constructor.db['ON']
        ):
            print('Feedpump was already on.')
        else:
            GPIO.output(
                self.constructor.feedpmp_pin,
                self.constructor.db['ON']
            )
            self.toggle_feedpmp = 'on'
            self.feedpmp_call()
            self.start_feedpmp_counter = time.time()

    def turn_feedpmp_off(self):
        """Switch feed pump off."""
        print('feed_pmp_off')
        if GPIO.input(
            self.constructor.feedpmp_pin
        ) == self.constructor.db['OFF']:
            print('Feed pump was already off.')
        else:
            GPIO.output(
                self.constructor.feedpmp_pin,
                self.constructor.db['OFF']
            )
            self.toggle_feedpmp = 'off'
            self.feedpmp_call()
            if self.start_feedpmp_counter != 0:
                self.stop_feedpmp_counter = time.time()
                elapsed_time_min = int((
                    self.stop_feedpmp_counter - self.start_feedpmp_counter
                ) / 60)
                self.constructor.db['feedpmp_op_time'][0] += elapsed_time_min
                self.constructor.db['feedpmp_tubelife'][0] += elapsed_time_min
                self.constructor.save_db()

    def turn_recirpmp_on(self):
        """Switch recirculation pump on."""
        if GPIO.input(
            self.constructor.recirpmp_pin
        ) == self.constructor.db['ON']:
            print('Recir pump was already on.')
        else:
            GPIO.output(
                self.constructor.recirpmp_pin,
                self.constructor.db['ON']
            )
            self.toggle_recirpmp = 'on'
            self.recirpmp_call()
            self.start_recirpmp_counter = time.time()

    def turn_recirpmp_off(self):
        """Switch recirculation pump off."""
        if GPIO.input(
            self.constructor.recirpmp_pin
        ) == self.constructor.db['OFF']:
            print('Recirculation pump was already off.')
        else:
            GPIO.output(
                self.constructor.recirpmp_pin,
                self.constructor.db['OFF']
            )
            self.toggle_recirpmp = 'off'
            self.recirpmp_call()
            if self.start_recirpmp_counter != 0:
                self.stop_recirpmp_counter = time.time()
                elapsed_time_min = int((
                    self.stop_recirpmp_counter - self.start_recirpmp_counter
                ) / 60)
                self.constructor.db['recirpmp_op_time'][0] += elapsed_time_min
                self.constructor.save_db()

    def turn_outpmp_on(self):
        """Switch outlet pump on."""
        if GPIO.input(
            self.constructor.outpmp_pin
        ) == self.constructor.db['ON']:
            print('Attempted to start out pump when it was already turned on.')
        else:
            GPIO.output(self.constructor.outpmp_pin, self.constructor.db['ON'])
            self.toggle_outpmp = 'on'
            self.outpmp_call()
            self.start_outpmp_counter = time.time()

    def turn_outpmp_off(self):
        """Switch outlet pump off."""
        if GPIO.input(
            self.constructor.outpmp_pin
        ) == self.constructor.db['OFF']:
            print('Outlet pump was already turned off.')
        else:
            GPIO.output(
                self.constructor.outpmp_pin,
                self.constructor.db['OFF']
            )
            self.toggle_outpmp = 'off'
            self.outpmp_call()
            if self.start_outpmp_counter != 0:
                self.stop_outpmp_counter = time.time()
                elapsed_time_min = int((
                    self.stop_outpmp_counter - self.start_outpmp_counter
                ) / 60)
                self.constructor.db['outpmp_op_time'][0] += elapsed_time_min
                self.constructor.db['outpmp_tubelife'][0] += elapsed_time_min
                self.constructor.save_db()

    def turn_o2_on(self):
        """Open oxygen valve."""
        if GPIO.input(self.constructor.o2_pin) == self.constructor.db['ON']:
            print('Attempted to open O2 valve when it was already open.')
        else:
            GPIO.output(self.constructor.o2_pin, self.constructor.db['ON'])
            self.toggle_o2 = 'on'
            self.o2_call()

    def turn_o2_off(self):
        """Close oxygen valve."""
        if GPIO.input(self.constructor.o2_pin) == self.constructor.db['OFF']:
            print('O2 valve was already closed.')
        else:
            GPIO.output(self.constructor.o2_pin, self.constructor.db['OFF'])
            self.toggle_o2 = 'off'
            self.o2_call()

    def turn_o3_on(self):
        """Switch ozone generator on."""
        if GPIO.input(self.constructor.o3_pin) == self.constructor.db['ON']:
            print('O3 generator was already on.')
        else:
            GPIO.output(self.constructor.o3_pin, self.constructor.db['ON'])
            self.toggle_o3 = 'on'
            self.o3_call()
            self.start_o3_counter = time.time()

    def turn_o3_off(self):
        """Switch ozone generator off."""
        if GPIO.input(self.constructor.o3_pin) == self.constructor.db['OFF']:
            print('O3 generator was already off.')
        else:
            GPIO.output(self.constructor.o3_pin, self.constructor.db['OFF'])
            self.toggle_o3 = 'off'
            self.o3_call()
            if self.start_o3_counter != 0:
                self.stop_o3_counter = time.time()
                elapsed_time_min = int((
                    self.stop_o3_counter - self.start_o3_counter
                ) / 60)
                self.constructor.db['o3_op_time'][0] += elapsed_time_min
                self.constructor.save_db()

    def turn_uv_on(self):
        """Switch UV lamp on."""
        if GPIO.input(self.constructor.uv_pin) == self.constructor.db['ON']:
            print('Attempted to open UV lamp when it was already open.')
        else:
            GPIO.output(self.constructor.uv_pin, self.constructor.db['ON'])
            self.toggle_uv = 'on'
            self.uv_call()
            self.start_uv_counter = time.time()

    def turn_uv_off(self):
        """Switch UV lamp off."""
        if GPIO.input(self.constructor.uv_pin) == self.constructor.db['OFF']:
            print('Attempted to close the UV lamp when it was already closed.')
        else:
            GPIO.output(self.constructor.uv_pin, self.constructor.db['OFF'])
            self.toggle_uv = 'off'
            self.uv_call()
            if self.start_uv_counter != 0:
                self.stop_uv_counter = time.time()
                elapsed_time_min = int((
                    self.stop_uv_counter - self.start_uv_counter
                ) / 60)
                self.constructor.db['uv_op_time'][0] += elapsed_time_min
                self.constructor.save_db()

    def error_procedure(self):
        """
        Error procedure.

        This method is called whenever there is an error
        In this method can reside, p.e., the sound alarmes
        routine. Or the error pop-ups...
        """
        self.iserror = True
