from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

#window size
width=320
hight=420

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE) #add double buffer
    glutInitWindowSize(width, hight)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"OpenGL Test")      # show window
    glutDisplayFunc(display)         # draw callback function
    glutReshapeFunc(reshape)         # resize callback function
    glutKeyboardFunc(keyboard)       # キーボードが押されたときに呼び出される関数を登録
    glutSpecialFunc(special)         #特殊キーが押されたとき呼び出される
    glutMouseFunc(mouse)             #　マウスを使用する関数設定
    init()
    glutMainLoop()

def init():
    """ initialize """
    glClearColor(0.5, 0.5, 0.5, 1.0)#背景色(灰色)
    glEnable(GL_DEPTH_TEST)#デプスバッファ有効
    glEnable(GL_CULL_FACE)#カーリングの削除
    #glCullFace(GL_BACK)#裏面消去
    glCullFace(GL_FRONT)#表面消去

def drawArrow():
    # Arrow作成
    glLineWidth( 2.0 )
    glColor3f(1.0, 0.0, 0.0)# X-vector ->Red
    glBegin (GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(2.3, 0.0, 0.0)
    glVertex3f(2.2, 0.1, 0)
    glVertex3f(2.3, 0, 0)
    glVertex3f(2.2, -0.1, 0)
    glVertex3f(2.3, 0, 0)
    glEnd()
    glColor3f(0.0, 1.0, 0.0)# Y-vector ->Green
    glBegin (GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 2.3, 0.0)
    glVertex3f(0.1, 2.2, 0.0)
    glVertex3f(0.0, 2.3, 0.0)
    glVertex3f(-0.1, 2.2, 0.0)
    glVertex3f(0.0, 2.3, 0.0)
    glEnd()
    glColor3f(0.0, 0.0, 1.0)# Z-vector ->Blue
    glBegin (GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 2.3)
    glVertex3f(0.1, 0.0, 2.2)
    glVertex3f(0.0, 0.0, 2.3)
    glVertex3f(-0.1, 0.0, 2.2)
    glVertex3f(0.0, 0.0, 2.3)
    glEnd()

#正方形
vertex = [#点
[-0.5, 0.0,-0.5 ], # A
[ 0.5, 0.0,-0.5 ], # B
[ 0.5, 1.0,-0.5 ], # C
[-0.5, 1.0,-0.5 ], # D
[-0.5, 0.0, 0.5 ], # E
[ 0.5, 0.0, 0.5 ], # F
[ 0.5, 1.0, 0.5 ], # G
[-0.5, 1.0, 0.5 ]  # H
]
face = [#面情報 物体の中心から見て反時計回り
    [ 0, 1, 2, 3, 0],#A-B-C-D面
    [ 1, 5, 6, 2, 1],#B-F-G-C面
    [ 5, 4, 7, 6, 5],#F-E-H-G面
    [ 4, 0, 3, 7, 4],#E-A-D-H面
    [ 4, 5, 1, 0, 4],#E-F-B-A面
    [ 3, 2, 6, 7, 3]#D-C-G-H面
]
color = [#色情報
    [ 1.0, 0.0, 0.0],#Red
    [ 0.0, 1.0, 0.0],#Green
    [ 0.0, 0.0, 1.0],#Blue
    [ 1.0, 1.0, 0.0],#Yellow
    [ 1.0, 0.0, 1.0],#Magenta
    [ 0.0, 1.0, 1.0] #Cyan
]

#四角錐
vertex2 = [
    [-0.8, 1.0,-0.8 ], # A
    [ 0.8, 1.0,-0.8 ], # B
    [-0.8, 1.0, 0.8 ], # C
    [ 0.8, 1.0, 0.8 ], # D
    [ 0.0, 2.0, 0.0 ]  # E
]
face2 = [#面情報 物体の中心から見て反時計回り
    [ 0, 1, 4, 0, 0],#A-B-E面
    [ 1, 3, 4, 1, 1],#B-D-E面
    [ 3, 2, 4, 3, 1],#D-C-E面
    [ 2, 0, 4, 2, 2],#C-A-E面
    [ 0, 2, 3, 1, 0]#A-C-D-B面　ここのみ四角形の面
]#4番目の要素は四列目のもののみ使用　その他は３番めの要素と同じにして三角形の面にした
color2 = [#色情報
    [ 1.0, 0.0, 0.0],#Red
    [ 1.0, 1.0, 0.0],#Yellow
    [ 1.0, 0.0, 1.0],#Magenta
    [ 0.0, 1.0, 0.0],#Green
    [ 0.4, 0.4, 0.4],#Gray?
]

r=0 #回転
d=1 #回転方向
viw=0.0#視点

def display():
    global r
    global d
    """ display """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)#色指定
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    ##set camera
    gluLookAt(11.0, 1.0*viw, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glRotated(45.0, 0.0, 1.0, 0.0)
    #図形表示
    glPushMatrix()#スタック設定
    glRotated(1.0*r, 0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    #立方体表示
    for j in range(6):
        glColor3dv(color[j])#各面の色指定
        for i in range(4):
            glVertex3dv(vertex[face[j][i]])
    glEnd()
    glPopMatrix()#スタックの設定
    #四角錐表示
    glPushMatrix()#スタック設定
    glRotated(-1.0*r, 0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    for j in range(5):
        glColor3dv(color2[j])#各面の色指定
        for i in range(4):
            glVertex3dv(vertex2[face2[j][i]])
    glEnd()
    glPopMatrix()#スタックの設定
    drawArrow()# ３次元軸表示
    #glFlush()  # enforce OpenGL command
    glutSwapBuffers() #double buffer use
    r+=d
    if r>=360:#360で0に戻す
        r=0
    if r<0:#0で360に戻す
        r=360

def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0,float(width)/float(height), 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def idle():
    glutPostRedisplay()#画面を再描画する

def keyboard(*args):
    print(args)
    if args[0] == b"q" or args[0] == b"Q" or args[0] == b"\x1b":#q,Q,escボタンで停止
        print("停止が支持されました")
        sys.exit()
def special(*args):
    global viw
    global d
    print(args)
    d=0#回転停止
    if args[0] == 101:#UP
        glutIdleFunc(idle)
        viw+=1
    elif args[0] == 103:#down
        glutIdleFunc(idle)
        viw-=1

def mouse(*args):
    global d
    print(args)
    if args[0] == 0:#左クリック
        if args[1] == 0:#押されたとき
            glutIdleFunc(idle)
            d=1 #回転方向
        else:
            glutIdleFunc(0)
    elif args[0] == 2:#右クリック
        if args[1] == 0:
            glutIdleFunc(idle)
            d=-1 #回転方向
        else:
            glutIdleFunc(0)
        #else:
            #glutIdleFunc(0)

if __name__ == "__main__":
    main()