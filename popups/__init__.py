"""Collection of app popups."""
import tkinter as tk
from helpers import colors
import RPi.GPIO as GPIO
import graphics

graph = graphics.Popups()


class ResettubePU:
    """Reset tube life popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(
            master=self.master,
            data=graph.reset_tube_life
        )
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)


class ResettubeOutPU:
    """Reset tube life popup (outlet pump)."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(
            master=self.master,
            data=graph.reset_tube_life_outlet
        )
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)


class ResetconsumuvPU:
    """Reset UV time popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(
            master=self.master,
            data=graph.reset_consum_uv
        )
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)


class Resetconsumo3PU:
    """Reset O3 time popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(
            master=self.master,
            data=graph.reset_consum_o3
        )
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)


class Resetstats:
    """Reset stats popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(
            master=self.master,
            data=graph.reset_stats
        )
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)


class GemaPU:
    """Gema popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.gema_pu)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)


class VaPU:
    """VA popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.va_pop)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)


class SteriPU:
    """Steri popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.steri_pu)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)


class ShutdownPU:
    """Shutdown popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(
            master=self.master,
            data=graph.shutdown_pu
        )
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)


class FeedTk:
    """Feed tank popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.feedtk)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)
        self.lbl1 = tk.Label(
            self.master, text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl1.place(x=130, y=67)
        self.lbl2 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl2.place(x=130, y=109)
        self.lbl3 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl3.place(x=130, y=151)
        self.c_feed = tk.Canvas(
            self.master,
            width=50,
            height=77,
            bg=colors.BG_COLOR,
            borderwidth=0,
            highlightthickness=0
        )
        self.c_feed.place(x=25, y=58)
        self.c_feed.create_rectangle(
            0,
            0,
            50,
            77,
            fill=colors.GREEN_COLOR,
            outline=colors.GREEN_COLOR,
            tags='obj1'
        )

    def update_pop(self, master):
        """Update the popup."""
        self.constructor.update_db()
        self.var1 = master.level_percent
        self.var3 = self.constructor.db['pop_feedtk'][2]
        self.var2 = self.var1 * self.var3 / 100
        self.lbl1['text'] = self.var1
        self.lbl2['text'] = self.var2
        self.lbl3['text'] = self.var3
        self.y_feedtk_level = int(77 * (1 - self.var1 / 100))
        self.c_feed.coords('obj1', 0, self.y_feedtk_level, 50, 77)
        if self.var1 > 90 or self.var1 < 10:
            self.c_feed.itemconfig(
                'obj1',
                fill=colors.RED_COLOR,
                outline=colors.RED_COLOR
            )
            self.lbl1['fg'] = colors.RED_COLOR
            self.lbl2['fg'] = colors.RED_COLOR
        elif self.var1 > 10 and self.var1 < 90:
            self.c_feed.itemconfig(
                'obj1',
                fill=colors.GREEN_COLOR,
                outline=colors.GREEN_COLOR
            )
            self.lbl1['fg'] = colors.GREEN_COLOR
            self.lbl2['fg'] = colors.GREEN_COLOR


class Reactor:
    """Reactor popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.reactor)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)
        self.c_reactor_lmax = tk.Canvas(
            self.master,
            width=10,
            height=10,
            bg=colors.GREEN_COLOR,
            borderwidth=0,
            highlightthickness=0
        )
        self.c_reactor_lmax.place(x=51, y=58)
        self.c_reactor_lmin = tk.Canvas(
            self.master,
            width=10,
            height=10,
            bg=colors.GREEN_COLOR,
            borderwidth=0,
            highlightthickness=0
        )
        self.c_reactor_lmin.place(x=51, y=103)
        self.lbl1 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl1.place(x=130, y=67)
        self.lbl2 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl2.place(x=130, y=109)
        self.lbl3 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl3.place(x=130, y=151)

    def update_pop(self):
        """Update the popup."""
        self.constructor.update_db()
        self.var1 = self.constructor.db['status_flag']
        if self.var1 == 'idle':
            self.lbl1['text'] = 'Idle state'
        elif self.var1 == 'steri':
            self.lbl1['text'] = 'Sterilization stage'
        elif self.var1 == 'filling':
            self.lbl1['text'] = 'Filling'
        elif self.var1 == 'emptying':
            self.lbl1['text'] = 'Emptying'
        self.var2 = not GPIO.input(self.constructor.reactor_llow_pin)
        self.var3 = not GPIO.input(self.constructor.reactor_lhigh_pin)
        if self.var2:  # If min level
            self.lbl2['text'] = 'Min level ok'
            self.lbl2['fg'] = colors.GREEN_COLOR
            self.c_reactor_lmin['bg'] = colors.GREEN_COLOR
        else:  # No min level
            self.lbl2['text'] = 'Low level alarm'
            self.lbl2['fg'] = colors.RED_COLOR
            self.c_reactor_lmin['bg'] = colors.RED_COLOR
        self.lbl2.place(x=130, y=151)
        if self.var3:  # If max level
            self.lbl3['text'] = 'High level alarm'
            self.lbl3['fg'] = colors.RED_COLOR
            self.c_reactor_lmax['bg'] = colors.RED_COLOR
        else:  # No max level
            self.lbl3['text'] = 'High level ok'
            self.lbl3['fg'] = colors.GREEN_COLOR
            self.c_reactor_lmax['bg'] = colors.GREEN_COLOR
        self.lbl3.place(x=130, y=109)


class FeedPmp:
    """Feed pump popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.feedpmp)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)

        self.lbl1 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl1.place(x=130, y=67)
        self.lbl2 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl2.place(x=130, y=109)
        self.lbl3 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl3.place(x=130, y=151)

    def update_pop(self):
        """Update the popup."""
        self.constructor.update_db()
        # State - Running or Stopped
        if GPIO.input(
            self.constructor.feedpmp_pin
        ) == self.constructor.db['ON']:
            self.var1 = 'Running'
        elif GPIO.input(
            self.constructor.feedpmp_pin
        ) == self.constructor.db['OFF']:
            self.var1 = 'Stopped'
        # Total operation time
        self.var2 = self.constructor.db['feedpmp_op_time'][0]
        # Tube life
        self.var3 = self.constructor.db['feedpmp_tubelife'][0]
        self.lbl1['text'] = self.var1
        self.lbl2['text'] = format(self.var2, '.1f')
        self.lbl3['text'] = format(self.var3, '.1f')


class OutPmp:
    """Outlet pump popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.outpmp)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)
        self.lbl1 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl1.place(x=130, y=67)
        self.lbl2 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl2.place(x=130, y=109)
        self.lbl3 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl3.place(x=130, y=151)

    def update_pop(self):
        """Update the popup."""
        self.constructor.update_db()
        # State - Running or Stopped
        if GPIO.input(
            self.constructor.outpmp_pin
        ) == self.constructor.db['ON']:
            self.var1 = 'Running'
        elif GPIO.input(
            self.constructor.outpmp_pin
        ) == self.constructor.db['OFF']:
            self.var1 = 'Stopped'
        # Total operation time
        self.var2 = self.constructor.db['outpmp_op_time'][0]
        # Tube life
        self.var3 = self.constructor.db['outpmp_tubelife'][0]
        self.lbl1['text'] = self.var1
        self.lbl2['text'] = format(self.var2, '.1f')
        self.lbl3['text'] = format(self.var3, '.1f')


class RecirPmp:
    """Recirculation pump popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.recirpmp)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)
        self.lbl1 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl1.place(x=130, y=67)
        self.lbl2 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl2.place(x=130, y=109)
        self.lbl3 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl3.place(x=130, y=151)

    def update_pop(self):
        """Update the popup."""
        self.constructor.update_db()
        # State - Running or Stopped
        if GPIO.input(
            self.constructor.recirpmp_pin
        ) == self.constructor.db['ON']:
            self.var1 = 'Running'
        elif GPIO.input(
            self.constructor.recirpmp_pin
        ) == self.constructor.db['OFF']:
            self.var1 = 'Stopped'
        # Total operation time
        self.var2 = self.constructor.db['recirpmp_op_time'][0]
        # Sterilization time
        self.var3 = self.constructor.db['steri_time'][3]

        self.lbl1['text'] = self.var1
        self.lbl2['text'] = format(self.var2, '.1f')
        self.lbl3['text'] = format(self.var3, '.1f')


class Uv:
    """UV popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.uv)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)
        self.lbl1 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl1.place(x=130, y=67)
        self.lbl2 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl2.place(x=130, y=109)
        self.lbl3 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl3.place(x=130, y=151)

    def update_pop(self):
        """Update the popup."""
        self.constructor.update_db()
        # State - ON or OFF
        if GPIO.input(self.constructor.uv_pin) == self.constructor.db['ON']:
            self.var1 = 'ON'
        elif GPIO.input(self.constructor.uv_pin) == self.constructor.db['OFF']:
            self.var1 = 'OFF'
        self.var2 = self.constructor.db['uv_op_time'][0]
        self.lbl1['text'] = self.var1
        self.lbl2['text'] = format(self.var2, '.1f')


class O3:
    """UV popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop = tk.PhotoImage(master=self.master, data=graph.ozone)
        self.label = tk.Label(self.master, image=self.ima_pop, bd=0)
        self.label.place(x=0, y=0)
        self.lbl1 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl1.place(x=130, y=67)
        self.lbl2 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl2.place(x=130, y=109)
        self.lbl3 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl3.place(x=130, y=151)

    def update_pop(self):
        """Update the popup."""
        self.constructor.update_db()
        # State - ON or OFF
        if GPIO.input(self.constructor.o3_pin) == self.constructor.db['ON']:
            self.var1 = 'ON'
        elif GPIO.input(self.constructor.o3_pin) == self.constructor.db['OFF']:
            self.var1 = 'OFF'
        self.var2 = self.constructor.db['o3_op_time'][0]
        self.var3 = self.constructor.db['steri_time'][3]
        self.lbl1['text'] = self.var1
        self.lbl2['text'] = format(self.var2, '.1f')
        self.lbl3['text'] = format(self.var3, '.1f')


class O2:
    """Oxygen valve popup."""

    def __init__(self, constructor, master, width=300, height=200):
        """Constructor."""
        self.constructor = constructor
        self.master = master
        self.ima_pop_o2_open = tk.PhotoImage(
            master=self.master, data=graph.o2_open
        )
        self.ima_pop_o2_close = tk.PhotoImage(
            master=self.master,
            data=graph.o2_close
        )
        self.label = tk.Label(self.master, image=self.ima_pop_o2_close, bd=0)
        self.label.place(x=0, y=0)

        self.lbl1 = tk.Label(
            self.master,
            text='',
            bg='white',
            fg=colors.FG_COLOR,
            font=('Roboto', 10)
        )
        self.lbl1.place(x=130, y=67)

    def update_pop(self):
        """Update the popup."""
        self.constructor.update_db()
        if GPIO.input(self.constructor.o2_pin) == self.constructor.db['ON']:
            self.var1 = 'Open'
            self.label['image'] = self.ima_pop_o2_open
            self.lbl1['fg'] = colors.GREEN_COLOR
        elif GPIO.input(self.constructor.o2_pin) == self.constructor.db['OFF']:
            self.var1 = 'Closed'
            self.label['image'] = self.ima_pop_o2_close
            self.lbl1['fg'] = colors.FG_COLOR
        self.lbl1['text'] = self.var1
