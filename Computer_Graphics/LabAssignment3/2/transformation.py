import glfw
from OpenGL.GL import *
import numpy as np

global gComposedM
gComposedM = np.identity(3)

def render(T):
    global gComposedM
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((T @ np.array([.0, .5, 1.]))[:-1])
    glVertex2fv((T @ np.array([.0, .0, 1.]))[:-1])
    glVertex2fv((T @ np.array([.5, .0, 1.]))[:-1])
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if action == glfw.PRESS or action==glfw.REPEAT:
        if key == glfw.KEY_W:
            newM = np.array([[1., 0., 0.],
                             [0., .9, 0.],
                             [0., 0., 1.]])
        elif key==glfw.KEY_E :
            newM = np.array([[1., 0., 0.],
                             [0., 1.1, 0.],
                             [0., 0., 1.]])
        elif key==glfw.KEY_S :
            t = np.radians(10)
            newM = np.array([[np.cos(t), -np.sin(t), 0.],
                             [np.sin(t), np.cos(t), 0.],
                             [0., 0., 1.]])
        elif key==glfw.KEY_D :
            t = np.radians(-10)
            newM = np.array([[np.cos(t), -np.sin(t), 0.],
                             [np.sin(t), np.cos(t), 0.],
                             [0., 0., 1.]])
        elif key==glfw.KEY_X :
            newM = np.array([[1., 0., .1],
                             [0., 1., 0.],
                             [0., 0., 1.]])
        elif key==glfw.KEY_C :
            newM = np.array([[1., 0., -.1],
                             [0., 1., 0.],
                             [0., 0., 1.]])
        elif key==glfw.KEY_R :
            newM = np.array([[-1., 0., 0.],
                             [0., -1., 0.],
                             [0., 0., 1.]])
        elif key==glfw.KEY_1 :
            newM = np.identity(3)
            gComposedM = np.identity(3)
        else:
            return

        gComposedM = newM @ gComposedM

def main():
    global gComposedM
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2018007956", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(gComposedM)

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
