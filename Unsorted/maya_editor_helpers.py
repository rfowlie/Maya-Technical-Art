from PySide6 import QtWidgets


def print_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.objectName()} ({type(widget).__name__})")
    for child in widget.children():
        if isinstance(child, QtWidgets.QWidget):
            print_widget_tree(child, indent + 2)


def print_all_widget_tree():
    for widget in QtWidgets.QApplication.allWidgets():
        if not widget.parentWidget():
            print_widget_tree(widget)

