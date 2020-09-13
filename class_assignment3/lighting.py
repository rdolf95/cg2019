from OpenGL.GL import *


def set_light():
    light_color = (.1, .1, .2, 1.)
    glEnable(GL_LIGHTING)
    glEnable(GL_RESCALE_NORMAL)

    # set light
    lighting(GL_LIGHT0, (3., 1.5, 3., 1.), light_color)
    lighting(GL_LIGHT1, (-3., 1.5, 3., 1.), light_color)
    lighting(GL_LIGHT2, (1.5, 3., 3., 1.), light_color)
    lighting(GL_LIGHT3, (-1.5, 3., 3., 1.), light_color)
    lighting(GL_LIGHT4, (0., 6., 3., 1.), light_color)


def set_color(objectColor):
    # material reflectance for each color channel
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)


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
