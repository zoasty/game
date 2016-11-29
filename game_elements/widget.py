from PyQt5.QtWidgets import QWidget


class Widget(QWidget):
    """Create a QWidget object.

    The __init__ method is documented in the class level docstring.

    Args:
        width (int): widget width
        height (int): widget heigt

        posx=None (int): widget x-position, (0,0) is left upper corner
        posy=None (int): widget y-position, (0,0) is left upper corner
        color=None, must be RGB-String,e.g. "rgb(0,0,0)", bg color
        parent=None (object): parent-object

    Note:
        positioning arguments (posx, posy) are relative to parent object

    """

    def __init__(self, width, height, color, parent=None):  # noqa
        super(Widget, self).__init__(parent=parent)
        this_widget = QWidget(parent)
        this_widget.resize(width, height)
        this_widget.setStyleSheet("background-color:" + color)
