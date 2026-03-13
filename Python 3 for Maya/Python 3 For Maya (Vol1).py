# Maya Commands

import maya.cmds as cmds

cmds.help("polySphere")

# create mode
cmds.polySphere(name="World", radius=20)
# create commands often return a list of nodes, generally you take the first
world2 = cmds.polySphere(name="World2", radius=20)[0]

# query mode
cmds.polySphere(query=True, radius=True)
# this is valid but only one property gets returned = undefined behaviour
cmds.polySphere(query=True, radius=True, heightBaseline=True)

# edit mode
# fires on current selection
cmds.polySphere(edit=True, radius=2)
# fires on object with name
cmds.polySphere("World", edit=True, radius=5)
# fires on object contained in variable
cmds.polySphere(world2, edit=True, radius=5)
# unlike query, you can edit any number of variables in one call
cmds.polySphere(world2, edit=True, radius=10, subdivisionsAxis=50, subdivisionsHeight=50)

# two most common commands in maya
cmds.help("ls")
cmds.help("select")

# displays all objects in scene
cmds.ls()
# list camera nodes
cmds.ls(cameras=True)
# list shape nodes
cmds.ls(shapes=True)
# list geometry nodes
cmds.ls(geometry=True)
# list selection
cmds.ls(selection=True)
# list types of selection, returns [name, type, name, type...]
cmds.ls(selection=True, showType=True)
# list has flags for the most common types, but when dealing with uncommon use the type flag
cmds.ls(type="transform")
# list only the top level nodes (top level in the outliner?)
cmds.ls(assemblies=True)
# list objects in scene using wildcard syntax * (case sensitive)
cmds.ls("W*")
cmds.ls("*1")

# clear selection
cmds.select(clear=True)
# select objects by name
cmds.select("World2")
# add to selection
cmds.select("World", add=True)
# replace current selection with new objects
cmds.select("World2", replace=True)
# pass in multiple objects using a list
cmds.select(["World", "World2"], replace=True)
# toggle the selection of a specific object
cmds.select("World", toggle=True)

# MEL for new scene (file -f -new;) as python
cmds.file(force=True, newFile=True)

# get attribute allows you to query any attribute from any object in the scene
cmds.getAttr("World2.visibility")
cmds.getAttr("World2.v")
# check if attribute is locked (unchangable)
cmds.getAttr("World2.tx", lock=True)
# check if attribute is keyable (adjustable through editor window)
cmds.getAttr("World2.tx", keyable=True)
# get attribute of current selection, ensure you include the dot
cmds.getAttr(".ry")

# set attribute allows you to adjust attributes on objects
cmds.setAttr("World2.sy", 5)
# set all values in attribute set, need to tell maya what the type is
cmds.setAttr("World2.rotate", 10, 20, 30, type="double3")
# set lock and keyable states for attributes
cmds.setAttr("World2.tx", lock=True)


# building example
def create_car(name, length=2, width=1):
    body = create_body(length, width)
    tires = create_tires(length, width)
    car = assemble_car(name, body, tires)
    # do not want object selected after creation...
    cmds.select(clear=True)


def create_body(length, width):
    body = cmds.polyPlane(name="Body", w=length, h=width)[0]
    return body


def create_tires(body_length, body_width):
    tire_radius = 0.25 * body_length
    tire_width = 0.25 * body_width
    x_pos = 0.5 * body_length
    z_pos = 0.5 * body_width + 0.5 * tire_width

    fl = create_tire("front_left_tire", tire_width, tire_radius, x_pos, 0, -z_pos)
    fr = create_tire("front_right_tire", tire_width, tire_radius, x_pos, 0, z_pos)
    bl = create_tire("back_left_tire", tire_width, tire_radius, -x_pos, 0, -z_pos)
    br = create_tire("back_right_tire", tire_width, tire_radius, -x_pos, 0, z_pos)

    return [fl, fr, bl, br]


# using keyword args similar to mayas for clarity
def create_tire(name, width, radius, tx, ty, tz):
    tire = cmds.polyCylinder(name=name, h=width, r=radius, ax=(0, 0, 1), sc=True)[0]
    cmds.setAttr(f"{tire}.translate", tx, ty, tz)
    return tire


# important to organize your objects
def assemble_car(name, body, tires):
    group_body = cmds.group(body, name="body_grp")
    group_tires = cmds.group(tires, name="tires_grp")
    group_car = cmds.group(group_body, group_tires, name=name)
    return group_car


if __name__ == "__main__":
    create_car("Car", length=10, width=5)
