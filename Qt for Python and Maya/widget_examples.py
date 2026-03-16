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



class CustomLineEdit(QtWidgets.QLineEdit):

    # should these be global?
    enter_pressed = QtCore.Signal(str)
    return_pressed = QtCore.Signal(str)

    # function is called when this widget has focus and any key on keyboard is pressed
    # we will override this method to find the right time to fire our custom signals
    def keyPressEvent(self, arg__1):
        super().keyPressEvent(arg__1)

        if arg__1.key() == QtCore.Qt.Key_Enter:
            self.enter_pressed.emit(self.text())
        elif arg__1.key() == QtCore.Qt.Key_Return:
            self.return_pressed.emit(self.text())


class MainToolWindow(QtWidgets.QDialog):
    # create static tool name to find if it exists later
    OBJECT_NAME = "MainToolWindowExample"
    def __init__(self, parent=get_maya_main_window()):
        super().__init__(parent)

        # for macOS make window a tool to keep it in focus
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        # clamp windows possible sizes.
        self.setMinimumSize(200, 200)
        self.setMaximumSize(400, 600)

        self.setWindowTitle("Windows and Dialogs")

        # create elements
        self.btn_1 = QtWidgets.QPushButton("Button 1")
        self.btn_2 = QtWidgets.QPushButton("Button 2")
        self.btn_3 = QtWidgets.QPushButton("Button 3")
        self.btn_4 = QtWidgets.QPushButton("Button 4")
        self.btn_5 = QtWidgets.QPushButton("Button 5")
        self.btn_6 = QtWidgets.QPushButton("Button 6")
        self.btn_7 = QtWidgets.QPushButton("Button 7")
        self.btn_8 = QtWidgets.QPushButton("Button 8")

        # create connection (signal and slot)
        # signal is the clicked action of the button
        # slot is the self.close() (the close of the main widget)
        self.btn_1.clicked.connect(self.close)
        self.btn_2.clicked.connect(self.print_widget)

        # layout example 1
        self.vertical_layout = QtWidgets.QVBoxLayout()
        # set border margins
        self.vertical_layout.setContentsMargins(5, 15 ,5 ,15)
        # set default widget spacing
        self.vertical_layout.setSpacing(3)
        self.vertical_layout.addWidget(self.btn_1)
        self.vertical_layout.addWidget(self.btn_2)
        self.vertical_layout.addWidget(self.btn_3)
        self.vertical_layout.addWidget(self.btn_4)
        # a stretch widget eats up all the available space where it is positioned
        self.vertical_layout.addStretch()

        # layout example 2
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.addWidget(self.btn_5)
        self.horizontal_layout.addWidget(self.btn_6)
        self.horizontal_layout.addWidget(self.btn_7)
        self.horizontal_layout.addWidget(self.btn_8)

        self.horizontal_layout.addStretch()

        # form layout builds a standard 2 column layout, helpful for many uses
        # can be passed widgets OR layouts with addRow
        self.line_edit_1 = QtWidgets.QLineEdit()
        self.line_edit_2 = QtWidgets.QLineEdit()
        self.check_box_1 = QtWidgets.QCheckBox("Check Me!")
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow("Name", self.line_edit_1)
        # passing no name is possible
        self.form_layout.addRow("", self.check_box_1)

        # nested layouts
        # always have a main layout that parents everything and attaches to the main widget
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.horizontal_layout)
        self.main_layout.addLayout(self.vertical_layout)
        self.main_layout.addLayout(self.form_layout)

        # custom signal example
        self.cle = CustomLineEdit()
        self.cle.enter_pressed.connect(self.print_line_edit)
        self.main_layout.addWidget(self.cle)


    @QtCore.Slot()
    def print_widget(self):
        # sender() gets the widget whose signal fired this slot
        # helpful for slots that get called by multiple objects
        widget = self.sender()
        print(f"{widget}")

    def print_line_edit(self):
        print(self.cle.text())



# QWidgets are not recognized as individual widgets normally
class MainToolWindow2(QtWidgets.QWidget):

    def __init__(self, parent=get_maya_main_window()):
        super().__init__(parent)

        # for macOS make window a tool to keep it in focus
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        # QWidget is a super of QDialog and does not set important functionality
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        # clamp windows possible sizes.
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 600)

        self.setWindowTitle("Windows and Dialogs")
        QtWidgets.QPushButton("Hello", self)


# QMainWindow has a variety of extra functionality that might be useful
class MainToolWindow3(QtWidgets.QMainWindow):

    def __init__(self, parent=get_maya_main_window()):
        super().__init__(parent)

        # for macOS make window a tool to keep it in focus
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        # QWidget is a super of QDialog and does not set important functionality
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        # clamp windows possible sizes.
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 600)

        self.setWindowTitle("Windows and Dialogs")

        # built in easy menu setups
        file_menu = self.menuBar().addMenu("File")
        file_menu.addMenu("New Scene")
        file_menu.addMenu("Open Scene")


# TODO: this is not working...
def launch():

    maya_window = get_maya_main_window()
    window = maya_window.findChild(QtWidgets.QWidget, MainToolWindow.OBJECT_NAME)
    if window:
        window.close()
        window.delete()
        return

    tool = MainToolWindow(parent=maya_window)
    tool.show()


if __name__ == "__main__":
    launch()