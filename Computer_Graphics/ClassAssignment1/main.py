import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

mouseleft = 0
mouseright = 0
mousewheel = 0

eyex = 7
eyey = 3
eyez = 7
atx = 0
aty = 0
atz = 0
upx = 0
upy = 1
upz = 0

left_click_position0 = 0
left_click_position1 = 0
right_click_position0 = 0
right_click_position1 = 0

Xrotate = 0
Yrotate = 0
Xtranslate = 0
Ytranslate = 0

ortho = 0

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            (-1, -1, -1),   # v0
            (1, -1, -1),    # v1
            (1, 1, -1),     # v2
            (-1, 1, -1),    # v3
            (-1, -1, 1),    # v4
            (1, -1, 1),     # v5
            (1, 1, 1),      # v6
            (-1, 1, 1),     # v7
            ], 'float32')
    iarr = np.array([
        (0, 1, 2, 3),   # 윗면
        (4, 5, 6, 7),   # 밑면
        (0, 1, 5, 4),   # 옆면
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
            ])
    return varr, iarr


def render():
    global eyex, eyey, eyez, atx, aty, atz
    global Xrotate, Yrotate, Xtranslate, Ytranslate
    global ortho

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    if ortho:
        glOrtho(-10, 10, -10, 10, -100, 100)
    else:
        gluPerspective(45, 1, 1, 100)

    gluLookAt(eyex, eyey, eyez, atx, aty, atz, upx, upy, upz)

    # orbit or panning
    glTranslatef(Xtranslate/400, 0, -Xtranslate/400)
    glTranslatef(0, Ytranslate/400, 0)
    glRotatef(Xrotate/50, 0, 1, 0)
    glRotatef(Yrotate/50, 1, 0, -1)

    drawFrame()
    drawGrid()

    drawCube_glDrawElements()

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexAvrray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)  # Enable it to use vertex array
    glVertexPointer(3, GL_FLOAT, 3 * varr.itemsize, varr)
    glDrawElements(GL_QUADS, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-50., 0., 0.]))
    glVertex3fv(np.array([50., 0., 0.]))

    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 50., 0.]))

    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 50.]))
    glVertex3fv(np.array([0., 0., -50.]))
    glEnd()

def drawGrid():
    glBegin(GL_LINES)
    glColor3ub(210, 210, 210)
    for i in range(1, 50):
        glVertex3fv(np.array([i, 0, -50]))
        glVertex3fv(np.array([i, 0, 50]))
    for i in range(1, 50):
        glVertex3fv(np.array([-i, 0, -50]))
        glVertex3fv(np.array([-i, 0, 50]))
    for i in range(1, 50):
        glVertex3fv(np.array([50, 0, i]))
        glVertex3fv(np.array([-50, 0, i]))
    for i in range(1, 50):
        glVertex3fv(np.array([50, 0, -i]))
        glVertex3fv(np.array([-50, 0, -i]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global ortho
    if action == glfw.PRESS:
        if key == glfw.KEY_V:
            # Toggle perspective projection / orthogonal perspective projection
            ortho = not ortho

def button_callback(window, button, action, mod):
    global mouseleft, mouseright
    global left_click_position0, left_click_position1, right_click_position0, right_click_position1
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            mouseleft = 1
            left_click_position0 = glfw.get_cursor_pos(window)[0]
            left_click_position1 = glfw.get_cursor_pos(window)[1]
        elif action == glfw.RELEASE:
            mouseleft = 0

    if button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            mouseright = 1
            right_click_position0 = glfw.get_cursor_pos(window)[0]
            right_click_position1 = glfw.get_cursor_pos(window)[1]
        elif action == glfw.RELEASE:
            mouseright = 0


def cursor_callback(window, xpos, ypos):
    global mouseleft, mouseright
    global left_click_position0, left_click_position1, right_click_position0, right_click_position1
    global Xrotate, Yrotate, Xtranslate, Ytranslate
    # 마우스의 움직임을 3차원 회전으로 변환
    # -> x cursor가 증가하거나 감소하는 경우 좌우로 orbit 혹은 panning
    # -> y cursor가 증가하거나 감소하는 경우 위아래로 orbit 혹은 panning
    if mouseleft:
        # change Azimuth, Elevation angle
        if abs(xpos - left_click_position0) > 0 or abs(left_click_position1 - ypos) > 0:
            Xrotate = Xrotate + xpos - left_click_position0
            Yrotate = Yrotate + ypos - left_click_position1
    if mouseright:
        # change Camera position (:eye point) and Target point (:look-at point)
        if abs(xpos - right_click_position0) > 0 or abs(right_click_position1 - ypos) > 0:
            Xtranslate = Xtranslate + xpos - right_click_position0
            Ytranslate = Ytranslate + right_click_position1 - ypos


def scroll_callback(window, xoffset, yoffset):
    global eyex, eyey, eyez, atx, aty, atz
    # yoffset>0: zoom in, yoffset<0: zoom out
    eyex -= yoffset
    eyey -= yoffset
    eyez -= yoffset
    atx -= yoffset
    aty -= yoffset
    atz -= yoffset

gVertexArrayIndexed = None
gIndexArray = None


def main():
    global gVertexArrayIndexed, gIndexArray

    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "cube manipulation", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)


    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
