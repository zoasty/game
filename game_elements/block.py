from PyQt5.QtWidgets import QLabel


class Block(QLabel):
    """Create a QLabel object with an unique ID.

    The User need to specify the size and location of the object.
    The object optional parameters are labeltext, color or/and parent object.
    The Class contains three methods to move (left, right, down)
    an Block-object.

    Required attributes are listet in init-method documentation.

    """

    def __init__(self, id,
                        width, height,
                        posx, posy,
                        labeltext=None,
                        color=None,
                        parent=None):
        """Documentary of the Block class init-method.

        Requires arguments for size, location and (unique) identification
        of Block-object. Optional parameters are label, bg color and
        parent-object.

        Args:
           id (int): unique idendification variable
           width (int): block width
           height (int): block height
           posx (int): block x-position, (0,0) is left upper corner
           posy (int): block y-position, (0,0) is left upper corner

           labeltext=None (str): block label
           color=None (str), must be RGB-Hex-String, e.g. "#FFFFFF"
           parent=None (object): parent-object

        Note:
            positioning arguments (posx, posy) are relative to parent object

        """
        super(Block, self).__init__(parent, text=labeltext)
        self.id = id
        self.color = color
        self.resize(width, height)
        self.move(posx, posy)
        if color is not None:
            self.setStyleSheet('QLabel{background-color:' + color + '}')

    def move_block_left(self, blockw, blockmatrix, col_x, col_y):
        """Move block one tile (=one block width) to the left.

        If block position is at the left border (from parent), do nothing.

        Args:
            blockw (int): blockwidth

        """
        empty = ''
        try:
            block_obstacle = blockmatrix[col_y][col_x - 1]
        except IndexError:
            block_obstacle = None

        if self.pos().x() == 0:
            print("ende spielfeld")
            pass
        elif block_obstacle is not empty:
            print("block im weg")
            pass
        else:
            self.move(self.pos().x() - blockw, self.pos().y())

    def move_block_down(self, spielfeldh, blockh,
                                    blockmatrix, col_x, col_y):
        """Move block one tile (=one block height) down.

        If block position is at the bottom border (from parent), do nothing.

        Args:
            blockh (int): block height
            spielfeldh (int): spielfeld height

        """
        empty = ''
        try:
            block_obstacle = blockmatrix[col_y + 1][col_x]
        except IndexError:
            block_obstacle = None

        if self.pos().y() == (spielfeldh - blockh):
            # print("ende spielfeld")
            pass
        elif block_obstacle is not empty:
            pass
        else:
            self.move(self.pos().x(), self.pos().y() + blockh)

    def move_block_right(self, spielfeldw, blockw,
                                    blockmatrix, col_x, col_y):
        """Move block one tile (=one block width) to the right.

        If block position is at the right border (from parent), do nothing.
        Args:
            blockw (int): block width
            spielfeldw (int): spielfeld width

        """
        empty = ''
        try:
            block_obstacle = blockmatrix[col_y][col_x + 1]
        except IndexError:
            block_obstacle = None

        if self.pos().x() == spielfeldw - blockw:
            # print("ende spielfeld")
            pass
        elif block_obstacle is not empty:
            print("block im weg")
            pass
        else:
            self.move(self.pos().x() + blockw, self.pos().y())
