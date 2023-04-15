import glfw
from OpenGL.GL import *
import numpy as np

global key_pressed
key_pressed = 'W'
def render():
    global key_pressed
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    a = np.linspace(0,90,4) # [0, 30, 60, 90]
    x = np.abs(np.cos(a*np.pi/180.))
    y = np.abs(np.sin(a*np.pi/180.))
    v = np.column_stack([x,y])

    glBegin(GL_LINE_LOOP)
    for i in range(4):
        glVertex2fv(v[i])
    for i in range(2,0,-1):
        x = -v[i][0]
        glVertex2fv([x,v[i][1]])
    for i in range(4):
        glVertex2fv(-v[i])
    for i in range(2,0,-1):
        y = -v[i][1]
        glVertex2fv([v[i][0],y])
    glEnd()

    glBegin(GL_LINES)
    if key_pressed == 1:
        glVertex2fv(v[2])
    elif key_pressed == 2:
        glVertex2fv(v[1])
    elif key_pressed == 3:
        glVertex2fv(v[0])

    # x축 대칭 (-y)
    elif key_pressed == 4:
        y=-v[1][1]
        glVertex2f(v[1][0],y)
    elif key_pressed == 5:
        y=-v[2][1]
        glVertex2f(v[1][1],y)

    elif key_pressed == 6:
        glVertex2fv(-v[3])
    elif key_pressed == 7:
        glVertex2fv(-v[2])
    elif key_pressed == 8:
        glVertex2fv(-v[1])
    elif key_pressed == 9:
        glVertex2fv(-v[0])

    # y축 대칭 (-x)
    elif key_pressed == 0:
        x = -v[1][0]
        glVertex2f(x,v[1][1])
    elif key_pressed == 'Q':
        x = -v[2][0]
        glVertex2f(x,v[2][1])

    elif key_pressed == 'W':
        glVertex2fv(v[3])

    glVertex2f(0, 0)
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global key_pressed

    if action==glfw.PRESS:
        if key==glfw.KEY_1 :
            key_pressed = 1
        elif key==glfw.KEY_2 :
            key_pressed = 2
        elif key==glfw.KEY_3 :
            key_pressed = 3
        elif key==glfw.KEY_4 :
            key_pressed = 4
        elif key==glfw.KEY_5 :
            key_pressed = 5
        elif key==glfw.KEY_6 :
            key_pressed = 6
        elif key==glfw.KEY_7 :
            key_pressed = 7
        elif key==glfw.KEY_8 :
            key_pressed = 8
        elif key==glfw.KEY_9 :
            key_pressed = 9
        elif key==glfw.KEY_0 :
            key_pressed = 0
        elif key==glfw.KEY_Q :
            key_pressed = 'Q'
        elif key==glfw.KEY_W :
            key_pressed = 'W'


def main():
    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2018007956", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
