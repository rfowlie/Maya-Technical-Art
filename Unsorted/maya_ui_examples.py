import maya.cmds as cmds


def ui_pop_up_example():
    window_name = "UI - Pop Up"
    # If the window already exists, delete it
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # Create the window
    window = cmds.window(
        window_name,
        title=window_name,
        widthHeight=(300, 100)
    )

    # Layout (UI elements must live inside layouts)
    cmds.columnLayout(adjustableColumn=True)

    # Add UI elements
    cmds.text(label="Hello Maya!")
    # cmds.button(label="Create Cube", command=lambda x: cmds.polyCube())

    # Show the window
    cmds.showWindow(window)


def ui_docked_example():

    workspace_name = "UI - Docked"

    if cmds.workspaceControl(workspace_name, exists=True):
        cmds.deleteUI(workspace_name)

    workspace = cmds.workspaceControl(
        workspace_name,
        label="My Docked Tool",
        # dockToMainWindow=("right", 1)
        dockToPanel=("right", 1)
    )

    layout = cmds.columnLayout(adjustableColumn=True, parent=workspace)

    cmds.text(label="Hello Maya!", parent=layout)
    cmds.button(label="Create Cube", parent=layout, command=lambda x: cmds.polyCube())