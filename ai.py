# -*- coding: utf-8 -*-

import random
import numpy as np
import DummyTile as dt


class AI:

    def __init__(self, playboard=None):
        # Playboard size and mine count
        self.playboard = playboard
        self.rows = 1
        self.cols = 1
        self.mines = 0
        self.total_tiles = self.rows * self.cols
        # AI action count related
        self.initial_action = True
        self.tiles_opened = 0
        # Mine probability array for all tiles in playboard
        self.mines_found = 0
        # Lists
        self.tiles = {}
        self.mine_list = []
        self.mine_marked_list = []
        self.clicked = []
        self.label_tiles = []
        self.init_stuff()
        # Flags
        self.new_mine_flag = False
        self.new_empty_flag = False

    def init_stuff(self):
        self.init_playboard()

    def init_playboard(self):
        if self.playboard is not None:
            self.rows = self.playboard.rows
            self.cols = self.playboard.cols
            self.mines = self.playboard.mines
            self.total_tiles = self.rows * self.cols
            for x in range(self.rows):
                for y in range(self.cols):
                    self.tiles[(x, y)] = dt.DummyTile((x, y))
                    tile = self.tiles[(x, y)]
                    adj_tiles = self.check_adj_tile_count((x, y))
                    tile.set_adj_tiles(adj_tiles)
                    tile.set_adj_unchecked(adj_tiles)
        else:
            print('Playboard not set. Use set_playboard function to set one')

    def set_playboard(self, playboard):
        if self.playboard is None:
            self.playboard = playboard

    def play(self):
        if self.initial_action:
            self.initial_action = False
            self.click_tile((self.random_pos()))
        elif self.new_mine_flag:
            self.mark_mines()
        elif self.new_empty_flag:
            self.handle_empty_tile_que()
        else:
            self.detect_mines()
            self.update_board_state()
            # TODO: PRESS TILE WITH LOWEST PROBABILITY
            if not self.new_mine_flag:
                self.click_tile((self.random_pos()))
        self.update_board_state()

    def click_tile(self, pos):
        # BOARD GIVES TILE'S ADJACENT MINE COUNT (eg. 0, 1 or 2 etc.)
        result = self.playboard.ai_press_event(pos)
        self.tiles_opened = self.tiles_opened + 1
        self.handle_result(pos, result)

    def handle_result(self, pos, result):
        x, y = pos
        if pos not in self.clicked:
            self.clicked.append(pos)
        label = result
        tile = self.tiles[(x, y)]
        tile.set_label(label)
        if label is 0:
            self.new_empty_flag = True
        elif label > 0:
            self.label_tiles.append((x, y))
        self.update_board_state()

    def handle_empty_tile_que(self):
        que = []
        for x in range(self.rows):
            for y in range(self.cols):
                pos = (x, y)
                tile = self.tiles[pos]
                if tile.checked:
                    seq1 = self.directions(pos)
                    seq2 = self.directions(pos)
                    if tile.label is 0:
                        for elem in seq1:
                            if elem not in que and elem not in self.clicked:
                                que.append(elem)
                    elif tile.label > 0:
                        if tile.label == tile.adj_mines:
                            for e in seq2:
                                if e not in que and e not in self.clicked and e not in self.mine_list:
                                    que.append(e)
        if len(que) > 0:
            i = len(que)
            r = random.randint(0, i-1)
            r_pos = que[r]
            x, y = r_pos
            self.click_tile((x, y))
        else:
            self.new_empty_flag = False

    def update_board_state(self):
        # UPDATE AVAILABLE INFORMATION ABOUT PLAYBOARD STATE
        for pos in self.label_tiles:
            count = 0
            mine_count = 0
            tile = self.tiles[pos]
            seq = self.directions(pos)
            # LOOK FOR CLICKED TILES AROUND
            for adj_tile in seq:
                if adj_tile in self.clicked or adj_tile in self.mine_marked_list:
                    count = count + 1
                if adj_tile in self.mine_list:
                    mine_count = mine_count + 1
            total = tile.adj_tiles
            unchecked = total - count
            tile.set_adj_unchecked(unchecked)
            tile.set_adj_checked(count)
            tile.set_adj_mines(mine_count)
            if tile.label == tile.adj_mines and tile.adj_unchecked > 0:
                self.new_empty_flag = True

    def playboard_seq(self):
        # TODO CHANGE TO INIT FUNCTION WITH NO RETURN VALUE
        seq = []
        for x in range(self.rows):
            for y in range(self.cols):
                seq.append((x, y))
        return seq

    def directions(self, position):
        # CREATE OWN CLASS
        limit_r = self.rows
        limit_c = self.cols
        pos = np.array(position)
        upleft = np.add(pos, [1, -1])
        up = np.add(pos, [1, 0])
        upright = np.add(pos, [1, 1])
        right = np.add(pos, [0, 1])
        downright = np.add(pos, [-1, 1])
        down = np.add(pos, [-1, 0])
        downleft = np.add(pos, [-1, -1])
        left = np.add(pos, [0, -1])
        upleft_lst = upleft.tolist()
        up_lst = up.tolist()
        upright_lst = upright.tolist()
        right_lst = right.tolist()
        downright_lst = downright.tolist()
        down_lst = down.tolist()
        downleft_lst = downleft.tolist()
        left_lst = left.tolist()
        seq = [upleft_lst, up_lst, upright_lst, right_lst,
               downright_lst, down_lst, downleft_lst, left_lst]
        ret = []
        for lst in seq:
            if lst[0] >= 0 and lst[1] >= 0:
                if lst[0] < limit_r and lst[1] < limit_c:
                    ret.append(tuple(lst))
        return ret

    def random_pos(self):
        x = random.randint(0, self.cols-1)
        y = random.randint(0, self.rows-1)
        return x, y

    def detect_mines(self):
        for pos in self.label_tiles:
            x, y = pos
            tile = self.tiles[x, y]
            label = tile.label
            seq = self.directions(pos)
            adj_unchecked = tile.adj_unchecked
            adj_mines = tile.adj_mines
            if adj_mines is 0 and label == adj_unchecked:
                # MINE DETECTED
                for cand in seq:
                    if self.tiles[cand].checked is False and cand not in self.mine_list:
                        self.mine_list.append(cand)
                        self.new_mine_flag = True
            elif adj_mines > 0:
                if (label - adj_mines) == adj_unchecked:
                    for unc in seq:
                        if self.tiles[unc].checked is False and unc not in self.mine_list:
                            self.mine_list.append(unc)
                            self.new_mine_flag = True

    def mark_mines(self):
        for mine in self.mine_list:
            if mine not in self.clicked and mine not in self.mine_marked_list:
                self.mine_marked_list.append(mine)
                self.tiles[mine].mark()
                self.playboard.ai_mark_mine(mine)
        if len(self.mine_marked_list) < len(self.mine_list):
            self.new_mine_flag = True
        else:
            self.new_mine_flag = False

    def check_adj_tile_count(self, pos):
        MAX_X = self.rows-1
        MAX_Y = self.cols-1
        if pos is not None:
            # TILE IS IN A CORNER
            if (pos == (0, 0) or pos == (0, MAX_Y) or
                    pos == (MAX_X, 0) or pos == (MAX_X, MAX_Y)):
                return 3
            # TILE IS AT AN EDGE
            elif pos[0] == 0 or pos[0] == MAX_X and pos[1] > 0 and pos[1] < MAX_Y:
                return 5
            elif pos[1] == 0 or pos[1] == MAX_Y and pos[0] > 0 and pos[0] < MAX_X:
                return 5
            else:
                return 8

