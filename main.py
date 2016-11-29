from Lib.copy import copy
import random
import sys
import time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

from game_elements.block import Block
from game_elements.pushbutton import PushButton
from game_elements.widget import Widget
from game_elements.time_display import TimeDisplay


class Game(QWidget):
    """Missing Docstring."""

    def __init__(self, parent=None):
        """Missing Docstring."""
        super(Game, self).__init__(parent)

        # Block size and numbers of tiles
        self.blockw = 100
        self.blockh = 100
        self.cols = 4
        self.rows = 6

        # Game settings
        self.speed = 1000       # Time in ms within a block stays in a box
        self.blockposx = self.blockw * (self.cols - 2)
        self.blockposy = 0
        self.colorlist = ("#FF0000", "#FF9900", "#FFFF00", "#FFFF99")
        self.block_id = 0

        # Timer
        self.timer_move_block_down = QTimer()

        # List of blocks to store block-objects
        self.blocklist = []

        # Matrix of game field dimension, storing block positions with their ID
        self.empty_entry = ''
        self.blockmatrix = [
            [self.empty_entry for x in range(self.cols)] for y in range(self.rows)] # noqa
        self.blockcolorlist = []

        # Current block object
        self.current_block = None
        self.pos_x = -1
        self.pos_y = -1
        self.pos_y_storage = copy(self.pos_y)

        # Window settings
        self.gamew = self.blockw * (self.cols + 1)
        self.gameh = self.blockh * self.rows
        self.gameposx = 100
        self.gameposy = 100
        self.gamebg = "rgb(0, 170, 127)"

        # UI
        self.init_ui()

    def init_ui(self):
        """Create the user interface."""
        # Window
        self.resize(self.gamew, self.gameh)
        self.move(self.gameposx, self.gameposy)
        self.setWindowTitle('Game: The Most Desired Block')
        self.setStyleSheet("background-color: " + self.gamebg)

        # Spielfeld
        self.spielfeldw = self.blockw * self.cols
        self.spielfeldh = self.blockh * self.rows
        spielfeldcolor = "rgb(0,0,0)"
        self.spielfeld = Widget(
            self.spielfeldw, self.spielfeldh,
            spielfeldcolor, parent=self)

        # Display: Played Time
        timerw = self.blockw
        timerh = self.blockh / 2
        timerposx = self.blockw * self.cols
        timerposy = self.blockh * self.rows
        self.played_time_display = TimeDisplay(
            timerw, timerh, timerposx, timerposy, digits=5, parent=self)

        # Start Button
        sbuttonw = self.blockw
        sbuttonh = self.blockh / 2
        sbuttonposx = self.blockw * self.cols
        sbuttonposy = self.blockh * (self.rows - 5)
        self.start_button = PushButton(sbuttonw, sbuttonh,
                                                    sbuttonposx, sbuttonposy,
                                                    self.start_game,
                                                    labeltext="Start Game",
                                                    color=None,
                                                    parent=self)

        # Cancel Button
        cbuttonw = self.blockw
        cbuttonh = self.blockh / 2
        cbuttonposx = self.blockw * self.cols
        cbuttonposy = self.blockh * (self.rows - 1)
        self.cancel_button = PushButton(cbuttonw, cbuttonh,
                                                    cbuttonposx, cbuttonposy,
                                                    self.close,
                                                    labeltext='Exit Game',
                                                    parent=self)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.played_time_display)
        vbox.addWidget(self.start_button)
        vbox.addStretch(self.rows - 3)
        vbox.addWidget(self.cancel_button)
        hbox = QHBoxLayout()
        hbox.addWidget(self.spielfeld, stretch=self.cols + 1)
        hbox.addLayout(vbox, stretch=1)
        self.setLayout(hbox)

    def start_game(self):
        """Start Timer. Create first block. Create blocks within interval."""
        # Start the display timer
        self.played_time_display.time_counter(display_format="mm:ss")

        # Call create_new_block function for the first time
        self.create_new_block()

        # block shall fall down
        self.block_fall_down_timer()

    def create_new_block(self):
        """Create a colored block and gives it a uniqed ID."""
        # Each block gets a random color out of a given colorpool
        color = random.choice(self.colorlist)

        # Create block
        # todo für wartungsarbeiten hier ein print
        # print("Blockmatrix vor letztem Create Block:")
        # for i in range(0, 6):
        #    print(self.blockmatrix[i])
        self.block = Block(
            self.block_id, self.blockw, self.blockh,
            self.blockposx, self.blockposy,
            parent=self, color=color)
        self.block.show()
        self.set_current_block(self.block)
        self.block_id += 1

    def block_fall_down_timer(self):
        """Move block in y direction with given.

        intervall & a num of steps.
        Args:
            spielfeldh (int): spielfeld height.
        """
        # Timer with certain interval to move a block one tile down
        self.timer_move_block_down.timeout.connect(
            self.if_possible_move_block_down)
        self.timer_move_block_down.start(self.speed)

    def if_possible_move_block_down(self):
        """Missing Docstring."""
        # self.current_block = self.block

        # set block position relative to matrix to self.cols
        self.set_blockmatrix_position()

        # if block at the end of game field height
        if self.current_block.pos().y() == self.spielfeldh - self.blockh:
            # save block position in matrix
            self.write_block_into_blockmatrix()
            self.create_new_block()

        # elif matrix entry below is empty
        elif self.blockmatrix[self.pos_y + 1][self.pos_x] == '':
            self.current_block.move_block_down(
                self.spielfeldh, self.blockh,
                self.blockmatrix,
                self.pos_x, self.pos_y)
            # move block one down
            # TODO

        else:
            # self.blockmatrix[self.pos_y][self.pos_x] = block
            # print(self.blockmatrix)
            # self.create_new_block()

            # get block of matrix entry below
            block_below = self.blockmatrix[self.pos_y + 1][self.pos_x]
            # check color
            block_below_color = block_below.color
            block_color = self.current_block.color

            # if color is identical
            # proof_color_in_y
            if block_color == block_below_color:
                # if color is the last color in colorlist, do nothing
                if block_color == self.colorlist[len(self.colorlist) - 1]:
                    # save block position in matrix
                    self.blockmatrix[self.pos_y][self.pos_x] = self.current_block  # noqa
                    # create new block
                    self.create_new_block()

                # remove block object
                # self.block.close()
                else:
                    if self.blockmatrix[self.pos_y][self.pos_x] is not '':
                        self.blockmatrix[self.pos_y][self.pos_x] = ''
                    self.current_block.close()
                    # set block below to current block
                    self.set_current_block(block_below)

                    self.change_block_color()
                    self.if_possible_move_block_down()

            else:
                # save block position in matrix
                self.write_block_into_blockmatrix()
                # create new block
                self.create_new_block()

    def set_current_block(self, block): # noqa
        self.current_block = block

    def set_blockmatrix_position(self):  # noqa
        self.pos_x = int(self.current_block.pos().x() / self.blockw)
        self.pos_y = int(self.current_block.pos().y() / self.blockh)

    def write_block_into_blockmatrix(self):  # noqa
        self.blockmatrix[self.pos_y][self.pos_x] = self.current_block
        # Check if row is complete
        self.check_win_condition()

    def change_block_color(self):  # noqa
        color_pos_in_list = self.colorlist.index(self.current_block.color)
        try:
            color = self.colorlist[color_pos_in_list + 1]
            self.current_block.setStyleSheet(
                'QLabel{background-color:' + color + '}')
            self.current_block.color = color
        except IndexError:
            pass

    def check_win_condition(self):  # noqa

        # Check rowentries on self.pos_y. All blocks?
        if all(self.blockmatrix[self.pos_y]) is True:
            self.create_blockcolorlist(self.pos_y)

            # Check if colors in self.blockcolorlist are identical
            print(set(self.blockcolorlist))
            if len(set(self.blockcolorlist)) == 1:
                print("Win Condition!")
                self.remove_rowblocks(self.pos_y)
                self.pull_blocks_down()
            else:
                # print("colors in self.blockcolorlist are not identical.")
                pass
        else:
            # print("There is an empty entry in the row.")
            pass

    def create_blockcolorlist(self, pos_y):  # noqa
        self.blockcolorlist = []
        for pos_x in range(self.cols):
            self.blockcolorlist.append(self.blockmatrix[pos_y][pos_x].color)

    def remove_rowblocks(self, pos_y):  # noqa
        print("Remove Rowblocks!")
        print("blockmatrix_before:")
        for i in range(0, 6):
            print(self.blockmatrix[i])
        for pos_x in range(self.cols):
            # print("remove block ", pos_x)
            self.blockmatrix[pos_y][pos_x].close()
            self.blockmatrix[pos_y][pos_x] = self.empty_entry
        print("blockmatrix_after:")
        for i in range(0, 6):
            print(self.blockmatrix[i])

    def pull_blocks_down(self):  # noqa
        print("Pull Blocks Down!")
        # Recursivly go to the right of the self.blockmatrix
        self.pos_x = 0
        self.pos_y_storage = copy(self.pos_y)
        while self.pos_x < self.cols:
            print("while loop pos_x:", self.pos_x)
            # Recursivly go to the top of the self.blockmatrix
            while self.pos_y > 0:
                print("while loop pos_y:", self.pos_y, "\t pos_y_storage:", self.pos_y_storage) # noqa
                if self.blockmatrix[self.pos_y - 1][self.pos_x] is self.empty_entry: # noqa
                    print("empty entry above")
                    self.pos_y -= 1
                else:
                    print("block above!")
                    self.blockmatrix_update(self.pos_x, self.pos_y)
                    self.check_block_fusion()
                    # To iterate same column again
                    self.pos_x -= 1
                    # self.pos_y = self.pos_y_storage
                    break
            self.pos_x += 1
            self.pos_y = self.pos_y_storage

    def blockmatrix_update(self, pos_x, pos_y):  # noqa
        print("Blockmatrix update!")
        # Move block one tile down
        # QLabel
        # block_pos_x = self.blockmatrix[pos_y - 1][pos_x].pos().x()
        # block_pos_y = self.blockmatrix[pos_y - 1][pos_x].pos().y()
        print("pos_x, pos_y:", pos_x, pos_y)
        print("block to move down (pos_y - 1", pos_y - 1, ") = ", self.blockmatrix[pos_y - 1][pos_x]) # noqa
        self.blockmatrix[pos_y - 1][pos_x].move_block_down(
            self.spielfeldh, self.blockh, self.blockmatrix, self.pos_x,
            self.pos_y - 1)
        # def move_block_down(self, spielfeldh, blockh,
        #                             blockmatrix, col_x, col_y):
        # self.blockmatrix[pos_y - 1][pos_x].move(block_pos_x, block_pos_y + self.blockh) # noqa
        # Entry
        self.blockmatrix[pos_y][pos_x] = self.blockmatrix[pos_y - 1][pos_x] # noqa
        # Set an empty entry at position of moved block
        self.blockmatrix[pos_y - 1][pos_x] = self.empty_entry

        # time.sleep(5555)

    def check_block_fusion(self):  # noqa
        try:
            if self.blockmatrix[self.pos_y][self.pos_x] == self.blockmatrix[self.pos_y + 1][self.pos_x]: # noqa
                self.blockmatrix_update(self.pos_x, self.pos_y + 1)
                # block_change_color()

                self.create_blockcolorlist(self.pos_y + 1)
                # Check if colors in self.blockcolorlist are identical
                if len(set(self.blockcolorlist)) <= 1 is True:
                    self.remove_rowblocks(self.pos_y + 1)
                    self.pos_y_storage -= 1
        except IndexError:
            print("y max reached")
            pass

    def keyPressEvent(self, key_event):  # noqa
        '''If a key on keyboard is pressed, one of the following events happens
        Events:
        Press "A": block will move one tile to the left
        Press "S": block will move one tile down
        Press "D": block will move one tile to the right
        Press "Esc": Application will shut down'''

        # set block position relative to matrix to self.cols
        self.set_blockmatrix_position()

        if key_event.key() == (Qt.Key_A or Qt.Key_Left):
            self.current_block.move_block_left(
                self.blockw,
                self.blockmatrix,
                self.pos_x, self.pos_y)

        if key_event.key() == (Qt.Key_S or Qt.Key_Down):
            self.current_block.move_block_down(
                self.spielfeldh, self.blockh,
                self.blockmatrix,
                self.pos_x, self.pos_y)

        if key_event.key() == (Qt.Key_D or Qt.Key_Right):
            self.current_block.move_block_right(
                self.spielfeldw, self.blockw,
                self.blockmatrix,
                self.pos_x, self.pos_y)

        if key_event.key() == Qt.Key_Escape:
            self.close()

app = QApplication(sys.argv)
game = Game()
game.show()
sys.exit(app.exec_())
