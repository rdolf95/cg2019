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
vertex_array = None
normal_array = None
index_array = None
face_normal_array = None
face3_num = 0
polygon_mode = 1
shading_mode = 1
forced_normal = 0.
seperated_vertex = None
light_color = (.1, .1, .2, 1.)
check_normal = False


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

    glTranslate(0, 0, first_eye + zooming)
    x = elav_accumulator @ accumulator
    glMultMatrixf(x.T)


# set key call back to change speed of the dog
def key_callback(window, key, scancode, action, mods):
    global polygon_mode, shading_mode
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_Z:
            if polygon_mode == 0:
                polygon_mode = 1
            else:
                polygon_mode = 0
        if key == glfw.KEY_S:
            if shading_mode == 1 and check_normal == 1:
                shading_mode = 0
            else:
                shading_mode = 1


# after release button -> change to do nothing
def cursor_callback_e(window, xpos, ypos):
    pass


# When left mosue button is clicked and dragged, rotate camera
def cursor_callback(window, xpos, ypos):
    global origin_xpos, origin_ypos, gCamAng, elavation, accumulator, elav_accumulator

    gCamAng = -(np.radians(origin_xpos - xpos)) / 1.5
    elavation = -(np.radians(origin_ypos - ypos)) / 1.5
    origin_xpos = xpos
    origin_ypos = ypos
    rot_matrix = np.array([[np.cos(gCamAng), 0, np.sin(gCamAng), 0],
                           [0, 1, 0, 0],
                           [-np.sin(gCamAng), 0, np.cos(gCamAng), 0],
                           [0, 0, 0, 1]])

    elav_matrix = np.array([[1, 0, 0, 0],
                            [0, np.cos(elavation), -np.sin(elavation), 0],
                            [0, np.sin(elavation), np.cos(elavation), 0],
                            [0, 0, 0, 1]])

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


def drop_callback(window, paths):
    global vertex_array, normal_array, index_array, face_normal_array, face3_num, forced_normal, seperated_vertex, \
        check_normal, shading_mode
    v_arr = []
    n_arr = []
    i_arr = []
    face_normals = []
    names = paths[0].split('/')
    f_name = names[len(names) - 1]
    f = open(paths[0], "r")
    face3_num = 0
    face4_num = 0
    face_over4_num = 0

    while True:
        line = f.readline()
        if not line:
            break
        line = line.rstrip()

        line = line.replace('  ', ' ')
        tag = line.split(' ', 1)

        if tag[0] == 'v':
            vertex = tag[1].split(' ', 3)
            v_arr.append([np.float32(vertex[0]), np.float32(vertex[1]), np.float32(vertex[2])])

        elif tag[0] == 'vn':
            normal = tag[1].split(' ', 3)
            n_arr.append([np.float32(normal[0]), np.float32(normal[1]), np.float32(normal[2])])

        elif tag[0] == 'f':
            face_arr = tag[1].split(' ', 4)
            temp_index = []
            temp_normal = []
            for i in range(3):
                face = face_arr[i].split('/', 3)
                if len(face) < 3:
                    print("This OBJ file has no information of vertex normals.\n"
                          "You can't use [shading using normal data in obj file] mode.")
                    temp_index.append(np.int(face[0]) - 1)
                    check_normal = False
                    shading_mode = 1
                else:
                    temp_index.append(np.int(face[0]) - 1)
                    temp_normal.append(np.int(face[2]) - 1)
                    check_normal = True
            i_arr.append(temp_index)
            if check_normal is True:
                face_normals.append(temp_normal)
            face3_num += 1
            if len(face_arr) == 4:
                face4_num += 1
            elif len(face_arr) > 4:
                face_over4_num += 1

    f.close()
    print("File name:", f_name)
    print("Total number of faces:", face3_num + face4_num + face_over4_num)
    print("Number of faces with 3 vertices:", face3_num)
    print("Number of faces with 4 vertices:", face4_num)
    print("Number of faces with more than 4 vertices:", face_over4_num)

    vertex_array = np.array(v_arr)
    index_array = np.array(i_arr)
    if check_normal is True:
        face_normal_array = np.array(face_normals)
        normal_array = np.array(n_arr)
    forced_normal = calculate_normal()
    seperated_vertex = create_vertex_sperate()


def create_vertex_sperate():
    global vertex_array, normal_array, face_normal_array, index_array, face3_num, check_normal

    varr = []

    for i in range(face3_num):
        for j in range(3):
            if check_normal is True:
                varr.append(normal_array[face_normal_array[i][j]])
            else:
                varr.append(np.array((1., 0., 0.))) # for files with no vertex normal data
            varr.append(vertex_array[index_array[i][j]])

    return np.array(varr)


def draw_vertex_seperate():
    global seperated_vertex, check_normal

    if seperated_vertex is None:
        return
    varr = seperated_vertex

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize,
                    ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 6))


def draw_forced_smooth_shading():
    global vertex_array, index_array, forced_normal

    if vertex_array is None:
        return

    varr = vertex_array
    iarr = index_array
    narr = forced_normal

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glNormalPointer(GL_FLOAT, 3 * narr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3 * varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)


def calculate_normal():
    global face3_num, index_array, vertex_array

    if vertex_array is None:
        return

    narr = []
    normals = []
    for x in range(len(vertex_array)):
        normals.append([])

    for i in range(face3_num):
        p1 = vertex_array[index_array[i][0]]
        p2 = vertex_array[index_array[i][1]]
        p3 = vertex_array[index_array[i][2]]
        temp_normal = np.cross(p1 - p2, p1 - p3)
        temp_normal = temp_normal / np.sqrt(np.dot(temp_normal, temp_normal))

        for j in range(3):
            normals[index_array[i][j]].append(temp_normal)

    for i in range(len(normals)):
        temp_sum = [0., 0., 0.]
        for j in range(len(normals[i])):
            for k in range(3):
                temp_sum[k] += np.float32(normals[i][j][k])
        temp = np.array(temp_sum)
        temp = temp / (np.sqrt(np.dot(temp, temp)))

        narr.append(np.float32(temp))

    return np.array(narr)


def lighting(light_num, light_pos, light_color):
    # lighting

    glEnable(light_num)

    # light position
    glPushMatrix()
    glLightfv(light_num, GL_POSITION, light_pos)
    glPopMatrix()

    # light intensity for each color channel
    specular_color = (1., 1., 1., 1.)
    ambient_color = (.1, .1, .1, 1.)
    glLightfv(light_num, GL_DIFFUSE, light_color)
    glLightfv(light_num, GL_SPECULAR, specular_color)
    glLightfv(light_num, GL_AMBIENT, ambient_color)


# render model, projection, viewpoint
def render():
    global polygon_mode, shading_mode, light_color

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if polygon_mode == 0:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    set_camera(-20)

    glEnable(GL_LIGHTING)
    glEnable(GL_RESCALE_NORMAL)

    # set light
    lighting(GL_LIGHT0, (3., 1.5, 3., 1.), light_color)
    lighting(GL_LIGHT1, (-3., 1.5, 3., 1.), light_color)
    lighting(GL_LIGHT2, (1.5, 3., 3., 1.), light_color)
    lighting(GL_LIGHT3, (-1.5, 3., 3., 1.), light_color)
    lighting(GL_LIGHT4, (0., 6., 3., 1.), light_color)

    # material reflectance for each color channel
    objectColor = (.3, .3, .3, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    # redering model
    drawFrame()

    if shading_mode == 0:
        draw_vertex_seperate()
        light_color = (.1, .1, .3, 1.)
    else:
        draw_forced_smooth_shading()
        light_color = (.3, .1, .1, 1.)

    glColor3ub(255, 255, 255)

    glDisable(GL_LIGHTING)


def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, 'my_viewer', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.make_context_current(window)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()

