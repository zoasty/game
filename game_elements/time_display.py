from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QLCDNumber


class TimeDisplay(QLCDNumber):
    """Create QLCDNumber object to display a time.

    Includes:
        Method current_time() to show the current system time.
        Method time_counter() to show starting timer.

    Required attributes are listet in init-method documentation.

    """

    def __init__(self,
                        width, height,
                        posx, posy,
                        digits=2,
                        parent=None):
        """Documentary of the TimeDisplay class init-method.

        Args:
            width (int): diplay width
            height (int): display height
            posx (int): display x-position, (0,0) is left upper corner
            posy (int): display y-position, (0,0) is left upper corner

            digits=2 (int): number of display digits, include separators
            parent=None (object): parent-object

        """
        super(QLCDNumber, self).__init__(digits, parent)
        self.resize(width, height)
        self.move(posx, posy)

    def current_time(self):
        """Show current system time on display.

        Function show_time() is called by a timer to show time on display.
        The timer interval is 100ms.

        """
        def show_time():
            """Show time on display.

            Note:
                function is initialized before called.

            """
            self.time = self.time.currentTime()
            self.time = self.time.toString()
            self.display(self.time)
        self.time = QTime()
        self.timer = QTimer()
        self.timer.timeout.connect(show_time)
        self.timer.start(100)

    def time_counter(self, interval=1000, display_format="hh:mm:ss.zzz"):
        """Show starting timer time on display.

        Counts from zero onwards. Like a stop watch.
        Interval and display format are optional parameters.

        Args:
            interval=1000 (int): timer interval in ms
            display_format="hh:mm:ss.zzz" (str): display format

        Note:
            Start time is displayed before timer starts, because otherwise
            the first time showed would be 00:00:01 (hh:mm:ss).

        """
        def count_time():
            """Count time within an interval and show time on display.

            Note:
                function is initialized before called.

            """
            self.time = self.time.addMSecs(interval)
            self.display(self.time.toString(display_format))

        self.time = QTime(0, 0, 0, 0)
        self.timer = QTimer()
        self.display(self.time.toString(display_format))
        self.timer.timeout.connect(count_time)
        self.timer.start(interval)
