# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 13:45:41 2019

@author: AC
"""

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
import board


class mainwindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.title = "MIINAHARAVA --- MIINOJA 80 KPL"
        self.setWindowTitle(self.title)
        self.initBoard()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.new_board)

    def initBoard(self):
        self.new_board = board.board(self)

if __name__ == '__main__':
    import sys
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
