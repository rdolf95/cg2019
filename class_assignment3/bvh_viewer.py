import glfw
from OpenGL.GL import *
import numpy as np

hierarchy = []
motion = []
frame_num = 0
frame_time = 0
joint_num = 1
joint_name = []
channel_num = 0
frame_index = 0
file_check = False
animate_check = False
box_check = False
size_rescaling = True
max_len = np.array([0., 0., 0.])
local_max = np.array([0., 0., 0.])
base_time = 1


def draw_line(offset):
    glBegin(GL_LINES)
    glVertex3f(0., 0., 0.)
    glVertex3fv(offset)
    glEnd()


def drawUnitCube(offset, normal):
    glBegin(GL_QUADS)
    glNormal3f(0, normal[1], 0)
    glVertex3f(offset[0], offset[1], - offset[2])
    glVertex3f(- offset[0], offset[1], - offset[2])
    glVertex3f(- offset[0], offset[1], offset[2])
    glVertex3f(offset[0], offset[1], offset[2])

    glNormal3f(0, -normal[1], 0)
    glVertex3f(offset[0], - offset[1], offset[2])
    glVertex3f(- offset[0], - offset[1], offset[2])
    glVertex3f(- offset[0], - offset[1], - offset[2])
    glVertex3f(offset[0], - offset[1], - offset[2])

    glNormal3f(0, 0, normal[2])
    glVertex3f(offset[0], offset[1], offset[2])
    glVertex3f(- offset[0], offset[1], offset[2])
    glVertex3f(- offset[0], - offset[1], offset[2])
    glVertex3f(offset[0], - offset[1], offset[2])

    glNormal3f(0, 0, -normal[2])
    glVertex3f(offset[0], - offset[1], - offset[2])
    glVertex3f(- offset[0], - offset[1], - offset[2])
    glVertex3f(- offset[0], offset[1], - offset[2])
    glVertex3f(offset[0], offset[1], - offset[2])

    glNormal3f(-normal[0], 0, 0)
    glVertex3f(- offset[0], offset[1], offset[2])
    glVertex3f(- offset[0], offset[1], - offset[2])
    glVertex3f(- offset[0], - offset[1], - offset[2])
    glVertex3f(- offset[0], - offset[1], offset[2])

    glNormal3f(normal[0], 0, 0)
    glVertex3f(offset[0], offset[1], - offset[2])
    glVertex3f(offset[0], offset[1], offset[2])
    glVertex3f(offset[0], - offset[1], offset[2])
    glVertex3f(offset[0], - offset[1], - offset[2])
    glEnd()


def get_offset(offset):
    temp = [0., 0., 0.]
    if offset[0] > 0:
        temp[0] = offset[0] + 0.02
    elif offset[0] < 0:
        temp[0] = offset[0] - 0.02
    else:
        temp[0] = 0.02
    if offset[1] > 0:
        temp[1] = offset[1] + 0.02
    elif offset[1] < 0:
        temp[1] = offset[1] - 0.02
    else:
        temp[1] = 0.02
    if offset[2] > 0:
        temp[2] = offset[2] + 0.02
    elif offset[2] < 0:
        temp[2] = offset[2] - 0.02
    else:
        temp[2] = 0.02

    normal = [temp[0]/abs(temp[0]), temp[1]/abs(temp[1]), temp[2]/abs(temp[2])]

    return temp, normal


def set_hierarchy(f, head):
    global joint_num, joint_name, local_max, max_len

    local_max = np.array([0., 0., 0.])
    joint = []
    joint.append(head)
    c_head = head

    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()

        tag = line.split(' ', 1)
        if tag[0] == 'ROOT':
            c_head = 'R'
        elif tag[0] == 'JOINT':
            c_head = 'J'
            joint_num += 1
            joint_name.append(tag[1])
        elif tag[0] == 'End':
            c_head = 'E'
        elif tag[0] == 'OFFSET':
            offset = tag[1].split(' ')
            offset_arr = np.array([np.float32(offset[0]), np.float32(offset[1]), np.float32(offset[2])])
            local_max += offset_arr
            joint.append(offset_arr)
        elif tag[0] == 'CHANNELS':
            num = tag[1].split(' ', 1)
            channels = num[1].split(' ')
            joint.append(channels)
        elif tag[0] == '{':
            child = set_hierarchy(f, c_head)
            joint.append(child)
        elif tag[0] == '}':
            max_len += abs(local_max)
            return joint


def set_motion(f):
    motions = []
    while True:
        temp = []
        line = f.readline()
        if not line:
            break
        line = line.rstrip()
        frame_motion = line.split(' ')
        for i in range(len(frame_motion)):
            temp.append(np.float32(frame_motion[i]))
        motions.append(temp)

    return motions


def drop_callback(window, paths):
    global hierarchy, motion, frame_num, frame_time, joint_num, joint_name, file_check, max_len, base_time

    names = paths[0].split('/')
    f_name = names[len(names) - 1]
    f = open(paths[0], "r")
    file_check = True
    hierarchy = []
    motion = []
    frame_num = 0
    frame_time = 0
    joint_name = []
    joint_num = 1
    max_len = np.array([0., 0., 0.])

    while True:
        line = f.readline()
        if not line:
            break
        line = line.rstrip()

        tag = line.split(' ', 1)
        if tag[0] == 'HIERARCHY':
            line = f.readline()    # line for ROOT
            line = line.rstrip()
            root = line.split(' ', 1)
            joint_name.append(root[1])
            f.readline()            # line for first {
            hierarchy = set_hierarchy(f, 'R')
        elif tag[0] == 'MOTION':
            line = f.readline()
            line = line.rstrip()
            line = line.replace('\t', ' ')
            tag = line.split(' ', 1)
            frame_num = int(tag[1])

            line = f.readline()
            line = line.rstrip()
            line = line.replace('\t', ' ')
            tag = line.split(' ', 2)
            frame_time = np.float32(tag[2])
            motion = set_motion(f)

    print('1. File name: ', f_name)
    print('2. Number of frames: ', frame_num)
    print('3. FPS: ', 1/frame_time)
    print('4. Number of joints: ', joint_num)
    print('5. List of all joint names: ', joint_name)
    base_time = glfw.get_time()


def key_callback(window, key, scancode, action, mods):
    global animate_check, box_check, base_time, size_rescaling
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_SPACE:
            if animate_check is True:
                animate_check = False
                base_time = 1
            else:
                animate_check = True
                base_time = glfw.get_time()
        elif key == glfw.KEY_A:
            if box_check is True:
                box_check = False
            else:
                box_check = True
        elif key == glfw.KEY_S:
            if size_rescaling is True:
                size_rescaling = False
            else:
                size_rescaling = True


def get_lighting_mode():
    global box_check
    return box_check


def draw_hierarchy(hierarchy_data):
    global hierarchy, channel_num, motion, frame_index, animate_check, \
        frame_num, box_check, max_len, frame_time, base_time
    if size_rescaling is True:
        model_len = max_len
    else:
        model_len = np.array([1., 1., 1.])
    tag = hierarchy_data[0]
    offset = hierarchy_data[1]
    offset = offset / model_len
    glPushMatrix()

    if box_check is True:
        temp = [offset[0] / 2, offset[1] / 2, offset[2] / 2]
        temp_offset, normal = get_offset(temp)
        glTranslate(offset[0] / 2, offset[1] / 2, offset[2] / 2)
        drawUnitCube(temp_offset, normal)
        glTranslate(offset[0]/2, offset[1]/2, offset[2]/2)
    else:
        draw_line(offset)
        glTranslate(offset[0], offset[1], offset[2])
    frame_index = int(((glfw.get_time() - base_time) / frame_time) % frame_num)

    if tag != 'E':
        child_num = len(hierarchy_data) - 3
        channel = hierarchy_data[2]
        if animate_check is True:
            for i in range(len(channel)):
                if channel[i].upper() == 'XPOSITION':
                    xpos = motion[frame_index][channel_num]
                    xpos = xpos/model_len[0]
                    glTranslate(xpos, 0, 0)
                    channel_num += 1
                elif channel[i].upper() == 'YPOSITION':
                    ypos = motion[frame_index][channel_num]
                    ypos = ypos/model_len[1]
                    channel_num += 1
                    glTranslate(0, ypos, 0)
                elif channel[i].upper() == 'ZPOSITION':
                    zpos = motion[frame_index][channel_num]
                    zpos = zpos/model_len[2]
                    channel_num += 1
                    glTranslate(0, 0, zpos)
                elif channel[i].upper() == 'XROTATION':
                    xrot = motion[frame_index][channel_num]
                    channel_num += 1
                    glRotate(xrot, 1, 0, 0)
                elif channel[i].upper() == 'YROTATION':
                    yrot = motion[frame_index][channel_num]
                    channel_num += 1
                    glRotate(yrot, 0, 1, 0)
                elif channel[i].upper() == 'ZROTATION':
                    zrot = motion[frame_index][channel_num]
                    channel_num += 1
                    glRotate(zrot, 0, 0, 1)
        for i in range(child_num):
            draw_hierarchy(hierarchy_data[i+3])

    glPopMatrix()


def render_hierarchy():
    global hierarchy, file_check, channel_num
    if file_check is True:
        channel_num = 0
        draw_hierarchy(hierarchy)


