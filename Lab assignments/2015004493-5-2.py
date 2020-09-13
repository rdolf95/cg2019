import glfw
import numpy as np
from OpenGL.GL import *


def render(M, N):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    drawFrame()
    glColor3ub(255, 255, 255)
    drawTriangle()

    glMultMatrixf(N)
    glMultMatrixf(M)
    drawFrame()
    glColor3ub(0, 0, 255)
    drawTriangle()



def drawFrame():
    glBegin(GL_LINES)

    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()


def drawTriangle():
    glBegin(GL_TRIANGLES)

    glVertex2fv(np.array([0., .5]))
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([.5, 0.]))
    glEnd()


def main():

    if not glfw.init():
        return

    window = glfw.create_window(480, 480, "2015004493-5-2", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        r = (30 * np.pi) / 180
        rt = np.identity(4)
        rt[:3, :3] = np.array([[np.cos(r), -np.sin(r), 0.],
                              [np.sin(r),   np.cos(r), 0.],
                              [0.,         0.,         1.]])
        tl = np.identity(4)
        tl[:3, 3] = np.array([0.6, 0., 0.])

        render(rt.transpose(), tl.transpose())

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()

