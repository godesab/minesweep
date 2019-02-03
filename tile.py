# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class BaseTile(QLabel):
    def __init__(self, grid=None, parent=None):
        super().__init__()
        # TILE ICONS
        self.baseicon = QPixmap('img//basetile_50.png')
        self.markicon = QPixmap('img//marktile_50.png')
        self.boomicon = QPixmap('img//boomtile_50.png')
        self.emptyicon = QPixmap('img//emptytile_50.png')
        self.tile1_icon = QPixmap('img//1_tile_50.png')
        self.tile2_icon = QPixmap('img//2_tile_50.png')
        self.tile3_icon = QPixmap('img//3_tile_50.png')
        self.tile4_icon = QPixmap('img//4_tile_50.png')
        self.tile5_icon = QPixmap('img//5_tile_50.png')
        self.tile6_icon = QPixmap('img//6_tile_50.png')
        self.tile7_icon = QPixmap('img//7_tile_50.png')
        self.tile8_icon = QPixmap('img//8_tile_50.png')
        self.setPixmap(self.baseicon)
        # grid means x,y position on grid. To be changed (pos() is QObject attribute alrdy)
        self.grid = grid
        # BOOLEAN STATES
        self.markable = True
        self.checked = False
        self.marked = False

    def check_adj_tile_count(self):
        # TODO CURRENTLY NOT WORKING WITH BIGGER PLAYBOARDS
        if self.grid is not None:
            # TILE IS IN A CORNER
            if (self.grid == (0, 0) or self.grid == (0, 8) or
                    self.grid == (8, 0) or self.grid == (8, 8)):
                return 3
            # TILE IS AT AN EDGE
            elif self.grid[0] == 0 or self.grid[0] == 8 and self.grid[1] > 0 and self.grid[1] < 8:
                return 5
            elif self.grid[1] == 0 or self.grid[1] == 8 and self.grid[0] > 0 and self.grid[0] < 8:
                return 5
            else:
                return 8

    def __repr__(self):
        return "JustATile"

    def check(self):
        # OVERRIDE IN SUBCLASS
        pass

    def mark(self):
        if self.markable:
            # MARK TILE
            if self.marked is False:
                self.setPixmap(self.markicon)
                self.marked = True
            # UNMARK TILE
            elif self.marked is True:
                self.setPixmap(self.baseicon)
                self.marked = False


class EmptyTile(BaseTile):

    def __init__(self, grid, parent=None):
        super().__init__()
        self.is_mine = False
        self.adj_mines = None
        self.adj_empty = None
        self.grid = grid
        self.adj_tiles = self.check_adj_tile_count()

    def set_adj_mine_count(self, count):
        self.adj_mines = count
        self.checked = True
        self.markable = False
        if count == 1:
            self.set_1_tile()
        elif count == 2:
            self.set_2_tile()
        elif count == 3:
            self.set_3_tile()
        elif count == 4:
            self.set_4_tile()
        elif count == 5:
            self.set_5_tile()
        elif count == 6:
            self.set_6_tile()
        elif count == 7:
            self.set_7_tile()
        elif count == 8:
            self.set_8_tile()
        else:
            print('WEIRD TILE COUNT ERROR:', count)

    def set_as_empty_tile(self):
        self.markable = False
        if self.checked is False:
            self.setPixmap(self.emptyicon)
        self.checked = True
        self.adj_mines = 0

    def set_1_tile(self):
        self.setPixmap(self.tile1_icon)

    def set_2_tile(self):
        self.setPixmap(self.tile2_icon)

    def set_3_tile(self):
        self.setPixmap(self.tile3_icon)

    def set_4_tile(self):
        self.setPixmap(self.tile4_icon)

    def set_5_tile(self):
        self.setPixmap(self.tile5_icon)

    def set_6_tile(self):
        self.setPixmap(self.tile6_icon)

    def set_7_tile(self):
        self.setPixmap(self.tile7_icon)

    def set_8_tile(self):
        self.setPixmap(self.tile8_icon)


class MineTile(BaseTile):

    def __init__(self, grid, parent=None):
        super().__init__()
        self.is_mine = True
        self.adj_tiles = self.check_adj_tile_count()
        self.adj_empty = None
        self.adj_mines = None
        self.grid = grid
        self.adj_tiles = self.check_adj_tile_count()

    def check(self):
        if self.checked is False and self.marked is False:
            self.setPixmap(self.boomicon)
            print('###MINE PRESSED at POS##: ', self.grid)
            self.checked = True
            self.markable = False
