import maya.cmds as cmds

menu_name = "MyCustomMenu"

# Delete the menu if it already exists
if cmds.menu(menu_name, exists=True):
    cmds.deleteUI(menu_name)

# Create the menu in the main Maya window
main_maya_window = cmds.window("MayaWindow", exists=True)
if main_maya_window:
    cmds.menu(menu_name, label="My Custom Menu", parent="MayaWindow")

# Define a custom function
def my_custom_function():
    sphere = cmds.polySphere()[0]
    cmds.setAttr(f"{sphere}.translateX", 5)
    print("Sphere created and moved to X=5")

# Add menu items
cmds.menuItem(label="Create Sphere", parent=menu_name, command=lambda x: cmds.polySphere())
cmds.menuItem(label="Create Cube", parent=menu_name, command=lambda x: cmds.polyCube())
cmds.menuItem(divider=True)
cmds.menuItem(label="Run Custom Function", parent=menu_name, command=my_custom_function)


if __name__ == '__main__':
    print('Create Menu')