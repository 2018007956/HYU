import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

azimuth = 0
elevation = 0
distance = 5
up = 1
gComposedM = np.identity(4)
w = np.array([0.,0.,1.])
u = np.array([1.,0.,0.])
v = np.array([0.,1.,0.])
origin = np.array([0.,0.,0.])

fcnt = 0
curr_frame = 0

def render():
    global azimuth, elevation, distance
    global origin, up, w, u, v
    global moving, curr_frame
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(45, 1, 1, 100)
   
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    w = np.array([np.cos(elevation)*(np.sin(azimuth)),np.sin(elevation),np.cos(elevation)*(np.cos(azimuth))])
    u = np.cross(np.array([0.,up, 0.]), w)
    u /= np.sqrt(np.dot(u,u))
    v = np.cross(u, w)
    v /= np.sqrt(np.dot(v,v))
    gluLookAt(distance*w[0]+origin[0],distance*w[1]+origin[1],distance*w[2]+origin[2], origin[0],origin[1],origin[2], 0,up,0)

    # draw grid
    glBegin(GL_LINES)
    glColor3ub(64, 64, 64)
    for i in np.linspace(-10, 10, 200):
        glVertex3fv(np.array([-10.,0., i]))
        glVertex3fv(np.array([10.,0., i]))
        glVertex3fv(np.array([i,0., -10.]))
        glVertex3fv(np.array([i,0., 10.]))
    glEnd()

    glEnable(GL_LIGHTING)   
    
    glEnable(GL_NORMALIZE)  
    glEnable(GL_RESCALE_NORMAL)

    glPushMatrix()
    glEnable(GL_LIGHT0)
    lightPos0 = (3.,4.,5.,1.) # point light
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0) 
    glEnable(GL_LIGHT1)
    lightPos1 = (-3.,4.,-5.,1.) 
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glPopMatrix()

    lightColor0 = (1.,0.,1.,1.)
    lightColor1 = (0.,1.,0.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

    # material reflectance for each color channel
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    # glColor3ub(0,255,255)

    drawHierarchy()

    if moving and fcnt != 0: # animation mode & frame file exist
        curr_frame += 1
        curr_frame %= fcnt
    glDisable(GL_LIGHTING)
    
oldpos = (0,0)
newpos = (0,0)
enableOrbit = False
enablePanning = False
face = up

moving = False # Animate the motion
resize = 1

def cursor_callback(window, xpos, ypos):
    global azimuth, elevation, oldpos, newpos
    global enableOrbit, origin, up
    global w, u, v
    if enableOrbit:
        oldpos = newpos
        newpos = glfw.get_cursor_pos(window)
        elevation -= (oldpos[1] - newpos[1])/100
        if np.cos(elevation)<0:
            up = -1
        else:
            up = 1
        azimuth += face*(oldpos[0] - newpos[0])/100
        
    if enablePanning:
        oldpos = newpos
        newpos = glfw.get_cursor_pos(window)
        origin += ((oldpos[0] - newpos[0])*u+(oldpos[1] - newpos[1])*v)/500
        
def button_callback(window, button, action, mod):
    global azimuth, elevation, oldpos, newpos
    global enableOrbit, enablePanning
    global face, up
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            oldpos = glfw.get_cursor_pos(window)
            newpos = glfw.get_cursor_pos(window)
            enableOrbit = True
        elif action==glfw.RELEASE:
            enableOrbit = False
            face = up
            while azimuth > 2*np.pi:
                azimuth -= 2*np.pi
            while azimuth < 0:
                azimuth += 2*np.pi
            while elevation > 2*np.pi:
                elevation -= 2*np.pi
            while elevation < 0:
                elevation += 2*np.pi
    if button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            oldpos = glfw.get_cursor_pos(window)
            newpos = glfw.get_cursor_pos(window)
            enablePanning = True
        elif action==glfw.RELEASE:
            enablePanning = False
        
def scroll_callback(window, xoffset, yoffset):
    global distance
    distance *= 10**(float(-yoffset)/10)

channel_list = []
offset_list = []
motion_list = []

def drop_callback(window, paths):
    global channel_list, offset_list, motion_list, fcnt, resize
    jname_list = [] # joint name
    channel_list = [] # joint stack: rotatation, translation
    offset_list = [] # offset value
    motion_list = [] # motion data: pose
    fcnt = 0 # the number of frames
    fps = 0 # FPS: ?frames/1s
    jcnt = 0 # number of joint
    resize = 1 # resize object
    hierarchy = False
    motion = False

    file = open(paths[0])
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip() # -> remove '\n' 

        if line == 'HIERARCHY': # static data
            hierarchy = True
            motion = False
            continue
        elif line == 'MOTION': # time-varying data
            hierarchy = False
            motion = True
            continue

        parsedline = line.split()

        if hierarchy:
            if parsedline[0] == 'ROOT' or parsedline[0] == 'JOINT':
                jname_list.append(parsedline[1]) # <- ex) Hips, LeftUpLeg ...
                jcnt += 1
            elif parsedline[0] == '{':
                channel_list.append('push')
            elif parsedline[0] == '}':
                channel_list.append('pop')
            elif parsedline[0] == 'OFFSET':
                t = np.array(list(map(float, parsedline[1:])))
                if np.dot(t, t) > 1: 
                    resize = 50 
                offset_list.append(t)
            elif parsedline[0] == 'CHANNELS':
                channel_list.append(parsedline[2:])
        elif motion:
            if parsedline[0] == 'Frames:':
                fcnt = int(parsedline[1])
            elif parsedline[0] == 'Frame' and parsedline[1] == 'Time:':
                fps = 1.0/float(parsedline[2]) # 1/(한 프레임당 시간간격) => 1초에 몇 프레임인지
            else:
                motion_list.append(list(map(float, parsedline)))
                
    print("1. File Name: " + paths[0].split('\\')[-1])
    print("2. Number of Frames: "+str(fcnt))
    print("3. FPS (which is 1/FrameTIme): "+str(fps))
    print("4. Number of Joints: "+str(jcnt))
    print("5. List of all joint names:")
    for n in jname_list:
        print(n, end=' ')

def key_callback(window, key, scancode, action, mods):
    global moving
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            moving = True

def drawHierarchy():
    global moving, channel_list, offset_list, motion_list, curr_frame, resize

    joint_stack = []
    jcnt = 0
    mcnt = 0
    for ch in channel_list:
        if ch == 'push':
            glPushMatrix()
            glTranslatef(offset_list[jcnt][0]/resize, offset_list[jcnt][1]/resize, offset_list[jcnt][2]/resize)
            if len(joint_stack)!=0:
                # glBegin(GL_LINES)
                # glVertex3fv(-offset_list[jcnt]/resize)
                # glVertex3fv(np.array([0.,0.,0.])/resize)
                # glEnd()
                drawCube(-offset_list[jcnt]/resize, np.array([0.,0.,0.])/resize)
                joint_stack.append(joint_stack[-1]+offset_list[jcnt]) # compute hierarchy
            else:
                joint_stack.append(offset_list[jcnt])
            jcnt += 1
        elif ch == 'pop':
            glPopMatrix()
            joint_stack = joint_stack[:-1]
        else:
            if moving:
                for m in ch:
                    m = m.upper()
                    if m == 'XPOSITION':
                        glTranslatef(motion_list[curr_frame][mcnt]/resize, 0, 0)
                    elif m == 'YPOSITION':
                        glTranslatef(0, motion_list[curr_frame][mcnt]/resize, 0)
                    elif m == 'ZPOSITION':
                        glTranslatef(0, 0, motion_list[curr_frame][mcnt]/resize)
                    elif m == 'XROTATION':
                        glRotatef(motion_list[curr_frame][mcnt], 1, 0, 0)
                    elif m == 'YROTATION':
                        glRotatef(motion_list[curr_frame][mcnt], 0, 1, 0)
                    elif m == 'ZROTATION':
                        glRotatef(motion_list[curr_frame][mcnt], 0, 0, 1)
                    mcnt+=1

def drawCube(p1, p2):
    v = p1-p2
    nv = v/np.sqrt(np.dot(v, v)) # normalize
    n = np.array([0.,1.,0.]) # y-axis

    c = np.cross(nv, n)
    cn = np.sqrt(np.dot(c, c))
    theta = np.rad2deg(np.arcsin(cn)) 
    if np.dot(nv, n) < 0:
        theta = 180 - theta
    if cn != 0:
        c /= cn

    glPushMatrix()
    glRotatef(-theta, c[0], c[1], c[2])
    glScalef(.05, np.sqrt(np.dot(v, v)), .05)
    
    glBegin(GL_TRIANGLES)
    glNormal3f(0,0,1) # v0, v2, v1, v0, v3, v2 normal
    glVertex3f( -1 ,  1 ,  1 ) # v0 position
    glVertex3f(  1 ,  0 ,  1 ) # v2 position
    glVertex3f(  1 ,  1 ,  1 ) # v1 position

    glVertex3f( -1 ,  1 ,  1 ) # v0 position
    glVertex3f( -1 ,  0 ,  1 ) # v3 position
    glVertex3f(  1 ,  0 ,  1 ) # v2 position

    glNormal3f(0,0,-1)
    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f(  1 ,  1 , -1 ) # v5
    glVertex3f(  1 ,  0 , -1 ) # v6

    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f(  1 ,  0 , -1 ) # v6
    glVertex3f( -1 ,  0 , -1 ) # v7

    glNormal3f(0,1,0)
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  1 , -1 ) # v5

    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f(  1 ,  1 , -1 ) # v5
    glVertex3f( -1 ,  1 , -1 ) # v4

    glNormal3f(0,-1,0)
    glVertex3f( -1 ,  0 ,  1 ) # v3
    glVertex3f(  1 ,  0 , -1 ) # v6
    glVertex3f(  1 ,  0 ,  1 ) # v2

    glVertex3f( -1 ,  0 ,  1 ) # v3
    glVertex3f( -1 ,  0 , -1 ) # v7
    glVertex3f(  1 ,  0 , -1 ) # v6

    glNormal3f(1,0,0)
    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  0 ,  1 ) # v2
    glVertex3f(  1 ,  0 , -1 ) # v6

    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  0 , -1 ) # v6
    glVertex3f(  1 ,  1 , -1 ) # v5

    glNormal3f(-1,0,0)
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f( -1 ,  0 , -1 ) # v7
    glVertex3f( -1 ,  0 ,  1 ) # v3

    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f( -1 ,  0 , -1 ) # v7
    glEnd()
    glPopMatrix()
    
def main():
    if not glfw.init():
        return
    window = glfw.create_window(1000,1000,"bvh file viewer", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()
if __name__ == "__main__":
    main()