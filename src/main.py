#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from src.MainWindow import MainWindow

def main():
    app = QApplication([])
    ex=MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
