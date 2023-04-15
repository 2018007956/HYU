import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gCamHeight = .1

def render():
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glEnable(GL_DEPTH_TEST) -> 먼저 그린 것이 위에 오게 하는 코드

    glLoadIdentity()

    glColor3ub(255, 255, 255)
    drawTriangle()
    drawFrame()

    # Blue - rotate and translate
    #  will update the current matrix to TR
    glColor3ub(0, 0, 255)
    glTranslatef(.6, 0, 0)
    glRotatef(30, 0, 0, 1)
    drawTriangle()
    drawFrame()

    # Red - translate and rotate
    #  will update the current matrix to RT
    glLoadIdentity()
    glColor3ub(255, 0, 0)
    glRotatef(30, 0, 0, 1)
    glTranslatef(.6, 0, 0)
    drawTriangle()
    drawFrame()

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
    glVertex2fv(np.array([.0, .5]))
    glVertex2fv(np.array([.0, .0]))
    glVertex2fv(np.array([.5, .0]))
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2018007956', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()