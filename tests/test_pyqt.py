# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-22
import sys
from PyQt5 import QtWidgets, QtCore



app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()

widget.resize(400, 400)
widget.setWindowTitle("hello world")
widget.show()
sys.exit(app.exec_())