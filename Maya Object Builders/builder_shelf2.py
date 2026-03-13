import maya.cmds as cmds

WINDOW_NAME = "BuilderToolShelfWorkspace"


class BuilderToolShelf:

    def __init__(self):
        self.queryUI = {}

    # ---------------------------------------------------
    # UI
    # ---------------------------------------------------

    def build_ui(self):

        if cmds.workspaceControl(WINDOW_NAME, exists=True):
            cmds.deleteUI(WINDOW_NAME)

        workspace = cmds.workspaceControl(
            WINDOW_NAME,
            label="Shelf Builder",
            dockToMainWindow=("right", 1),
            initialWidth=200
        )

        main = cmds.columnLayout(adjustableColumn=True, rowSpacing=8, parent=workspace)

        self.queryUI["bottom"] = cmds.floatSliderGrp(
            label="Shelf Bottom %",
            min=0,
            max=1,
            value=0.2
        )

        self.queryUI["top"] = cmds.floatSliderGrp(
            label="Shelf Top %",
            min=0,
            max=1,
            value=0.9
        )

        self.queryUI["shelves"] = cmds.intFieldGrp(
            label="Number of Shelves",
            value1=5
        )

        cmds.separator(height=10)

        self.queryUI["height"] = cmds.floatFieldGrp(
            label="Height",
            value1=15
        )

        self.queryUI["width"] = cmds.floatFieldGrp(
            label="Width",
            value1=8
        )

        self.queryUI["depth"] = cmds.floatFieldGrp(
            label="Depth",
            value1=3
        )

        self.queryUI["thickness"] = cmds.floatFieldGrp(
            label="Board Thickness",
            value1=0.4
        )

        cmds.separator(height=10)

        self.queryUI["bevel"] = cmds.floatSliderGrp(
            label="Bevel Amount",
            min=0,
            max=0.5,
            value=0.05
        )

        self.queryUI["bevel_segments"] = cmds.intFieldGrp(
            label="Bevel Segments",
            value1=2
        )

        cmds.separator(height=10

        cmds.button(
            label="Create Shelf",
            height=40,
            command=self.run_tool
        )

    # ---------------------------------------------------
    # UI Query
    # ---------------------------------------------------

    def get_values(self):

        bottom = cmds.floatSliderGrp(self.queryUI["bottom"], q=True, value=True)
        top = cmds.floatSliderGrp(self.queryUI["top"], q=True, value=True)
        shelves = cmds.intFieldGrp(self.queryUI["shelves"], q=True, value1=True)
        height = cmds.floatFieldGrp(self.queryUI["height"], q=True, value1=True)
        width = cmds.floatFieldGrp(self.queryUI["width"], q=True, value1=True)
        depth = cmds.floatFieldGrp(self.queryUI["depth"], q=True, value1=True)
        thickness = cmds.floatFieldGrp(self.queryUI["thickness"], q=True, value1=True)
        bevel = cmds.floatSliderGrp(self.queryUI["bevel"], q=True, value=True)
        bevel_segments = cmds.intFieldGrp(self.queryUI["bevel_segments"], q=True, value1=True)

        return bottom, top, shelves, height, width, depth, thickness, bevel, bevel_segments

    # ---------------------------------------------------
    # Geometry Helpers
    # ---------------------------------------------------

    def create_board(self, width, height, depth, position):

        board = cmds.polyCube(w=width, h=height, d=depth)[0]

        cmds.move(
            position[0],
            position[1],
            position[2],
            board,
            ws=True
        )

        return board

    def bevel_object(self, obj, amount, segments):

        if amount <= 0:
            return

        cmds.polyBevel3(
            obj,
            fraction=amount,
            segments=segments,
            mitering=0
        )

    # ---------------------------------------------------
    # Tool Logic
    # ---------------------------------------------------

    def run_tool(self, *args):

        cmds.undoInfo(openChunk=True)

        try:

            (
                bottom,
                top,
                number,
                height,
                width,
                depth,
                thickness,
                bevel,
                bevel_segments
            ) = self.get_values()

            height_bottom = height * bottom
            height_top = (height - height_bottom) * top + height_bottom
            spacing = (height_top - height_bottom) / max(1, number - 1)

            boards = []

            # side panels
            for side in (-1, 1):
                board = self.create_board(
                    thickness,
                    height,
                    depth,
                    (side * width * 0.5, height * 0.5, 0)
                )

                self.bevel_object(board, bevel, bevel_segments)

                boards.append(board)

            # shelves
            for i in range(number):
                y = height_bottom + spacing * i

                board = self.create_board(
                    width,
                    thickness,
                    depth,
                    (0, y, 0)
                )

                self.bevel_object(board, bevel, bevel_segments)

                boards.append(board)

            # create group for all objects
            cmds.group(boards, name="shelf_geo")

        finally:

            cmds.undoInfo(closeChunk=True)


# ---------------------------------------------------
# Launch Tool
# ---------------------------------------------------

tool = BuilderToolShelf()
tool.build_ui()