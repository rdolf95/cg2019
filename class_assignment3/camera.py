import glfw
from OpenGL.GL import *
import numpy as np

gCamAng = 0.
origin_xpos = 0.
origin_ypos = 0.
origin_panningx = 0.
origin_panningy = 0.
origin_zooming = 0.
zooming = 0.
accumulator = np.identity(4)
elav_accumulator = np.identity(4)


# set camera postion when every time it changed
def set_camera(first_eye):
    global zooming, accumulator, elav_accumulator

    glTranslate(0, 0, first_eye+zooming)
    x = elav_accumulator @ accumulator
    glMultMatrixf(x.T)


# set key call back to change speed of the dog
def key_callback(window, key, scancode, action, mods):
    global speed
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            speed += 1
        elif key == glfw.KEY_3:
            speed -= 1


# after release button -> change to do nothing
def cursor_callback_e(window, xpos, ypos):
    pass


# When left mosue button is clicked and dragged, rotate camera
def cursor_callback(window, xpos, ypos):
    global origin_xpos, origin_ypos, gCamAng, elavation, accumulator, elav_accumulator

    gCamAng = -(np.radians(origin_xpos - xpos))/1.5
    elavation = -(np.radians(origin_ypos - ypos))/1.5
    origin_xpos = xpos
    origin_ypos = ypos
    rot_matrix = np.array([[np.cos(gCamAng),  0, np.sin(gCamAng), 0],
                           [0,                1,               0, 0],
                           [-np.sin(gCamAng), 0, np.cos(gCamAng), 0],
                           [0,                0,               0, 1]])

    elav_matrix = np.array([[1,               0,                0, 0],
                            [0, np.cos(elavation),  -np.sin(elavation), 0],
                            [0, np.sin(elavation),   np.cos(elavation), 0],
                            [0,               0,                0, 1]])

    accumulator = rot_matrix @ accumulator
    elav_accumulator = elav_matrix @ elav_accumulator


# When right mouse button is clicked and dragged, move camera and target point
def cursor_callback2(window, xpos, ypos):
    global panningx, panningy, origin_panningx, origin_panningy, accumulator, gCamAng, elav_accumulator

    panningx = (- origin_panningx + xpos) / 40
    panningy = (- origin_panningy + ypos) / 40

    pan_matrix = np.array([[1, 0, 0, panningx],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])

    pan_matrix_y = np.array([[1, 0, 0, 0],
                           [0, 1, 0, -panningy],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])


    origin_panningx = xpos
    origin_panningy = ypos

    accumulator = pan_matrix @ accumulator
    elav_accumulator = pan_matrix_y @ elav_accumulator


# When mouse scroll is rotated, move camera forward and backward
def scroll_callback(window, xoffset, yoffset):
    global zooming, origin_zooming
    zooming -= (origin_zooming - yoffset) / 5


# When mouse button is clicked or released, change cursor callback
def button_callback(window, button, action, mod):
    global origin_xpos, origin_ypos, origin_panningx, origin_panningy

    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            (origin_xpos, origin_ypos) = glfw.get_cursor_pos(window)
            glfw.set_cursor_pos_callback(window, cursor_callback)
        elif action == glfw.RELEASE:
            glfw.set_cursor_pos_callback(window, cursor_callback_e)

    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            (origin_panningx, origin_panningy) = glfw.get_cursor_pos(window)
            glfw.set_cursor_pos_callback(window, cursor_callback2)

        elif action == glfw.RELEASE:
            glfw.set_cursor_pos_callback(window, cursor_callback_e)
