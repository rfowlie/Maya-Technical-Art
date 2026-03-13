import maya.cmds as cmds


def hello_world(*args):
    print('hello, world!')


def create_ui():

    # windos is the top container
    window = cmds.window("Minimal UI", width=250)
    # windows require a layout to actually visualize
    layout = cmds.columnLayout(adjustableColumn=True, parent=window)

    cmds.checkBox(label="Fun Checkbox", parent=layout)
    # buttons have command flag that can take a func
    button = cmds.button(label="Sick Button", parent=layout)
    # elements can be edited after creation, use edit flag
    # NOTE: for buttons, some default args get passed on command call
    # ensure that the func you wish to call uses *args
    cmds.button(button, edit=True, command=hello_world)

    cmds.showWindow(window)


if __name__ == "__main__":
    create_ui()