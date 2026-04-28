from cProfile import label
from functools import partial

import maya.cmds as cmds
import mesh_scatter

def generate_meshes(mesh_type_option, mesh_count_field, *args):
    cmds.file(newFile=True, force=True)

    mesh_type = cmds.optionMenu(mesh_type_option, query=True, value=True)
    mesh_count = cmds.intField(mesh_count_field, query=True, value=True)

    mesh_scatter.mesh_scatter(mesh_type, mesh_count)

def create_ui():
    window = cmds.window("Mesh Scatter")
    layout = cmds.formLayout()

    mesh_type_option = cmds.optionMenu(label="Mesh Type", parent=layout)
    cmds.menuItem(label="cube")
    cmds.menuItem(label="cylinder")
    cmds.menuItem(label="sphere")
    cmds.menuItem(label="random")

    mesh_count_label = cmds.text(label="Mesh Count", parent=layout)
    mesh_count_field = cmds.intField(value=20, minValue=1, parent=layout)

    generate_btn = cmds.button(
        "Generate",
        parent=layout,
        command=partial(generate_meshes, mesh_type_option, mesh_count_field))