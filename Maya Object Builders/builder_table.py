import maya.cmds as cmds

WINDOW_NAME = "BuilderToolTableWorkspace"


class BuilderToolTable:

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
            label="Table Builder",
            dockToMainWindow=("right", 1),
            initialWidth=200
        )

        main = cmds.columnLayout(adjustableColumn=True, rowSpacing=8, parent=workspace)

        self.queryUI["Table Length"] = cmds.floatFieldGrp(
            label="Table Length",
            value1=20
        )

        self.queryUI["Table Width"] = cmds.floatFieldGrp(
            label="Table Width",
            value1=10
        )

        self.queryUI["Table Height"] = cmds.floatFieldGrp(
            label= "Table Height",
            value1=2
        )

        cmds.separator(height=10)

        self.queryUI["Leg Height"] = cmds.floatFieldGrp(
            label="Leg Height",
            value1=10
        )

        self.queryUI["Leg Radius"] = cmds.floatFieldGrp(
            label="Leg Radius",
            value1=1
        )

        self.queryUI["Leg Subdivisions"] = cmds.floatFieldGrp(
            label="Leg Subdivisions",
            value1=12
        )

        cmds.separator(height=10)

        self.queryUI["Leg Length Offset"] = cmds.floatSliderGrp(
            label="Leg Length Offset",
            min=0,
            max=1,
            value=0.9
        )

        self.queryUI["Leg Width Offset"] = cmds.floatSliderGrp(
            label="Leg Width Offset",
            min=0,
            max=1,
            value=0.9
        )

        cmds.separator(height=10)

        cmds.button(
            label="Create",
            height=40,
            command=self.run_tool
        )

    # ---------------------------------------------------
    # UI Query
    # ---------------------------------------------------

    def get_values(self):
        table_length = cmds.floatFieldGrp(self.queryUI["Table Length"], q=True, value1=True)
        table_width = cmds.floatFieldGrp(self.queryUI["Table Width"], q=True, value1=True)
        table_height = cmds.floatFieldGrp(self.queryUI["Table Height"], q=True, value1=True)
        leg_height = cmds.floatFieldGrp(self.queryUI["Leg Height"], q=True, value1=True)
        leg_radius = cmds.floatFieldGrp(self.queryUI["Leg Radius"], q=True, value1=True)
        leg_subdivisions = cmds.floatFieldGrp(self.queryUI["Leg Subdivisions"], q=True, value1=True)
        leg_length_offset = cmds.floatSliderGrp(self.queryUI["Leg Length Offset"], query=True, value=True)
        leg_width_offset = cmds.floatSliderGrp(self.queryUI["Leg Width Offset"], query=True, value=True)

        return table_length, table_width, table_height, leg_height, leg_radius, leg_subdivisions, leg_length_offset, leg_width_offset

    # ---------------------------------------------------
    # Geometry Helpers
    # ---------------------------------------------------

    def create_table(self, length, width, height):
        print(f"Create Table Widgth: {width}")
        table = cmds.polyCube(w=width, h=height, d=length)[0]
        return table

    def create_legs(self, height, radius, sub_division_axis, table_length, table_width, leg_length_offset, leg_width_offset):

        width = (table_width / 2) * leg_width_offset - radius
        length = (table_length /2) * leg_length_offset - radius
        move_height = -(height / 2)

        leg1 = cmds.polyCylinder(h=height, radius=radius, sa=sub_division_axis)[0]
        cmds.xform(leg1, translation=[width, move_height, length])
        leg2 = cmds.polyCylinder(h=height, radius=radius, sa=sub_division_axis)[0]
        cmds.xform(leg2, translation=[width, move_height, -length])
        leg3 = cmds.polyCylinder(h=height, radius=radius, sa=sub_division_axis)[0]
        cmds.xform(leg3, translation=[-width, move_height, length])
        leg4 = cmds.polyCylinder(h=height, radius=radius, sa=sub_division_axis)[0]
        cmds.xform(leg4, translation=[-width, move_height, -length])

        return [leg1, leg2, leg3, leg4]


    def run_tool(self, *args):

        cmds.undoInfo(openChunk=True)
        try:
            (
                table_length,
                table_width,
                table_height,
                leg_height,
                leg_radius,
                leg_subdivisions,
                leg_length_offset,
                leg_width_offset
            ) = self.get_values()

            objs = []
            objs.append(self.create_table(
                table_length, table_width, table_height))
            objs.extend(self.create_legs(
                leg_height, leg_radius, leg_subdivisions, table_length, table_width, leg_length_offset, leg_width_offset))

            # create group for all objects
            cmds.group(objs, name="table_geo")

        finally:
            cmds.undoInfo(closeChunk=True)


# ---------------------------------------------------
# Launch Tool
# ---------------------------------------------------

tool = BuilderToolTable()
tool.build_ui()