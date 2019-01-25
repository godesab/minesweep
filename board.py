# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 13:44:24 2019

@author: AC
"""

from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import Qt
import tile
from random import shuffle as shuffle
import numpy as np

class board(QWidget):
    # SET player = AI DISABLED AT THE MOMENT
    def __init__(self, parent=None, cols=9, rows=9, mines=10):
        super().__init__()
        self.mines = mines
        self.rows = rows
        self.cols = cols
        self.tilew = 50
        self.tileh = 50
        self.tiles = {}
        self.initUI()
        self.initTiles()

    def initUI(self):
        self.pos_left = 250
        self.pos_right = 250
        self.margin = 5
        self.spacing = 5
        self.width = self.cols*(self.tilew)
        self.height = self.rows*(self.tileh)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.setGeometry(self.pos_left, self.pos_right, self.width, self.height)
        self.layout.setOriginCorner(Qt.TopLeftCorner)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setHorizontalSpacing(3)
        self.layout.setVerticalSpacing(3)
        self.layout.setColumnMinimumWidth(55, 55)
        self.layout.setRowMinimumHeight(55, 55)

    def initTiles(self):
        tot = self.rows*self.cols
        mine_count = self.mines
        mines = []
        for z in range(tot-mine_count):
            mines.append(0)
        for w in range(mine_count):
            mines.append(1)
        # random.shuffle
        shuffle(mines)
        idx = 0
        for i in range(0, self.cols):
            for j in range(0, self.rows):
                if mines[idx] == 0:
                    self.tiles[(i, j)] = tile.EmptyTile([i, j], self)
                    self.layout.addWidget(self.tiles[(i, j)], i, j)
                else:
                    self.tiles[(i, j)] = tile.MineTile([i, j], self)
                    self.layout.addWidget(self.tiles[(i, j)], i, j)
                idx = idx+1

    def mousePressEvent(self, event):
        pos = event.pos()
        if event.button() == Qt.LeftButton:
            if self.childAt(pos):
                childW = self.childAt(pos)
                idx = self.layout.indexOf(childW)
                self.handleLeftClick(childW, idx)

        elif event.button() == Qt.RightButton:
            if self.childAt(pos):
                childW = self.childAt(pos)
                idx = self.layout.indexOf(childW)
                self.handleRightClick(childW, idx)

    def handleLeftClick(self, tile, idx):

        pos = tile.grid
        if tile.is_mine:
            tile.check()
        else:
            try:
                adj_mines = self.check_adjacent(pos)
                if adj_mines < 1:
                    tile.set_as_empty_tile()
                else:
                    tile.set_adj_mine_count(adj_mines)
            except KeyError:
                pass

    def handleRightClick(self, tile, idx):
        if tile.markable:
            tile.mark()

    def check_adjacent(self, position):
        my_pos = position
        seq = self.directions(my_pos)
        count = 0
        for turn in seq:
            temp = turn[:]
            tpl = tuple(temp)
            try:
                cand = self.tiles[tpl]
                # IF MINE AT TILE
                if cand.is_mine:
                    count = count + 1
            except KeyError:
                pass
        return count

    def directions(self, position):
        pos             = np.array(position)
        upleft          = np.add(pos,[ 1,-1])
        up              = np.add(pos,[ 1, 0])
        upright         = np.add(pos,[ 1, 1])
        right           = np.add(pos,[ 0, 1])
        downright       = np.add(pos,[-1, 1])
        down            = np.add(pos,[-1, 0])
        downleft        = np.add(pos,[-1,-1])
        left            = np.add(pos,[ 0,-1])
        upleft_lst      = upleft.tolist()
        up_lst          = up.tolist()
        upright_lst     = upright.tolist()
        right_lst       = right.tolist()
        downright_lst   = downright.tolist()
        down_lst        = down.tolist()
        downleft_lst    = downleft.tolist()
        left_lst        = left.tolist()
        seq             = [upleft_lst,up_lst,upright_lst,right_lst,
                           downright_lst,down_lst,downleft_lst, left_lst]
        return seq