from camera import *
from lighting import *
from bvh_viewer import *
from OpenGL.GLU import *


# draw coodinate axis and xy palne with rectangular grid
def drawFrame():
    glBegin(GL_LINES)
    glNormal3f(0, 0, 1)
    glVertex3fv(np.array([-1., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glVertex3fv(np.array([0., -1., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glVertex3fv(np.array([0., 0., -1.]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()

    for i in range(-10, 10):
        glBegin(GL_LINES)
        glVertex3fv(np.array([i, 0., 11.]))
        glVertex3fv(np.array([i, 0., -11.]))
        glVertex3fv(np.array([11., 0., i]))
        glVertex3fv(np.array([-11., 0., i]))
        glEnd()


# render model, projection, viewpoint
def render():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    set_camera(-10)
    if get_lighting_mode() is True:
        set_light()
        set_color((.3, .3, .3, 1.))

    # redering model
    drawFrame()
    if get_lighting_mode() is True:
        set_color((0., .25, .3, 1.))
    render_hierarchy()

    if get_lighting_mode() is True:
        glDisable(GL_LIGHTING)


def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, 'my_bvh_viewer', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.make_context_current(window)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
