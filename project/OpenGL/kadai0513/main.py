from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

#window size
width=320
hight=420

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(width, hight)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"OpenGL Test")      # show window
    glutDisplayFunc(display)         # draw callback function
    glutReshapeFunc(reshape)         # resize callback function
    init()
    glutMainLoop()

def init():
    """ initialize """
    glClearColor(0.5, 0.5, 0.5, 1.0)#背景色(灰色)

def drawArrow():
    # Arrow作成
    glLineWidth( 2.0 )
    glColor3f(1.0, 0.0, 0.0)# X-vector ->Red
    glBegin (GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    glVertex3f(0.9, 0.1, 0)
    glVertex3f(1.0, 0, 0)
    glVertex3f(0.9, -0.1, 0)
    glVertex3f(1.0, 0, 0)
    glEnd()
    glColor3f(0.0, 1.0, 0.0)# Y-vector ->Green
    glBegin (GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(0.1, 0.9, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(-0.1, 0.9, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glEnd()
    glColor3f(0.0, 0.0, 1.0)# Z-vector ->Blue
    glBegin (GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 1.0)
    glVertex3f(0.1, 0.0, 0.9)
    glVertex3f(0.0, 0.0, 1.0)
    glVertex3f(-0.1, 0.0, 0.9)
    glVertex3f(0.0, 0.0, 1.0)
    glEnd()

#正方形
vertex = [
[-0.5, 0.0,-0.5 ], # A
[ 0.5, 0.0,-0.5 ], # B
[ 0.5, 1.0,-0.5 ], # C
[-0.5, 1.0,-0.5 ], # D
[-0.5, 0.0, 0.5 ], # E
[ 0.5, 0.0, 0.5 ], # F
[ 0.5, 1.0, 0.5 ], # G
[-0.5, 1.0, 0.5 ]  # H
]
edge = [
[ 0, 1 ], # ア (A-B)
[ 1, 2 ], # イ (B-C)
[ 2, 3 ], # ウ (C-D)
[ 3, 0 ], # エ (D-A)
[ 4, 5 ], # オ (E-F)
[ 5, 6 ], # カ (F-G)
[ 6, 7 ], # キ (G-H)
[ 7, 4 ], # ク (H-E)
[ 0, 4 ], # ケ (A-E)
[ 1, 5 ], # コ (B-F)
[ 2, 6 ], # サ (C-G)
[ 3, 7 ]  # シ (D-H)
]

#四角錐
vertex2 = [
[-0.8, 1.0,-0.8 ], # A
[ 0.8, 1.0,-0.8 ], # B
[-0.8, 1.0, 0.8 ], # C
[ 0.8, 1.0, 0.8 ], # D
[ 0.0, 2.0, 0.0 ]  # E
]
edge2 = [
[ 0, 1 ], # ア (A-B)
[ 1, 3 ], # イ (B-D)
[ 3, 2 ], # ウ (D-C)
[ 2, 0 ], # エ (C-A)
[ 0, 4 ], # オ (A-E)
[ 1, 4 ], # カ (B-E)
[ 2, 4 ], # キ (C-E)
[ 3, 4 ]  # ク (D-E)
]

def display():
    """ display """
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)#色指定
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    ##set camera
    gluLookAt(8.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glRotated(-36.0, 0.0, 0.0, 1.0)
    glRotated(45.0, 0.0, 1.0, 0.0)
    #図形表示
    glBegin(GL_LINES)
    for i in range(12):
        glVertex3dv(vertex[edge[i][0]])
        glVertex3dv(vertex[edge[i][1]])
    for i in range(8):
        glVertex3dv(vertex2[edge2[i][0]])
        glVertex3dv(vertex2[edge2[i][1]])
    glEnd()
    drawArrow()# ３次元軸表示
    glFlush()  # enforce OpenGL command

def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0,float(width)/float(height), 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

if __name__ == "__main__":
    main()