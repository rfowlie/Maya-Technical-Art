import maya.cmds as cmds


def transforms_from_shapes_node(shapes):
    print(shapes)
    transforms = []
    for obj in shapes:
        # case-sensitive for type search
        if cmds.objectType(obj, isAType="shape"):
            parents = cmds.listRelatives(obj, parent=True)
            if parents:
                transforms.append(parents[0])
    print(transforms)
    return transforms


def get_camera_transforms():
    camera_shapes = cmds.ls(cameras=True)
    camera_transforms = transforms_from_shapes_node(camera_shapes)

    return camera_transforms


if __name__ == '__main__':
    cameras = get_camera_transforms()

    # create a UI window
    cmds.window(title="Cameras")
    # give it a pane layout
    cmds.paneLayout()
    # give a text scroll list
    cmds.textScrollList(append=cameras)

    # window is hidden by default
    cmds.showWindow()