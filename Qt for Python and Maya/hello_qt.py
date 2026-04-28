from PySide6 import QtWidgets  # Qt6
import maya.cmds as cmds


class HelloQtWindow(QtWidgets.QDialog):

    # qtwidgets have keyword argument parent, which we will default to None for now
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Hello Qt")

        # create controls
        self.name_line_edit = QtWidgets.QLineEdit()
        self.cube_button = QtWidgets.QPushButton("Cube")
        self.sphere_button = QtWidgets.QPushButton("Sphere")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.cube_button)
        layout.addWidget(self.sphere_button)
        self.setLayout(layout)

        # create connections
        # made up of a signal (event) and a slot (method)
        self.cube_button.clicked.connect(self.create_cube)
        self.sphere_button.clicked.connect(self.create_sphere)

    def get_name(self):
        # wrapped in a tuple?
        return (self.name_line_edit.text())

    def create_cube(self):
        print("Create Cube")
        cmds.polyCube(name=self.get_name())

    def create_sphere(self):
        print("Create Sphere")
        cmds.polySphere(name=self.get_name())


if __name__ == "__main__":
    window = HelloQtWindow()
    window.show()