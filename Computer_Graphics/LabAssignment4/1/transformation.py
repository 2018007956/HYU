import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

inputkey = []

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw coordinates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()

    glColor3ub(255, 255, 255)

    for key in reversed(inputkey):
        if key == 'Q':
            glTranslatef(-.1, 0., 0.)
        elif key =='E':
            glTranslatef(.1, 0., 0.)
        elif key == 'A':
            glRotatef(10., 0, 0, 1)
        elif key == 'D':
            glRotatef(-10., 0, 0, 1)
        elif key == 1:
            inputkey.clear()
    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([.0,.5]))
    glVertex2fv(np.array([.0,.0]))
    glVertex2fv(np.array([.5,.0]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global inputkey
    if action == glfw.PRESS or action==glfw.REPEAT:
        if key == glfw.KEY_Q:
            inputkey.append('Q')
        elif key==glfw.KEY_E :
            inputkey.append('E')
        elif key==glfw.KEY_A :
            inputkey.append('A')
        elif key==glfw.KEY_D :
            inputkey.append('D')
        elif key==glfw.KEY_1 :
            inputkey.append(1)
        else:
            return

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, '2018007956', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
