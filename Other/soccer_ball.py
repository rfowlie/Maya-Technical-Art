import maya.cmds as cmds


def update_scale(scale_slider):
    value = cmds.floatSliderGrp(scale_slider, query=True, value=True)
    cmds.setAttr(transform + '.scaleX', value)
    cmds.setAttr(transform + '.scaleY', value)
    cmds.setAttr(transform + '.scaleZ', value)
    cmds.setAttr(scultptor[1] + '.scaleX', value)
    cmds.setAttr(scultptor[1] + '.scaleY', value)
    cmds.setAttr(scultptor[1] + '.scaleZ', value)


def get_window_name():
    return 'soccer_ball_creator'


def create_window():
    pass


if cmds.window(get_window_name(), exists=True):
    cmds.deleteUI(get_window_name())

window = cmds.window(get_window_name(), resizeToFitChildren=True, sizeable=False)
main_layout = cmds.columnLayout()
scale_slider = cmds.floatSliderGrp(label='Scale', field=True, minValue=1.0, maxValue=20.0, value=8.0)
cmds.floatSliderGrp(scale_slider, edit=True, dragCommand=lambda x: update_scale(scale_slider))

cmds.showWindow(window)
scale = cmds.floatSliderGrp(scale_slider, query=True, value=True)
temp = cmds.polyPrimitive(radius=scale, sideLength=0.4, axis=[0, 1, 0], polyType=0, createUVs=4, constructionHistory=True)
print(temp)
transform = temp[0]
print(transform)
history = temp[1]
print(history)

# cmds.select(transform, replace=True)
# vertices = cmds.ConvertSelectionToVertices()
vertices = cmds.polyEvaluate(transform, vertex=True)
polySplitVert = cmds.polySplitVertex('{}.vtx[0:{}]'.format(transform, vertices))
cmds.select(transform, replace=True)
polySmooth = cmds.polySmooth()
print(polySmooth)
cmds.setAttr(polySmooth[0] + '.divisions', 1.6)
scultptor = cmds.sculpt(transform, mode='stretch', insideMode='even', maxDisplacement=0.1, dropoffType='linear', dropoffDistance=1, groupWithLocator=False, objectCentered=True)
# cmds.setAttr(scultptor[1] + '.scaleX', scale)
# cmds.setAttr(scultptor[1] + '.scaleY', scale)
# cmds.setAttr(scultptor[1] + '.scaleZ', scale)
cmds.scale(scale, scale, scale, scultptor[1])
print(scultptor)

# delete history when done scaling...
cmds.selectMode( object=True )
cmds.select(transform, replace=True)
cmds.DeleteHistory()
cmds.selectMode( object=True )
cmds.select(transform, replace=True)
extrude = cmds.polyExtrudeFacet(transform, constructionHistory=True, keepFacesTogether=True, pvx=0, pvz=0, divisions=1, twist=0, taper=1, offset=0, thickness=0, smoothingAngle=30)[0]
scale = cmds.floatSliderGrp(scale_slider, query=True, value=True)
cmds.setAttr(extrude + '.localTranslateZ', -scale/10.0)
cmds.setAttr(extrude + '.offset', -scale/20.0)

# cmds.selectMode( object=True )
# cmds.select(transform, replace=True)
cmds.polyNormal(transform, normalMode=0, userNormalMode=0)

# sets -e -forceElement aiStandardSurface1SG;

if __name__ == '__main__':
    print('Soccer Ball Test')