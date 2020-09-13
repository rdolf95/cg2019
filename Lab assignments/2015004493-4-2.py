import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0
gComposedM = np.identity(4)


def render(M, camAng):

    # enable depth test (we'll see details later)
    glLoadIdentity()
    # use orthogonal projection (we'll see details later)
    glOrtho(-1, 1, -1, 1, -1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    # rotate "camera" position to see this 3D space better (we'll see details later)
    gluLookAt(.1 * np.sin(camAng), .1, .1 * np.cos(camAng), 0, 0, 0, 0, 1, 0)

    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex3fv((M @ np.array([.0, .5, 0., 1.]))[:-1])
    glVertex3fv((M @ np.array([.0, .0, 0., 1.]))[:-1])
    glVertex3fv((M @ np.array([.5, .0, 0., 1.]))[:-1])
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gComposedM

    if action == glfw.PRESS or action == glfw.REPEAT:

        if key == glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key == glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key == glfw.KEY_Q:
            new_m = np.array([[1., 0., 0., -0.1],
                              [0., 1., 0., 0.],
                              [0., 0., 1., 0.],
                              [0., 0., 0., 1.]])
            gComposedM = new_m @ gComposedM
        elif key == glfw.KEY_E:
            new_m = np.array([[1., 0., 0., 0.1],
                              [0., 1., 0., 0.],
                              [0., 0., 1., 0.],
                              [0., 0., 0., 1.]])
            gComposedM = new_m @ gComposedM
        elif key == glfw.KEY_A:
            r = np.pi/180
            new_m = np.array([[np.cos(-10*r),  0., np.sin(-10*r),  0.],
                              [0.,             1.,            0.,  0.],
                              [-np.sin(-10*r), 0., np.cos(-10*r),  0.],
                              [0.,             0.,            0.,  1.]])
            gComposedM = gComposedM @ new_m
        elif key == glfw.KEY_D:
            r = np.pi/180
            new_m = np.array([[np.cos(10*r),  0., np.sin(10*r),  0.],
                              [0.,            1.,           0.,  0.],
                              [-np.sin(10*r), 0., np.cos(10*r),  0.],
                              [0.,            0.,           0.,  1.]])
            gComposedM = gComposedM @ new_m
        elif key == glfw.KEY_W:
            r = np.pi/180
            new_m = np.array([[1.,            0.,             0.,  0.],
                              [0., np.cos(-10*r), -np.sin(-10*r),  0.],
                              [0., np.sin(-10*r),  np.cos(-10*r),  0.],
                              [0.,            0.,             0.,  1.]])
            gComposedM = gComposedM @ new_m
        elif key == glfw.KEY_S:
            r = np.pi/180
            new_m = np.array([[1.,           0.,            0.,  0.],
                              [0., np.cos(10*r), -np.sin(10*r),  0.],
                              [0., np.sin(10*r),  np.cos(10*r),  0.],
                              [0.,           0.,            0.,  1.]])
            gComposedM = gComposedM @ new_m


def main():
    if not glfw.init():
        return

    window = glfw.create_window(480, 480, "2015004493-4-2", None, None)
    if not window:
        glfw.terminate()
        return
    global gComposedM

    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(gComposedM, gCamAng)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
