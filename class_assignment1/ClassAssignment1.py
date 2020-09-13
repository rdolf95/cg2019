import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
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
time = 0.
speed = 1
dog_time = 0.
dog_pos = 0.


# draw a cube of side 1, centered at the origin.
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)

    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)

    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)

    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glEnd()


def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)

        glEnd()


def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i, j, -k - 1)
                glScalef(.5, .5, .5)
                drawUnitCube()
                glPopMatrix()


# draw coodinate axis and xy palne with rectangular grid
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-1., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., -1., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., -1.]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()

    glColor3ub(255, 255, 255)
    for i in range(-10, 10):
        glBegin(GL_LINES)
        glVertex3fv(np.array([i, 0., 11.]))
        glVertex3fv(np.array([i, 0., -11.]))
        glVertex3fv(np.array([11., 0., i]))
        glVertex3fv(np.array([-11., 0., i]))
        glEnd()


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


# draw the dog's four legs
def draw_leg(upper_ang, lower_ang, lower_length):
    glRotate(upper_ang, 0, 0, 1)
    # draw upper pipe
    glPushMatrix()
    glScale(.1, .1, .1)
    drawSphere()
    glPopMatrix()  # pop to upper pipe

    # upper leg
    glPushMatrix()
    glTranslate(0, -0.3, 0)

    # draw upper leg
    glPushMatrix()
    glScale(.1, .5, .1)
    drawUnitCube()
    glPopMatrix()  # pop to upper leg

    # lower pipe
    glPushMatrix()
    glTranslate(0, -0.3, 0)
    glRotate(lower_ang, 0, 0, 1)

    # draw lower pipe
    glPushMatrix()
    glScale(.1, .1, .1)
    drawSphere()
    glPopMatrix()  # pop to lower pipe

    # lower leg
    glPushMatrix()
    glTranslate(0, -0.3, 0)

    # draw lower leg
    glPushMatrix()
    glScale(.1, lower_length, .1)
    drawUnitCube()
    glPopMatrix()  # pop to lower leg

    glPopMatrix()  # pop to lower pipe

    glPopMatrix()  # pop to upper leg

    glPopMatrix()  # pop to upper pipe


# draw the dog's head including nose, ears
def draw_head():
    # head
    glPushMatrix()
    glTranslate(-1.5 + 0.15, -.15, 0)
    # draw head
    glPushMatrix()
    glScale(.7, .7, .7)
    drawUnitCube()
    glPopMatrix()  # pop to head

    # nose
    glPushMatrix()
    glTranslate(-.55, -.15, 0)
    glScale(.4, .4, .4)
    drawUnitCube()
    glPopMatrix()  # pop to head

    # left ear
    glPushMatrix()
    glTranslate(-.3, .55, .25)
    glScale(.1, .4, .2)
    drawUnitCube()
    glPopMatrix()  # pop to head

    # right ear
    glPushMatrix()
    glTranslate(-.3, .55, -.25)
    glScale(.1, .4, .2)
    drawUnitCube()
    glPopMatrix()  # pop to head

    glPopMatrix()  # pop to body


# draw the dog's tail and its pipe
def draw_tail(tail_ang):
    # tail pipe
    glPushMatrix()
    glTranslate(1., .3, 0)
    glRotate(tail_ang, 0, 0, 1)
    # draw tail pipe
    glPushMatrix()
    glScale(.1, .1, .1)
    drawSphere()
    glPopMatrix()   # pop to tail pipe
    # tail
    glPushMatrix()
    glTranslate(.3, 0, 0,)
    # draw tail
    glPushMatrix()
    glScale(.5, .1, .1)
    drawUnitCube()
    glPopMatrix()   # pop to tail

    glPopMatrix()   # pop to tail pipe

    glPopMatrix()   # pop to body


# function to get front upper pipe rotation angle
def get_front_upper_ang(time_offset):
    global time
    t = time

    if ((t+time_offset) * 10) % 120 < 60:
        front_upper_ang = -40 + (10 * (t+time_offset)) % 60
    else:
        front_upper_ang = 20 - (10 * (t+time_offset)) % 60

    return front_upper_ang


# function to get front lower pipe rotation angle
def get_front_lower_ang(time_offset):
    global time
    t = time

    if (t + time_offset) % 12 < 4:
        front_lower_ang = 40 - (10 * (t + time_offset)) % 60
    elif 4 < (t + time_offset) % 12 < 6:
        front_lower_ang = 0
    elif 6 < (t + time_offset) % 12 < 8:
        front_lower_ang = (30 * (t + time_offset)) % 60
    elif 8 < (t + time_offset) % 12 < 10:
        front_lower_ang = 60
    else:    # 10 < t%12 <12
        front_lower_ang = 60 - ((10 * (t + time_offset)) % 60 - 40)

    return front_lower_ang


# function to get rear upper pipe rotation angle
def get_rear_upper_ang(time_offset):
    global time
    t = time

    if (t+time_offset) % 12 < 6:
        rear_upper_ang = 14 + 4 * ((t+time_offset) % 6)
    else:   # 6 < t < 12
        rear_upper_ang = 38 - 4 * ((t+time_offset) % 6)

    return rear_upper_ang


# function to get rear lower pipe rotation angle
def get_rear_lower_ang(time_offset):
    global time
    t = time

    if (t+time_offset) % 12 < 4:
        rear_lower_ang = -39 + 6 * ((t+time_offset) % 6)
    elif 4 < (t+time_offset) % 12 < 6:
        rear_lower_ang = -15
    elif 6 < (t+time_offset) % 12 < 8:
        rear_lower_ang = -15 - 18 * ((t+time_offset) % 6)
    elif 8 < (t+time_offset) % 12 < 10:
        rear_lower_ang = -51
    else:   # 10 < (t+time_offset) < 12
        rear_lower_ang = -51 + 6 * (((t+time_offset) % 6) - 4)

    return rear_lower_ang


# function to get tail pipe angle
def get_tail_ang():
    global time
    t = time

    if (t % 12) < 6:
        tail_ang = 30 - 10 * (t % 6)
    else:
        tail_ang = -30 + 10 * (t % 6)

    return tail_ang


# draw dog body and call function for each part of dog
def draw_dog():
    global speed, dog_time, dog_pos
    t = glfw.get_time()
    dog_pos += (t - dog_time) * speed
    dog_time = t

    glPushMatrix()
    glRotate(dog_pos*4, 0, 1, 0)
    glTranslate(0, 1 + 0.7, -5)

    # draw body
    glPushMatrix()
    glScale(2., 1., 1.)
    drawUnitCube()
    glPopMatrix()  # pop to body

    # head
    draw_head()

    # front left leg
    glPushMatrix()
    glTranslate(-.7, -.5 - .05, .4)
    draw_leg(get_front_upper_ang(0), get_front_lower_ang(0), .5)
    glPopMatrix()  # pop to body

    # front right leg
    glPushMatrix()
    glTranslate(-.7, -.5 - .05, -.4)
    draw_leg(get_front_upper_ang(6), get_front_lower_ang(6), .5)
    glPopMatrix()  # pop to body

    # rear left leg
    glPushMatrix()
    glTranslate(.7, -.5 - .05, .4)
    draw_leg(get_rear_upper_ang(6), get_rear_lower_ang(6), .6)
    glPopMatrix()  # pop to body

    # rear right leg
    glPushMatrix()
    glTranslate(.7, -.5 - .05, -.4)
    draw_leg(get_rear_upper_ang(0), get_rear_lower_ang(0), .6)
    glPopMatrix()  # pop to body

    # tail
    draw_tail(get_tail_ang())

    glPopMatrix()  # pop to identity


# render model, projection, viewpoint
def render():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # projection
    glLoadIdentity()
    gluPerspective(45, 1, 1, 100)

    set_camera(-20)

    # redering model
    drawFrame()

    glColor3ub(255, 255, 255)

    draw_dog()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, 'my_dog', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.make_context_current(window)
    glfw.set_scroll_callback(window, scroll_callback)

    global time, speed
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        time = glfw.get_time() * 3 *speed
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
