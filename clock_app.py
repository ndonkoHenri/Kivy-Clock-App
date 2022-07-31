from time import strftime
from kivy import Config

# a fixed size is set for the app's display when executed
Config.set("graphics", "height", "323")
Config.set("graphics", "width", "444")

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock




class ClockApp(MDApp):
    # Clock object for the clock(in the app) event
    event_clock = None

    def build(self):
        """
        The build function is the main entry point for the build system. It
        creates a new Builder object.
        :return: A MainScreen Object containing the main screen to the app
        """
        return MainScreen()

    def on_start(self):
        """
        The on_start function is called when the app is first opened. It creates a
        Clock event that calls the root widget's clock_update and chrono_update functions to
        update the clock and chrono in real time.
        """

        self.event_clock = Clock.schedule_interval(self.root.clock_update, 1)


class MainScreen(MDScreen):
    # Clock object for the Chrono event
    event_chrono = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.chrono_mins = 0
        self.chrono_secs = 0
        self.total_seconds = 0

    def clock_update(self, dt):
        """
        The clock_update function updates the time of the Clock in the app.
        This function is called once every second.

        :param dt: the time delta, which is approximately equal to the specified time-out (1sec in this case)
        """
        self.time_label.text = strftime('[b] %H [/b]: %M : %S %p')

    def chrono_update(self, dt):
        """
        The chrono_update function calculates the chrono_mins(number of mins since started)
        and chrono_secs(number of seconds since started) variables from the sum of ~param: dt (total_seconds)
        and then updates the text of Chrono in the app to reflect these changes.

        :param dt: Useful in updating the chrono_mins and chrono_secs variables
        """
        self.total_seconds += dt
        self.chrono_mins, self.chrono_secs = divmod(self.total_seconds, 60)

        # We update the chrono label. A
        self.ids.chrono_label.text = f"[b] {str(int(self.chrono_mins)).zfill(2)} [/b]: {str(int(self.chrono_secs)).zfill(2)}.[size=30sp]{str(int((self.chrono_secs * 100) % 100)).zfill(2)}[/size]"
        # The string function zfill() plays a significant role on the above line.
        # It adds leading Zeros accounting for a stable display.
        # Please read its documentation for more info at

    def reset_chrono(self):
        """
        Resets the Chrono and changes the start_stop_btn.text to "Start"
        """
        self.event_chrono.cancel()
        self.ids.chrono_label.text = "[b] 00 [/b]: 00.[size=30sp]00[/size]"
        self.total_seconds = 0
        self.ids.start_stop_btn.text = "Start"

    def start_stop_chrono(self):
        """
        Starts or Stops the Chrono depending on the Text in the Button(start_stop_btn)
        and equally changes it(the text) accordingly
        """
        if self.ids.start_stop_btn.text == "Start":
            self.event_chrono = Clock.schedule_interval(self.chrono_update, 0.042)
            self.ids.start_stop_btn.text = "Stop"
        else:
            self.event_chrono.cancel()
            self.ids.start_stop_btn.text = "Start"


if __name__ == "__main__":
    from kivy.core.text import LabelBase

    # Register the different font files(.ttf) to the LabelBase with a specific font_name
    # for easy referencing in both the .kv and .py files

    LabelBase.register(
        name="Roboto",
        fn_regular="assets/fonts/Roboto-Thin.ttf",
        fn_bold="assets/fonts/Roboto-Medium.ttf"
    )
    # Run the App
    ClockApp().run()
