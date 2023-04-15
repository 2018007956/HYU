import os
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

GRID_SIZE = 30

azimuth = 0
elevation = 0
distance = 5
up = 1
gComposedM = np.identity(4)
w = np.array([0.,0.,1.])
u = np.array([1.,0.,0.])
v = np.array([0.,1.,0.])
origin = np.array([0.,0.,0.])

animate = False
wiremode = True
smooth = False

ivarr = np.array([], 'float32')
iarr = np.array([])
varr = np.array([], 'float32')
face = [0] * 6

currentPath = os.getcwd()
path_lego = currentPath+'\\ClassAssignment2\\lego.obj'
path_wheel = currentPath+'\\ClassAssignment2\\wheel.obj'
path_car_body = currentPath+'\\ClassAssignment2\\car_body.obj'

def render():
    global azimuth, elevation, distance
    global origin, up, w, u, v
    global wiremode, smooth
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(45, 1, 1, 100)

    w = np.array([np.cos(elevation)*(np.sin(azimuth)),np.sin(elevation),np.cos(elevation)*(np.cos(azimuth))])
    u = np.cross(np.array([0.,up, 0.]), w)
    u /= np.sqrt(np.dot(u,u))
    v = np.cross(u, w)
    v /= np.sqrt(np.dot(v,v))
    gluLookAt(distance*w[0]+origin[0],distance*w[1]+origin[1],distance*w[2]+origin[2], origin[0],origin[1],origin[2], 0,up,0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if wiremode:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    drawGrid()

    glEnable(GL_LIGHTING)   
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    # light 0
    glPushMatrix()
    lightPos = (3., 4., 5., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    # light 1
    glPushMatrix()
    glRotatef(120, 0, 1, 0)
    lightPos = (-3., -4., 5., 1.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()

    ambientLightColor1 = (.1, .0, .0, 1.)
    diffuseLightColor1 = (.6, .0, .0, 1.)

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor1)
    ambientLightColor2 = (.0, .1, .0, 1.)
    diffuseLightColor2 = (.0, .6, .0, 1.)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor2)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor2)

    # material reflectance for each color channel
    objectColor = (1., 1., 1., 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    if animate == 1:
        hierarchical()
    else:
        if smooth:
            drawObject_glDrawElements()
        else:
            drawObject_glDrawArray()
    
    glDisable(GL_LIGHTING)

def drawGrid():
    glLineWidth(1)
    glColor3ub(255, 255, 255)
    for x in range(-GRID_SIZE, GRID_SIZE):
        glBegin(GL_LINE_LOOP)
        glVertex3f(-GRID_SIZE, 0., x)
        glVertex3f(GRID_SIZE, 0., x)
        glEnd()

    for z in range(-GRID_SIZE, GRID_SIZE):
        glBegin(GL_LINE_LOOP)
        glVertex3f(z, 0., -GRID_SIZE)
        glVertex3f(z, 0., GRID_SIZE)
        glEnd()

def hierarchical():
    global path_lego, path_wheel, path_car_body
    lego = open(path_lego,"r")
    wheel = open(path_wheel,"r")
    car_body = open(path_car_body,"r")

    t = glfw.get_time()

    glPushMatrix()
    glScalef(.3, .3, .3)

    # lego base transformation
    glPushMatrix()
    glTranslatef(10*np.sin(t*0.1), 0, 0)
    draw_object(lego)
    drawObject_glDrawArray()
    
    # wheel movement
    glPushMatrix()
    glRotatef(t* (180 / np.pi), 0, 1, 0)
    draw_object(wheel)
    drawObject_glDrawArray()
    
    # car movement
    glPushMatrix()
    draw_object(car_body)
    drawObject_glDrawArray()

    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()


def draw_object(file):
    # get value & set array
    global ivarr, iarr, varr, cnttotal, cnt3, cnt4, cntn
    tvarr, tnarr, inarr = [], [], []
    varr, iarr, ivarr = [], [], []
    cnttotal, cnt3, cnt4, cntn = 0, 0, 0, 0
    
    while True:
        line = file.readline()
        if not line:
            break
        parsedline = line.split()
        if len(parsedline)==0:
            continue
        if parsedline[0] == 'v':
            list.append(tvarr, (float(parsedline[1]), float(parsedline[2]), float(parsedline[3])))
            list.append(inarr, np.array([0,0,0], 'float32'))
        elif parsedline[0] == 'vn':
            list.append(tnarr, (float(parsedline[1]), float(parsedline[2]), float(parsedline[3])))
        elif parsedline[0] == 'f':
            fv, t, fn = 0, 0, -1
            p = parsedline[1].split('/')
            fv = p[0]
            if len(p)>=3:
                fn = p[2]
            fv = int(fv)
            fn = int(fn)
            sv, sn = None, None
            face_normal = np.array([0.,0.,0.])
            cnt = 0
            it = ()
            cnttotal += 1
            
            for pl in parsedline[2:]:
                a, b, c = 0, 0, -1
                p = pl.split('/')
                a = p[0]
                if len(p)>=3:
                    c = p[2]
                a = int(a)
                c = int(c)
                if (sv != None) and (sn != None):
                    list.append(varr, tuple(np.array(tnarr[fn-1])/np.sqrt(np.dot(np.array(tnarr[fn-1]), np.array(tnarr[fn-1])))))
                    list.append(varr, tvarr[fv-1])
                    it += (fv-1,)
                    
                    list.append(varr, tuple(np.array(tnarr[sn-1])/np.sqrt(np.dot(np.array(tnarr[sn-1]), np.array(tnarr[sn-1])))))
                    list.append(varr, tvarr[sv-1])           
                    it += (sv-1,)

                    list.append(varr, tuple(np.array(tnarr[c-1])/np.sqrt(np.dot(np.array(tnarr[c-1]), np.array(tnarr[c-1])))))
                    list.append(varr, tvarr[a-1])
                    it += (a-1,)

                    face_normal = np.cross(np.array(tvarr[sv - 1]) - np.array(tvarr[fv - 1]), np.array(tvarr[a - 1]) - np.array(tvarr[fv - 1]))
                    face_normal /= np.sqrt(np.dot(face_normal, face_normal))
                    
                    inarr[sv-1] += face_normal
                    
                    list.append(iarr, it)
                    it = ()
                    cnt += 1
                sv = a
                sn = c
            inarr[fv-1] += face_normal
            inarr[sv-1] += face_normal
            if cnt == 1:
                cnt3 += 1
            elif cnt == 2:
                cnt4 += 1
            else:
                cntn += 1
    varr = np.array(varr, 'float32')
    for i in range(len(tvarr)):
        d = np.sqrt(np.dot(inarr[i], inarr[i]))
        if d == 0:
            d = 1
        list.append(ivarr, tuple(inarr[i]/d))
        list.append(ivarr, tvarr[i])
    ivarr = np.array(ivarr, 'float32')
    iarr = np.array(iarr)

def drawObject_glDrawElements():
    global ivarr, iarr
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*ivarr.itemsize, ivarr)
    glVertexPointer(3, GL_FLOAT, 6*ivarr.itemsize, ctypes.c_void_p(ivarr.ctypes.data + 3*ivarr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawObject_glDrawArray():
    global varr
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

    
oldpos = (0,0)
newpos = (0,0)
enableOrbit = False
enablePanning = False
face = up

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

def drop_callback(window, paths):
    global ivarr, iarr, varr, cnttotal, cnt3, cnt4, cntn
    file = open(paths[0])

    draw_object(file)

    print('File name : ' + paths[0].split('\\')[-1])
    print('Total number of faces : '+str(cnttotal))
    print('Number of faces with 3 vertices : '+str(cnt3))
    print('Number of faces with 4 vertices : '+str(cnt4))
    print('Number of faces with more than 4 vertices : '+str(cntn))
    file.close()

def key_callback(window, key, scancode, action, mods):
    global animate, wiremode, smooth
    if action == glfw.PRESS:
        # animating hierarchical model rendering mode
        if key == glfw.KEY_H:
            animate = not animate
        # Toggle wireframe / solid mode by pressing
        elif key == glfw.KEY_Z:
            wiremode = not wiremode
        elif key == glfw.KEY_S:
            smooth = not smooth

    
def main():
    if not glfw.init():
        return
    window = glfw.create_window(1000,1000,"Class2_2018007956", None, None)
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