import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as openMaya


def get_keyframe_times(interval=1, skip_existing=False):
    selected_range = get_selected_range()
    if selected_range:
        start, end = selected_range
    else:
        start, end = get_playback_range()

    keyframes = list(range(start, end + 1, interval))
    if skip_existing:
        keyframes = [x for x in keyframes if not keyframe_exists(x)]

    return keyframes


def get_playback_range():
    start = int(cmds.playbackOptions(query=True, minTime=True))
    end = int(cmds.playbackOptions(query=True, maxTime=True))
    return start, end


def get_selected_range():
    # in mel variables are prefixed with $
    # $gPlayBackSlider is a global control
    main_time_control = mel.eval("$temp = $gPlayBackSlider")
    if cmds.timeControl(main_time_control, query=True, rangeVisible=True):
        selected_range = cmds.timeControl(main_time_control, query=True, rangeArray=True)
        # this will return +1 the actual selected range so we must subtract
        selected_range[1] -= 1
        return [int(x) for x in selected_range]

    return None


def keyframe_exists(keyframe_time):
    keyframe_count = cmds.keyframe(query=True, keyframeCount=True, time=(keyframe_time,))
    return keyframe_count > 0


def insert_keyframes(keyframe_times):
    # validate state
    if not cmds.ls(selection=True):
        openMaya.MGlobal.displayWarning("No Objects Selected")
        return

    # can accept a single value or list
    cmds.setKeyframe(time=keyframe_times)


if __name__ == "__main__":
    # insert_keyframes(get_keyframe_times(interval=1, skip_existing=True))
    print(get_keyframe_times(interval=1, skip_existing=True))