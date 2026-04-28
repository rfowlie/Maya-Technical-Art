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
        pass

    def create_layouts(self):
        pass

    def create_connections(self):
        pass

    def keyPressEvent(self, event):
        pass