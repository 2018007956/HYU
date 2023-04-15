import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.


def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()

def l2norm(v):
    return np.sqrt(np.dot(v, v))

def normalized(v):
    l = l2norm(v)
    return 1/l * np.array(v)

def exp(rv):
    theta = l2norm(rv)
    if theta == 0:
        R = np.identity(4)
        return R

    rv = normalized(rv)
    
    x = rv[0]
    y = rv[1]
    z = rv[2]
    R = np.identity(4)
    
    R[0,0] = np.cos(theta) + x*x*(1-np.cos(theta))
    R[1,0] = y*x*(1-np.cos(theta)) + z*np.sin(theta)
    R[2,0] = z*x*(1-np.cos(theta)) - y*np.sin(theta)

    R[0,1] = x*y*(1-np.cos(theta)) - z*np.sin(theta)
    R[1,1] = np.cos(theta) + y*y*(1-np.cos(theta))
    R[2,1] = z*y*(1-np.cos(theta)) + x*np.sin(theta)

    R[0,2] = x*z*(1-np.cos(theta)) + y*np.sin(theta)
    R[1,2] = y*z*(1-np.cos(theta)) - x*np.sin(theta)
    R[2,2] = np.cos(theta) + z*z*(1-np.cos(theta))
    
    return R

def log(R):
    theta = np.arccos((R[0,0] + R[1,1] + R[2,2] - 1)/2)
    rv0 = (R[2,1] - R[1,2]) / 2*np.sin(theta)
    rv1 = (R[0,2] - R[2,0]) / 2*np.sin(theta)
    rv2 = (R[1,0] - R[0,1]) / 2*np.sin(theta)
    rv = normalized(np.array([rv0, rv1, rv2]))
    return theta*rv

def slerp(R1, R2, t):
    return R1 @ exp(t*log(R1.T @ R2))

def XYZEulerToRotMat(euler):
    x, y, z = euler
    Rx = np.identity(4)
    Ry = np.identity(4)
    Rz = np.identity(4)
    Rx[1:3, 1:3] = np.array([[np.cos(x), -np.sin(x)],
                             [np.sin(x), np.cos(x)]])
    Ry[0, :3] = np.array([np.cos(y), 0, np.sin(y)])
    Ry[2, :3] = np.array([-np.sin(y), 0, np.cos(y)])
    Rz[:2, :2] = np.array([[np.cos(z), -np.sin(z)],
                           [np.sin(z), np.cos(z)]])
    return Rx @ Ry @ Rz

R1ang = [[np.radians(20), np.radians(30), np.radians(30)],
        [np.radians(45), np.radians(60), np.radians(40)],
        [np.radians(60), np.radians(70), np.radians(50)],
        [np.radians(80), np.radians(85), np.radians(70)]]
R2ang = [[np.radians(15), np.radians(30), np.radians(25)],
        [np.radians(25), np.radians(40), np.radians(40)],
        [np.radians(40), np.radians(60), np.radians(50)],
        [np.radians(55), np.radians(80), np.radians(65)]]
        
def Rotate1(t):
    R1 = np.identity(4)
    R2 = np.identity(4)
    
    if t >= 0 and t < 20: 
        euler1 = np.array(R1ang[0])
        R1 = XYZEulerToRotMat(euler1)

        euler2 = np.array(R1ang[1])    
        R2 = XYZEulerToRotMat(euler2)

        R1 = slerp(R1, R2, t/20)
            
    elif t >= 20 and t < 40:
        euler1 = np.array(R1ang[1])
        R1 = XYZEulerToRotMat(euler1)

        euler2 = np.array(R1ang[2])    
        R2 = XYZEulerToRotMat(euler2)

        R1 = slerp(R1, R2, (t - 20)/20)

    elif t >= 40 and t < 60:
        euler1 = np.array(R1ang[2])
        R1 = XYZEulerToRotMat(euler1)

        euler2 = np.array(R1ang[3])    
        R2 = XYZEulerToRotMat(euler2)

        R1 = slerp(R1, R2, (t - 40)/20)

    elif t == 60:
        euler = np.array(R1ang[3]) 
        R1 = XYZEulerToRotMat(euler)

    return R1

def Rotate2(t):
    R3 = np.identity(4)
    R4 = np.identity(4)
    if t >= 0 and t < 20:
        euler1 = np.array(R2ang[0])
        R3 = XYZEulerToRotMat(euler1)

        euler2 = np.array(R2ang[1])    
        R4 = XYZEulerToRotMat(euler2)

        R3 = slerp(R3, R4, t/20)

    elif t >= 20 and t < 40:
        euler1 = np.array(R2ang[1])
        R3 = XYZEulerToRotMat(euler1)

        euler2 = np.array(R2ang[2])    
        R4 = XYZEulerToRotMat(euler2)

        R3 = slerp(R3, R4, (t - 20)/20)

    elif t >= 40 and t < 60:
        euler1 = np.array(R2ang[2])
        R3 = XYZEulerToRotMat(euler1)

        euler2 = np.array(R2ang[3])    
        R4 = XYZEulerToRotMat(euler2)

        R3 = slerp(R3, R4, (t - 40)/20)

    elif t == 60:
        euler = np.array(R2ang[3])    
        R3 = XYZEulerToRotMat(euler)

    return R3

def render(t):
    global gCamAng, gCamHeight, pre_pos
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
  
    objectColor = (1.,1.,1.,1.)        
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    t = (t*10) % 61

    R1 = Rotate1(t)        
    J1 = R1
    
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

        
    R2 = Rotate2(t)
    T1 = np.identity(4)
    T1[0][3] = 1.

    J2 = R1 @ T1 @ R2
   
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    a = [0, 20, 40, 60]
    for i in a:
        
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        if i == 0:
            objectColor = (1., 0., 0., 1.)
            specularObjectColor = (1., 0., 0., 1.)
        elif i == 20:
            objectColor = (1., 1., 0., 1.)
            specularObjectColor = (1., 1., 0., 1.)
        elif i == 40:
            objectColor = (0., 1., 0., 1.)
            specularObjectColor = (0., 1., 0., 1.)
        elif i == 60:
            objectColor = (0., 0., 1., 1.)
            specularObjectColor = (0., 0., 1., 1.)
                    
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
        
        R1 = Rotate1(i)
        R2 = Rotate2(i)
           
        J1 = R1
    
        glPushMatrix()
        glMultMatrixf(J1.T)
        glPushMatrix()
        glTranslatef(0.5,0,0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()

        T1 = np.identity(4)
        T1[0][3] = 1.

        J2 = R1 @ T1 @ R2
       
        glPushMatrix()
        glMultMatrixf(J2.T)
        glPushMatrix()
        glTranslatef(0.5,0,0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()

    glDisable(GL_LIGHTING)
 


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2018007956', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        t = glfw.get_time()
        render(t)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
