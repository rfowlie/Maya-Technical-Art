import random

import maya.cmds as cmds

# random int between 2 ints
random.randint(-10, 10)

# return random float between 0 and 1
random.random()

# random number between a and b by increment
random.randrange(50, 100, 2)

# return an element from a list at random
random.choice(["red", "green", "blue"])


def set_random_position(transform_node):
    tx = random.randint(-10, 10)
    ty = random.randint(-10, 10)
    tz = random.randint(-10, 10)
    cmds.setAttr(f"{transform_node}.translate", tx, ty, tz, type="double3")


def mesh_scatter(mesh_type, num_mesh):
    mesh_transforms = []

    is_random = mesh_type == "random"

    for i in range(num_mesh):
        if is_random:
            mesh_type = random.choice(["sphere", "cylinder", "cube"])

        if mesh_type == "sphere":
            transform_node = cmds.polySphere()[0]
        elif mesh_type == "cylinder":
            transform_node = cmds.polyCylinder()[0]
        elif mesh_type == "cube":
            transform_node = cmds.polyCube()[0]

        mesh_transforms.append(transform_node)
        set_random_position(transform_node)

    # group for clarity
    cmds.group(mesh_transforms, name="scattered_meshes")


if __name__ == "__main__":
    cmds.file(newFile=True, force=True)

    mesh_scatter(mesh_type="random", num_mesh=10)