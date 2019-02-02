# -*- coding: utf-8 -*-


class DummyTile:

    def __init__(self, pos, label=None):
        self.pos = pos
        # Label tells adjacent mine count for this tile. Int between 0...8 or None if unknown
        self.label = label
        self.checked = False
        self.marked = False
        self.adj_mines = None
        self.adj_tiles = 0
        self.adj_checked = 0
        self.adj_unchecked = None

    def set_label(self, label):
        self.label = label
        self.checked = True

    def set_adj_mines(self, count):
        self.adj_mines = count
        self.checked = True

    def set_adj_tiles(self, count):
        self.adj_tiles = count

    def set_adj_checked(self, count):
        self.adj_checked = count

    def add_adj_checked(self):
        self.adj_checked = self.adj_checked + 1

    def set_adj_unchecked(self,  count):
        self.adj_unchecked = count

    def mark(self):
        self.marked = True
