import sys

from PySide6 import QtCore
from PySide6 import QtWidgets
import shiboken6

import maya.cmds as cmds
import maya.OpenMayaUI as omui


# work around for grabbing maya main window as obj
def get_maya_main_window():
    # C++ pointer to the maya main window
    main_window_ptr = omui.MQtUtil.mainWindow()
    # making the pointer into a Qtwidget...
    return shiboken6.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class TableWidgetExample(QtWidgets.QDialog):

    def __init__(self, parent=get_maya_main_window()):
        super(TableWidgetExample, self).__init__(parent)

        # for macOS make window a tool to keep it in focus
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        self.setWindowTitle("Table Widget Example")
        self.setMinimumSize(400, 100)


    def create_actions(self):
        pass

    def create_widgets(self):
        self.widget_table = QtWidgets.QTableWidget()
        self.widget_table.setColumnCount(5)
        self.widget_table.setColumnWidth(0, 25)
        self.widget_table.setColumnWidth(2, 75)
        self.widget_table.setColumnWidth(3, 75)
        self.widget_table.setColumnWidth(4, 75)
        # set this column to stretch and fill remaining space
        self.widget_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.widget_table.setHorizontalHeaderLabels([
            "", "Name", "Tx", "Ty", "Tz"
        ])



    def create_layouts(self):
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.setContentsMargins(3,3,3,3)
        self.layout_main.setSpacing(5)
        self.layout_main.addWidget(self.widget_table)

    def create_connections(self):
        pass

    def keyPressEvent(self, event):
        pass




def launch(cls):
    maya_window = get_maya_main_window()
    window = maya_window.findChild(QtWidgets.QWidget, cls.WIDGET_NAME)
    if window:
        window.close()
        window.deleteLater()

    tool = cls()
    tool.show()


if __name__ == "__main__":
    launch(TableWidgetExample)
