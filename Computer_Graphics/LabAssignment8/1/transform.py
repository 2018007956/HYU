import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

gCamAng = 0
gComposedM = np.identity(4)

def render(M, camAng):
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()

    # use orthogonal projection (we'll see details later)
    glOrtho(-1,1, -1,1, -1,1)

    # rotate "camera" position to see this 3D space better (we'll see details later)
    gluLookAt(.1*np.sin(camAng),.1, .1*np.cos(camAng), 0,0,0, 0,1,0)

    # draw ccoordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex3fv((M @ np.array([.0,.5,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.0,.0,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.5,.0,0.,1.]))[:-1])
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gComposedM
    newM = np.identity(4)
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_Q:
            # Translate by -0.1 in x direction w.r.t global coordinate
            gComposedM[:3, 3] += [-0.1, 0, 0]
        elif key == glfw.KEY_E:
            # Translate by 0.1 in x direction w.r.t global coordinate
            gComposedM[:3,3] += [0.1, 0, 0]
        elif key == glfw.KEY_A:
            # Rotate about y axis by -10 degrees w.r.t local coordinate
            t = np.radians(-10)
            newM[:3,:3] = np.array([[np.cos(t), 0., np.sin(t)],
                                   [0., 1., 0.],
                                   [-np.sin(t), 0., np.cos(t)]])
        elif key == glfw.KEY_D:
            # Rotate about y axis by 10 degrees w.r.t local coordinate
            t = np.radians(10)
            newM[:3,:3] = np.array([[np.cos(t), 0., np.sin(t)],
                                   [0., 1., 0.],
                                   [-np.sin(t), 0., np.cos(t)]])
        elif key == glfw.KEY_W:
            # Rotate about x axis by -10 degrees w.r.t local coordinate
            t = np.radians(-10)
            newM[:3,:3] = np.array([[1., 0., 0.],
                                   [0., np.cos(t), -np.sin(t)],
                                   [0., np.sin(t), np.cos(t)]])
        elif key == glfw.KEY_S:
            # Rotate about x axis by 10 degrees w.r.t local coordinate
            t = np.radians(10)
            newM[:3,:3] = np.array([[1., 0., 0.],
                                   [0., np.cos(t), -np.sin(t)],
                                   [0., np.sin(t), np.cos(t)]])
        gComposedM = gComposedM @ newM

def main():
    global gComposedM, gCamAng
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2018007956", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gComposedM, gCamAng)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()