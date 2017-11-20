"""Entry point module."""
import tkinter as tk
import pickle
from views import auto, home, manual, menu
from views.menu_views import (
    resetconsum,
    resettube,
    statistics,
    params,
    pub,
    changepass
)
import popups
from helpers import vkeyboard
from helpers import colors
import RPi.GPIO as GPIO
from mocks import serialthread, queue, serial


class Constructor:
    """
    App constructor.

    This is the entry point for the app.
    """

    def __init__(self, master, width, height):
        """Constructor."""
        with open('db', 'rb') as f:
            self.db = pickle.load(f)

        # First run settings
        self.db['error'][1] = False

        # Constants
        self.ON = 0
        self.OFF = 1

        # Equipments str
        self.equipments = ['feed pump',
                           'recir. pump',
                           'outlet pump',
                           'oxygen valve',
                           'ozone generator',
                           'ultraviolet lamp']

        # Main attrs
        self.master = master
        self.width = width
        self.height = height

        # Flag to ascertain which window is active
        self.global_focus = 'home'

        # GPIO
        GPIO.setmode(GPIO.BCM)
        self.feedpmp_pin = 18
        self.recirpmp_pin = 23
        self.outpmp_pin = 24
        self.o2_pin = 25
        self.o3_pin = 8
        self.uv_pin = 7
        self.reactor_llow_pin = 17
        self.reactor_lhigh_pin = 27
        self.lst_pins_out = [
            self.feedpmp_pin,
            self.recirpmp_pin,
            self.outpmp_pin,
            self.o2_pin,
            self.o3_pin,
            self.uv_pin
        ]
        self.lst_pins_in = [
            self.reactor_llow_pin,
            self.reactor_lhigh_pin
        ]
        for pin in self.lst_pins_out:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
        for pin in self.lst_pins_in:
            GPIO.setup(pin, GPIO.IN)

        # Serial
        self.queue = queue.Queue()
        self.arduino = serial.Serial('/dev/myduino', 9600)
        self.thread = serialthread.SerialThread(self.queue, self.arduino)
        self.thread.daemon = True
        self.thread.start()

        # eTape. Maximum and minimum values of the eTape sensor
        # (ADC values (possible range 0-1023))
        self.etape_max = 1023
        self.etape_min = 0

        # Button anim attrs
        self.step_anim_btn = 0
        self.t1_anim_btn = 300
        self.t2_anim_btn = 100

        # Frame anim attrs
        self.y = self.height
        self.t = 0
        self.anim_duration = 500

        # Frame instantiation
        self.homepanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.autopanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.manpanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.settingspanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.changepasspanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.vkeyboardpanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.paramspanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.resettubepanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.resetconsumpanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.statisticspanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pubpanel = tk.Frame(
            self.master,
            width=self.width,
            height=self.height,
            bd=0,
            bg=colors.BG_COLOR
        )

        # Pop-ups
        self.pop_resettubepanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_resettubepanelout = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_resetconsumpaneluv = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_resetconsumpanelo3 = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_feedtkpanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_reactorpanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_feedpmppanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_outpmppanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_recirpmppanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_uvpanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_o3panel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_o2panel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_shutdown = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_resetstatspanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_gemapanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_vapanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )
        self.pop_steripanel = tk.Frame(
            self.master,
            width=300,
            height=200,
            bd=0,
            bg=colors.BG_COLOR
        )

        # App objects
        self.homeapp = home.Winhome(self, self.homepanel)
        self.autoapp = auto.AutoView(self, self.autopanel)
        self.manapp = manual.Winman(self, self.manpanel)
        self.settingsapp = menu.Winsettings(self, self.settingspanel)
        self.changepassapp = changepass.ChangePass(self, self.changepasspanel)
        self.vkeyboardapp = vkeyboard.VKeyboard(self, self.vkeyboardpanel)
        self.paramsapp = params.Winparams(self, self.paramspanel)
        self.resettubeapp = resettube.Winresettube(self, self.resettubepanel)
        self.resetconsumapp = resetconsum.Winresetconsum(
            self,
            self.resetconsumpanel
        )
        self.statisticsapp = statistics.Winstatistics(
            self,
            self.statisticspanel
        )
        self.pubapp = pub.Winpub(self, self.pubpanel)

        # Pop-up objects
        self.pop_resettubeapp = popups.ResettubePU(
            self,
            self.pop_resettubepanel
        )
        self.pop_resettubeoutletapp = popups.ResettubeOutPU(
            self,
            self.pop_resettubepanelout
        )
        self.pop_resetconsumuvapp = popups.ResetconsumuvPU(
            self,
            self.pop_resetconsumpaneluv
        )
        self.pop_resetconsumo3app = popups.Resetconsumo3PU(
            self,
            self.pop_resetconsumpanelo3
        )
        self.pop_shutdownapp = popups.ShutdownPU(self, self.pop_shutdown)
        self.pop_feedtkapp = popups.FeedTk(self, self.pop_feedtkpanel)
        self.pop_reactorapp = popups.Reactor(self, self.pop_reactorpanel)
        self.pop_feedpmpapp = popups.FeedPmp(self, self.pop_feedpmppanel)
        self.pop_outpmpapp = popups.OutPmp(self, self.pop_outpmppanel)
        self.pop_recirpmpapp = popups.RecirPmp(self, self.pop_recirpmppanel)
        self.pop_uvapp = popups.Uv(self, self.pop_uvpanel)
        self.pop_o3app = popups.O3(self, self.pop_o3panel)
        self.pop_o2app = popups.O2(self, self.pop_o2panel)
        self.pop_resetstatsapp = popups.Resetstats(
            self,
            self.pop_resetstatspanel
        )
        self.pop_gemaapp = popups.GemaPU(self, self.pop_gemapanel)
        self.pop_vaapp = popups.VaPU(self, self.pop_vapanel)
        self.pop_steriapp = popups.SteriPU(self, self.pop_steripanel)

        # Pop anim attrs
        self.xpop = 848
        self.ypop = 140
        self.cpop = -574
        self.tpop = 0
        # self.anim_duration_pop = 500
        self.anim_duration_pop = 300  # 1000
        self.anim_duration_pop_out = 300  # 400
        self.oldframe_pop = self.homepanel

        # Place frames
        self.homepanel.place(x=0, y=0)
        self.autopanel.place(x=0, y=480)
        self.manpanel.place(x=0, y=480)
        self.settingspanel.place(x=0, y=480)
        self.changepasspanel.place(x=0, y=480)
        self.vkeyboardpanel.place(x=0, y=480)
        self.paramspanel.place(x=0, y=480)
        self.resettubepanel.place(x=0, y=480)
        self.resetconsumpanel.place(x=0, y=480)
        self.statisticspanel.place(x=0, y=480)
        self.pubpanel.place(x=0, y=480)

        # Place pop-ups
        self.pop_resettubepanel.place(x=848, y=self.ypop)
        self.pop_resettubepanelout.place(x=848, y=self.ypop)
        self.pop_feedtkpanel.place(x=848, y=self.ypop)
        self.pop_reactorpanel.place(x=848, y=self.ypop)
        self.pop_feedpmppanel.place(x=848, y=self.ypop)
        self.pop_outpmppanel.place(x=848, y=self.ypop)
        self.pop_recirpmppanel.place(x=848, y=self.ypop)
        self.pop_uvpanel.place(x=848, y=self.ypop)
        self.pop_o3panel.place(x=848, y=self.ypop)
        self.pop_o2panel.place(x=848, y=self.ypop)
        self.pop_resetstatspanel.place(x=848, y=self.ypop)
        self.pop_steripanel.place(x=848, y=self.ypop)
        self.pop_vapanel.place(x=848, y=self.ypop)
        self.pop_gemapanel.place(x=848, y=self.ypop)

        self.binds()

    def update_db(self):
        """Update DB."""
        with open('db', 'rb') as f:
            self.db = pickle.load(f)

    def save_db(self):
        """Save DB."""
        with open('db', 'wb') as f:
            pickle.dump(self.db, f)

    def binds(self):
        """Home panel bindings."""
        self.homeapp.lbl_auto.bind(
            '<Button-1>',
            lambda event,
            newfrm=self.autopanel,
            oldfrm=self.homepanel,
            lbl=self.homeapp.lbl_auto,
            ima=self.homeapp.ima_auto,
            imapush=self.homeapp.ima_auto_push,
            flag='auto',
            app=self.autoapp:
            self.anim_btn(event, newfrm, oldfrm, lbl, ima, imapush, flag, app)
        )

        self.homeapp.lbl_man.bind(
            '<Button-1>',
            lambda event,
            newfrm=self.vkeyboardpanel,
            oldfrm=self.homepanel,
            lbl=self.homeapp.lbl_man,
            ima=self.homeapp.ima_man,
            imapush=self.homeapp.ima_man_push,
            flag='kb',
            app=self.vkeyboardapp:
            self.anim_btn(event, newfrm, oldfrm, lbl, ima, imapush, flag, app)
        )

        self.homeapp.lbl_settings.bind(
            '<Button-1>',
            lambda event,
            newfrm=self.settingspanel,
            oldfrm=self.homepanel,
            lbl=self.homeapp.lbl_settings,
            ima=self.homeapp.ima_settings,
            imapush=self.homeapp.ima_settings_push,
            flag='settings',
            app=self.settingsapp:
            self.anim_btn(event, newfrm, oldfrm, lbl, ima, imapush, flag, app)
        )

        self.homeapp.lbl_shut.bind(
            '<Button-1>',
            lambda event,
            newfrm=self.pop_shutdown,
            oldfrm=self.homepanel:
            self.anim_pop(event, newfrm, oldfrm, self)
        )

        self.homeapp.lbl_steri.bind(
            '<Button-1>',
            lambda event,
            newfrm=self.pop_steripanel,
            oldfrm=self.homepanel:
            self.anim_pop(event, newfrm, oldfrm, self)
        )

        self.homeapp.lbl_va.bind(
            '<Button-1>',
            lambda event,
            newfrm=self.pop_vapanel,
            oldfrm=self.homepanel:
            self.anim_pop(event, newfrm, oldfrm, self)
        )

        self.homeapp.lbl_gema.bind(
            '<Button-1>',
            lambda event,
            newfrm=self.pop_gemapanel,
            oldfrm=self.homepanel:
            self.anim_pop(event, newfrm, oldfrm, self)
        )

    def unbinds(self):
        """Unbinds."""
        self.homeapp.lbl_auto.unbind('<Button-1>')
        self.homeapp.lbl_man.unbind('<Button-1>')
        self.homeapp.lbl_settings.unbind('<Button-1>')
        self.homeapp.lbl_shut.unbind('<Button-1>')
        self.homeapp.lbl_steri.unbind('<Button-1>')
        self.homeapp.lbl_va.unbind('<Button-1>')
        self.homeapp.lbl_gema.unbind('<Button-1>')

    # Start and animate app frames
    def anim_btn(self, event, newfrm, oldfrm, lbl, ima, imapush, flag, app):
        """Button touch animation."""
        if self.step_anim_btn == 0:
            self.unbinds()
            lbl['image'] = imapush
            self.step_anim_btn = 1
            self.master.after(
                self.t1_anim_btn,
                lambda: self.anim_btn(
                    event,
                    newfrm,
                    oldfrm,
                    lbl,
                    ima,
                    imapush,
                    flag,
                    app
                )
            )
        elif self.step_anim_btn == 1:
            lbl['image'] = ima
            self.step_anim_btn = 2
            self.master.after(
                self.t2_anim_btn,
                lambda: self.anim_btn(
                    event,
                    newfrm,
                    oldfrm,
                    lbl,
                    ima,
                    imapush,
                    flag,
                    app
                )
            )
        elif self.step_anim_btn == 2:
            lbl['image'] = imapush
            self.step_anim_btn = 3
            self.master.after(
                self.t1_anim_btn,
                lambda: self.anim_btn(
                    event,
                    newfrm,
                    oldfrm,
                    lbl,
                    ima,
                    imapush,
                    flag,
                    app
                )
            )
        else:
            self.step_anim_btn = 0
            lbl['image'] = ima
            self.show_frame(event, newfrm, oldfrm, flag, app)

    def show_frame(self, event, newfrm, oldfrm, flag, app):
        """Show frame."""
        newfrm.tkraise()
        self.global_focus = flag
        self.t = 0
        self.y = 480
        self.show_frame_after(newfrm, oldfrm, app)

    def show_frame_after(self, newfrm, oldfrm, app):
        """Show frame after."""
        if self.t <= self.anim_duration:
            self.y = self.get_y(
                self.t,
                self.height,
                -self.height,
                self.anim_duration
            )
            newfrm.place(x=0, y=self.y)
            self.t += 10
            self.master.after(
                10,
                lambda: self.show_frame_after(newfrm, oldfrm, app)
            )
        else:
            oldfrm.place(x=0, y=480)
            app.binds()
            app.inits()
            self.binds()

    # Start and animate pop-ups
    def anim_pop(self, event, newfrm, oldfrm, app):
        """Animate popups."""
        newfrm.tkraise()
        self.app_pop = app
        self.newframe_pop = newfrm
        self.oldframe_pop = oldfrm
        self.app_pop.unbinds()
        self.tpop = 0
        self.xpop = 848
        self.anim_pop_after()

    def anim_pop_after(self):
        """Animate popups (after)."""
        if self.tpop <= self.anim_duration_pop:
            self.xpop = self.get_x_elastic_out(
                self.tpop,
                self.width,
                self.cpop,
                self.anim_duration_pop
            )
            self.newframe_pop.place(x=self.xpop, y=self.ypop)
            self.tpop += 10
            self.master.after(10, self.anim_pop_after)
        else:
            self.bind_all()
            self.tpop = 0

    def anim_pop_out(self):
        """Animate popups out."""
        if self.tpop <= self.anim_duration_pop_out:
            self.unbind_all()
            self.xpop = self.get_x_back_ease_in(
                self.tpop,
                274,
                574,
                self.anim_duration_pop_out
            )
            self.newframe_pop.place(x=self.xpop, y=self.ypop)
            self.tpop += 10
            self.master.after(10, self.anim_pop_out)
        else:
            self.oldframe_pop.tkraise()
            self.newframe_pop.place(x=848, y=self.ypop)
            self.app_pop.binds()
            self.binds()
            if self.autoapp.pop_running:
                self.autoapp.pop_running = False

    def get_y(self, t, b, c, d):
        """Easing function."""
        t = t / d - 1
        return c * (t * t * t * t * t + 1) + b

    def get_x_elastic_out(self, t, b, c, d):
        """
        Ease Out Elastic.

        t - current time
        b - beginning pos
        c - change in value
        d - duration
        """
        t = t / d - 1
        return c * (t * t * t * t * t + 1) + b

    def get_x_back_ease_in(self, t, b, c, d):
        """Easing function."""
        s = 1.70158
        t = t / d
        result = c * t * t * ((s + 1) * t - s) + b
        return result

    def bind_all(self):
        """Global (app level) bindings (for pops)."""
        self.master.bind('<Button-1>', self.pop_out)

    def unbind_all(self):
        """Unbind global bindings."""
        self.master.unbind('<Button-1>')

    def pop_out(self, event):
        """Remove popup."""
        self.autoapp.pop_running = True
        self.anim_pop_out()


if __name__ == '__main__':
    root = tk.Tk()
    width = 848
    height = 480
    root.geometry('{0}x{1}+0+0'.format(width, height))
    root.config(bg='black')
    root.resizable(False, False)
    app = Constructor(root, width, height)
    root.mainloop()
