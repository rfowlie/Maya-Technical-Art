import maya.cmds as cmds
import maya.mel as mel

def test():

    floor_size = 24

    base = cmds.polyCube(name='Base')[0]
    cmds.xform(base, scale=[floor_size, 1, floor_size], worldSpace=True)
    # cmds.polyBevel(base, offset=0.2, segments=2)

    wall = cmds.polyCube(name='Wall')[0]
    cmds.xform(wall, scale=[1, floor_size // 2, 1], worldSpace=True)
    cmds.xform(wall, translation=[-(floor_size // 2), (floor_size // 4) + 1, -(floor_size // 2)], worldSpace=True)
    cmds.polyExtrudeFacet(f"{wall}.f[0]", localTranslateZ=floor_size)
    cmds.polyExtrudeFacet(f"{wall}.f[4]", localTranslateZ=floor_size)
    cmds.select(wall, replace=True)

    # todo: make this a parameter that can be adjusted between (0-1)
    wall_split1 = 0.8
    wall_split2 = 1 / (wall_split1 / (1 - wall_split1))
    cmds.polySplit(ip=[(4, wall_split1), (8, 1.0-wall_split1), (9, 1.0-wall_split1), (24, 1.0-wall_split1),
                       (27, wall_split1), (5, wall_split1), (16, wall_split1), (19, wall_split1), (4, wall_split1)])
    cmds.polySplit(ip=[(4, wall_split2), (29, 1-wall_split2), (30, 1-wall_split2), (31, 1-wall_split2),
                       (27, wall_split2), (5, wall_split2), (16, wall_split2), (19, wall_split2), (4, wall_split2)])

    wall_face_indices = [19, 18, 17, 16, 15, 14, 21, 20, 13, 4, 11, 2, 5, 9, 0, 7]
    faces = [f"Wall.f[{i}]" for i in wall_face_indices]
    cmds.polyExtrudeFacet(faces, thickness=1.5)


    wall_edge_indices = ['22', '23', '24', '25', '26', '27', '28', '29', '30', '32', '33', '34', '35', '36', '37', '38',
                         '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '54', '58', '60',
                         '61', '62', '63', '64', '65', '66', '67', '69', '72', '73', '74', '75', '76', '77', '78', '79',
                         '80', '81', '82', '83', '86', '90', '93', '96', '97', '98', '99', '100', '101', '102', '103',
                         '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116',
                         '117', '118', '119', '120', '121', '122', '123']

    edges = [f"Wall.e[{i}" for i in wall_edge_indices]
    cmds.select(edges)
    mel.eval("""
        polyBevel3 -fraction 0.5 -offsetAsFraction 1 -autoFit 1 -depth 1 -mitering 0 -miterAlong 0 -chamfer 1 -segments 1 -worldSpace 1 -smoothingAngle 30 -filterAngle 30 -filterEdgesByAngle 0 -filterHardEdges 0 -subdivideNgons 1 -mergeVertices 1 -mergeVertexTolerance 0.0001 -miteringAngle 180 -angleTolerance 180 -ch 1;
        """)

    floor_boards = []
    for x in range(1, floor_size // 2 + 1):
        board = cmds.polyCube(name=f"board_{x}")
        floor_boards.append(board)

        cmds.xform(board, scale=[floor_size, 0.5, 2], worldSpace=True)
        cmds.xform(board, translation=[0, 0.75, -(floor_size // 2 + 1) + (x * 2)], worldSpace=True)
        # this is acting strange, there are default for poly bevel button that are not captured in python
        # cmds.polyBevel(board, offset=0.2, segments=2)
        cmds.select(clear=True)
        cmds.select(board)
        mel.eval("performBevelOrChamfer")


def floors_and_walls():
    import maya.cmds as cmds

    floor_size = 24

    # floor base
    floor = cmds.polyCube(name='Base')[0]
    floor_height = 1
    cmds.xform(floor, scale=[floor_size, floor_height, floor_size], worldSpace=True)
    # cmds.polyBevel(base, offset=0.2, segments=2)

    # floor boards
    floor_board_height = 0.5
    floor_boards = []
    for x in range(1, floor_size // 2 + 1):
        board = cmds.polyCube(name=f"board_{x}")
        floor_boards.append(board)

        cmds.xform(board, scale=[floor_size, floor_board_height, 2], worldSpace=True)
        cmds.xform(board, translation=[0, 0.75, -(floor_size // 2 + 1) + (x * 2)], worldSpace=True)
        # this is acting strange, there are default for poly bevel button that are not captured in python
        # cmds.polyBevel(board, offset=0.2, segments=2)
        cmds.select(clear=True)
        cmds.select(board)
        mel.eval("performBevelOrChamfer")

    wall = cmds.polyCube(name='Wall')[0]
    wall_height = floor_size - 4
    cmds.xform(wall, scale=[1, wall_height, 1], worldSpace=True)
    cmds.xform(wall, translation=[-(floor_size // 2), (wall_height / 2) + floor_height + floor_board_height, -(floor_size // 2)],
               worldSpace=True)
    cmds.polyExtrudeFacet(f"{wall}.f[0]", localTranslateZ=floor_size)
    cmds.polyExtrudeFacet(f"{wall}.f[4]", localTranslateZ=floor_size)
    cmds.select(wall, replace=True)
    cmds.polySplit(ip=[(4, 0.7), (8, 0.3), (9, 0.3), (24, 0.3), (27, 0.7), (5, 0.7), (16, 0.7), (19, 0.7), (4, 0.7)])
    cmds.polySplit(
        ip=[(4, 0.35), (29, 0.65), (30, 0.65), (31, 0.65), (27, 0.35), (5, 0.35), (16, 0.35), (19, 0.35), (4, 0.35)])

    face_indices = [19, 18, 17, 16, 15, 14, 21, 20, 13, 4, 11, 2, 5, 9, 0, 7]
    faces = [f"Wall.f[{i}]" for i in face_indices]
    cmds.polyExtrudeFacet(faces, thickness=1.5)

    wall_edge_indices = ['22', '23', '24', '25', '26', '27', '28', '29', '30', '32', '33', '34', '35', '36', '37', '38',
                         '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '54', '58', '60',
                         '61', '62', '63', '64', '65', '66', '67', '69', '72', '73', '74', '75', '76', '77', '78', '79',
                         '80', '81', '82', '83', '86', '90', '93', '96', '97', '98', '99', '100', '101', '102', '103',
                         '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116',
                         '117', '118', '119', '120', '121', '122', '123']

    edges = [f"Wall.e[{i}]" for i in wall_edge_indices]
    cmds.select(edges)
    mel.eval("""
        polyBevel3 -fraction 0.3 -offsetAsFraction 1 -autoFit 1 -depth 1 -mitering 0 -miterAlong 0 -chamfer 1 -segments 2 -worldSpace 1 -smoothingAngle 30 -filterAngle 30 -filterEdgesByAngle 0 -filterHardEdges 0 -subdivideNgons 1 -mergeVertices 1 -mergeVertexTolerance 0.0001 -miteringAngle 180 -angleTolerance 180 -ch 1;
        """)

    # TODO: create the window... tutorial seems a bit odd here and not correct modeling
    for i in [150, 152]:
        cmds.select(clear=True)
        cmds.select([f"Wall.f[{i}]"], add=True)
        cmds.polyExtrudeFacet()
        cmds.scale(0.5, 0.5, 0.5, localSpace=True)
        cmds.move(7, 0, 0, relative=True)


def shelf():
    shelf_height = 15
    shelf_width = 5
    shelf_depth = 2
    shelf_bottom_percent = 0.25
    shelf_top_percent = 0.9
    shelf_boards = 3
    shelf_spacing = ((shelf_height * shelf_top_percent) - (shelf_height * shelf_bottom_percent)) / (shelf_boards - 1)

    for i in range(shelf_boards):
        board = cmds.polyCube()[0]
        cmds.select(board, replace=True)
        cmds.scale(shelf_width, 0.5, shelf_depth)
        cmds.move(0, shelf_height * shelf_bottom_percent + (shelf_spacing * i), 0)
        mel.eval("performBevelOrChamfer")

    for i in [-1,1]:
        board = cmds.polyCube()[0]
        cmds.select(board, replace=True)
        cmds.scale(0.5, shelf_height, shelf_depth)
        cmds.move(shelf_width / 2 * i, shelf_height / 2, 0)
        mel.eval("performBevelOrChamfer")


import maya.cmds as cmds


def run_tool(*args):
    # query values from tool
    bottom = cmds.floatSliderGrp("shelf_bottom", q=True, value=True)
    top = cmds.floatSliderGrp("shelf_top", q=True, value=True)
    number = cmds.intField("shelves_field", q=True, value=True)
    height = cmds.floatField("heightField", q=True, value=True)
    width = cmds.floatField("widthField", q=True, value=True)
    depth = cmds.floatField("depthField", q=True, value=True)

    # to ensure no fuckery, top should be the value between bottom and height
    height_bottom = height * bottom
    height_top = (height - height_bottom) * top + height_bottom
    shelf_spacing = (height_top - height_bottom) / (max(1, number - 1))
    # print(f"{height_bottom}, {height_top}, {shelf_spacing}")

    for i in range(number):
        board = cmds.polyCube()[0]
        cmds.select(board, replace=True)
        cmds.scale(width, 0.5, depth)
        cmds.move(0, height_bottom + (shelf_spacing * i), 0)
        mel.eval("performBevelOrChamfer")

    for i in [-1, 1]:
        board = cmds.polyCube()[0]
        cmds.select(board, replace=True)
        cmds.scale(0.5, height, depth)
        cmds.move(width / 2 * i, height / 2, 0)
        mel.eval("performBevelOrChamfer")


def build_ui():

    window = "myToolUI"

    if cmds.window(window, exists=True):
        cmds.deleteUI(window)

    window = cmds.window(window, title="My Tool", widthHeight=(300, 250))
    layout_main = cmds.columnLayout(adjustableColumn=True, rowSpacing=6, height=400, width=250)

    # Bottom value 1 (0–1)
    cmds.floatSliderGrp("shelf_bottom", label="Shelf Bottom Percentage", min=0, max=1, value=0.5)

    # Bottom value 2 (0–1)
    cmds.floatSliderGrp("shelf_top", label="Shelf Top Percentage", min=0, max=1, value=0.8)

    # Number (minimum 1)
    layout_number = cmds.rowLayout(adjustableColumn=True, numberOfColumns=2, columnWidth2= [20, 6], parent=layout_main)
    cmds.text(label="Number Of Shelves", parent=layout_number)
    cmds.intField("shelves_field", minValue=1, value=8, parent=layout_number)

    # Height (>0)
    layout_height = cmds.rowLayout(adjustableColumn=True, numberOfColumns=2, columnWidth2=[20, 6], parent=layout_main)
    cmds.text(label="Height", parent=layout_height)
    cmds.floatField("heightField", minValue=1, value=15, parent=layout_height)

    # Width (>0)
    layout_width = cmds.rowLayout(adjustableColumn=True, numberOfColumns=2, columnWidth2=[20, 6], parent=layout_main)
    cmds.text(label="Width", parent=layout_width)
    cmds.floatField("widthField", minValue=1, value=5, parent=layout_width)

    # Depth (>0)
    layout_depth = cmds.rowLayout(adjustableColumn=True, numberOfColumns=2, columnWidth2=[20, 6], parent=layout_main)
    cmds.text(label="Depth", parent=layout_depth)
    cmds.floatField("depthField", minValue=1, value=2, parent=layout_depth)

    cmds.separator(height=10, parent=layout_main)

    cmds.button(label="Create", height=40, command=run_tool, parent=layout_main)

    cmds.showWindow(window)


build_ui()