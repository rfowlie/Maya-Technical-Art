import sys

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui
import shiboken6

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui


# work around for grabbing maya main window as obj
def get_maya_main_window():
    # C++ pointer to the maya main window
    main_window_ptr = omui.MQtUtil.mainWindow()
    # making the pointer into a Qtwidget...
    return shiboken6.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class OpenImportTool(QtWidgets.QDialog):

    # singleton setup is helpful for active release tools
    __instance = None
    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = OpenImportTool()

        if cls.__instance.isHidden():
            cls.__instance.show()
        else:
            cls.__instance.raise_()
            cls.__instance.activateWindow()


    WIDGET_NAME = "OpenImportDialog"
    FILE_FILTERS = "Maya (*.ma, *mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
    SELECTED_FILTER = "Maya (*.ma, *mb)"

    def __init__(self, parent=get_maya_main_window()):
        super(OpenImportTool, self).__init__(parent)

        # for macOS make window a tool to keep it in focus
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        self.setWindowTitle("Open Import Dialog")
        self.setMinimumSize(400, 100)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.lineEdit_filepath = QtWidgets.QLineEdit()
        self.button_filepath = QtWidgets.QPushButton()
        # the special file path here means it is a file in maya resources
        self.button_filepath.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.radioButton_open = QtWidgets.QRadioButton("Open")
        self.radioButton_import = QtWidgets.QRadioButton("Import")
        self.radioButton_reference = QtWidgets.QRadioButton("Reference")
        self.radioButton_open.setChecked(True)
        self.checkBox_force = QtWidgets.QCheckBox("Force")
        self.button_apply = QtWidgets.QPushButton("Apply")
        self.button_close = QtWidgets.QPushButton("Close")


    def create_layouts(self):
        # create sub layouts then main
        filepath_layout = QtWidgets.QHBoxLayout()
        filepath_layout.addWidget(self.lineEdit_filepath)
        filepath_layout.addWidget(self.button_filepath)

        radioButton_layout = QtWidgets.QHBoxLayout()
        radioButton_layout.addWidget(self.radioButton_open)
        radioButton_layout.addWidget(self.radioButton_import)
        radioButton_layout.addWidget(self.radioButton_reference)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("File Path", filepath_layout)
        form_layout.addRow("", radioButton_layout)
        form_layout.addRow("", self.checkBox_force)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.button_apply)
        button_layout.addWidget(self.button_close)

        # main layout connect all layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.button_filepath.clicked.connect(self.show_file_select_dialog)
        self.radioButton_open.toggled.connect(self.set_force_checkBox_visibility)
        self.button_apply.clicked.connect(self.load_file)
        self.button_close.clicked.connect(self.close)

    def show_file_select_dialog(self):
        # get important maya file paths and locations with this
        file_path = self.lineEdit_filepath.text()
        if not file_path:
            file_path = cmds.internalVar(userAppDir=True)

        # can set the file types available for the open
        # the second variable will be updated according to the actions taken by the user in the open file widget
        file_path, self.SELECTED_FILTER = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select File",
            file_path,
            self.FILE_FILTERS,
            self.SELECTED_FILTER
        )

        print(file_path)
        if file_path:
            self.lineEdit_filepath.setText(file_path)

    def set_force_checkBox_visibility(self):
        self.checkBox_force.setVisible(self.radioButton_open.isChecked())

    def load_file(self):
        file_path = self.lineEdit_filepath.text()
        if not file_path:
            return

        # QFilePath provides useful functions regarding file paths
        file_info = QtCore.QFileInfo(file_path)
        if not file_info.exists():
            om.MGlobal.displayError("File does not exist")

        if self.radioButton_open.isChecked():
            self.open_file(file_path)
        elif self.radioButton_import.isChecked():
            self.import_file(file_path)
        elif self.radioButton_reference.isChecked():
            self.reference_file(file_path)

    def open_file(self, file_path):
        # check if current open file has changes
        force = False
        if not cmds.file(q=True, modified=True) and self.checkBox_force.isChecked():
            result = QtWidgets.QMessageBox.question(
                self,
                "Modified",
                "current scene has unchanged changes. Continue?")
            if result == QtWidgets.QMessageBox.StandardButton.Yes:
                force = True
            else:
                return

        cmds.file(file_path, open=True, force=force)

    def import_file(self, file_path):
        # import keyword causes issues with actual python import keyword so use short form
        cmds.file(file_path, i=True, ignoreVersion=True)

    def reference_file(self, file_path):
        cmds.file(file_path, reference=True, ignoreVersion=True)


    # util change
    # unless handled key presses get passed up to the parent widget
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

    launch(OpenImportTool)