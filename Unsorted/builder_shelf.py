import maya.cmds as cmds


WINDOW_NAME = "ShelfToolUI"


class ShelfTool:

    def __init__(self):
        self.ui = {}

    # ----------------------------
    # UI
    # ----------------------------

    def build_ui(self):

        if cmds.window(WINDOW_NAME, exists=True):
            cmds.deleteUI(WINDOW_NAME)

        cmds.window(
            WINDOW_NAME,
            title="Shelf Tool",
            widthHeight=(300, 250),
            width=300,
            height=250,
            sizeable=False
        )

        main = cmds.columnLayout(adjustableColumn=True, rowSpacing=8)

        self.ui["bottom"] = cmds.floatSliderGrp(
            label="Shelf Bottom Percentage",
            min=0,
            max=1,
            value=0.5
        )

        self.ui["top"] = cmds.floatSliderGrp(
            label="Shelf Top Percentage",
            min=0,
            max=1,
            value=0.8
        )

        self.ui["shelves"] = cmds.intFieldGrp(
            label="Number Of Shelves",
            value1=8
        )

        self.ui["height"] = cmds.floatFieldGrp(
            label="Height",
            value1=15
        )

        self.ui["width"] = cmds.floatFieldGrp(
            label="Width",
            value1=5
        )

        self.ui["depth"] = cmds.floatFieldGrp(
            label="Depth",
            value1=2
        )

        cmds.separator(height=10)

        cmds.button(
            label="Create Shelf",
            height=40,
            command=self.run_tool
        )

        cmds.showWindow()

    # ----------------------------
    # Data Query
    # ----------------------------

    def get_values(self):

        bottom = cmds.floatSliderGrp(self.ui["bottom"], q=True, value=True)
        top = cmds.floatSliderGrp(self.ui["top"], q=True, value=True)
        number = cmds.intFieldGrp(self.ui["shelves"], q=True, value1=True)
        height = cmds.floatFieldGrp(self.ui["height"], q=True, value1=True)
        width = cmds.floatFieldGrp(self.ui["width"], q=True, value1=True)
        depth = cmds.floatFieldGrp(self.ui["depth"], q=True, value1=True)

        return bottom, top, number, height, width, depth

    # ----------------------------
    # Shelf Creation
    # ----------------------------

    def create_board(self, width, height, depth, position):

        board = cmds.polyCube(w=width, h=height, d=depth)[0]
        cmds.move(position[0], position[1], position[2], board, ws=True)

        return board

    # ----------------------------
    # Tool Logic
    # ----------------------------

    def run_tool(self, *args):

        cmds.undoInfo(openChunk=True)

        try:

            bottom, top, number, height, width, depth = self.get_values()

            height_bottom = height * bottom
            height_top = (height - height_bottom) * top + height_bottom
            shelf_spacing = (height_top - height_bottom) / max(1, number - 1)

            boards = []
            # shelves
            for i in range(number):

                y = height_bottom + shelf_spacing * i

                board = self.create_board(
                    width,
                    0.5,
                    depth,
                    (0, y, 0)
                )

                boards.append(board)

            # side panels
            for side in (-1, 1):

                board = self.create_board(
                    0.5,
                    height,
                    depth,
                    (side * width * 0.5, height * 0.5, 0)
                )

                boards.append(board)

            cmds.group(boards, name="shelf_geo")

        finally:
            cmds.undoInfo(closeChunk=True)


# ----------------------------
# Launch
# ----------------------------

tool = ShelfTool()
tool.build_ui()