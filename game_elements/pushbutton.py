from PyQt5.QtWidgets import QPushButton


class PushButton(QPushButton):
    """"Blank Push Button. Documentary in __init__."""

    def __init__(self,
                        width, height,
                        posx, posy,
                        action,
                        labeltext=None,
                        color=None,
                        parent=None):
        """Documentary of the Block class init-method.

        Requires arguments for size, location and action of Block-object.
        Optional parameters are label, bg color and parent-object.
        When Button is pressed, the action function will be called.

        Args:
            width (int): block width
            height (int): block height
            posx (int): block x-position, (0,0) is left upper corner
            posy (int): block y-position, (0,0) is left upper corner
            action (func): function, which is called when button was pressed
            labeltext=None (str): block label
            color=None (str), must be RGB-Hex-String, e.g. ("#FFFFFF")
            parent=None (object): parent-object

        Note:
            positioning arguments (posx, posy) are relative to parent object

        """
        super(QPushButton, self).__init__(parent, text=labeltext)
        self.resize(width, height)
        self.move(posx, posy)
        if color is not None:
            self.setStyleSheet('QLabel{background-color:' + color + '}')

        self.clicked.connect(action)
