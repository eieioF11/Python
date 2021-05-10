from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

#window size
width=300
hight=450
#文字のフォント
font = GLUT_BITMAP_TIMES_ROMAN_24

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(width, hight)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"OpenGL Test")      # show window
    glutDisplayFunc(display)         # draw callback function
    init()
    glutMainLoop()

def init():
    """ initialize """
    glClearColor(1.0, 1.0, 1.0, 1.0)#背景色(白)


s=0.05#小さいダイヤのサイズ
p1=[[-0.9,0.8],[0.9,-0.75]]#ダイヤの位置(小さいダイヤ)
p2=[[0.35,-0.1],[0.0,0.0],[-0.35,0.1]]#ダイヤの位置(中心の３つのダイヤ)



def display():
    """ display """
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)#色指定(赤)
    #小さいダイヤ表示
    for i in range(2):
        glLoadIdentity()#初期化
        glTranslatef(p1[i][0],p1[i][1], 0)#移動
        glRotatef(45, 0.0, 0.0, 1.0)#回転
        glBegin(GL_POLYGON)
        #辺の指定
        glVertex2f(-s,s)
        glVertex2f(s,s)
        glVertex2f(s,-s)
        glVertex2f(-s,-s)
        glEnd()
    #文字表示
    glWindowPos2f(10,430)
    glutBitmapString(font, b"3")
    glWindowPos2f(280,10)
    glutBitmapString(font, b"3")
    #中心の３つのダイヤ表示
    for i in range(3):
        glLoadIdentity()#初期化
        glTranslatef(p2[i][0],p2[i][1], 0)#移動
        glRotatef(45, 0.0, 0.0, 1.0)#回転
        glBegin(GL_POLYGON)
        #辺の指定
        glVertex2f(-0.15+0.5*(i-1),0.15)
        glVertex2f(0.15+0.5*(i-1),0.15)
        glVertex2f(0.15+0.5*(i-1),-0.15)
        glVertex2f(-0.15+0.5*(i-1),-0.15)
        glEnd()
    glFlush()  # enforce OpenGL command

if __name__ == "__main__":
    main()