# globals
# g.py - globals for Numbers
import pygame,utils

XO=False # affects the pygame.display.set_mode() call only
app='Numbers'; ver='1.0'
ver='1.1'
# lighter buttons - except "new"
# added new1() call when level changed
# event q cleared straight after animation
# new style g.py - all globals are initialised to empty
#                - then main() calls g.init() to give them their proper values
ver='1.2'
# display moved up .5
# magician added
# improved score display
# load/save of level
ver='1.3'
# can click on level marks
ver='1.4'
# sugar cursor
ver='1.5'
# uses copy.copy(rect) instead of rect.copy() in utils
ver='1.6' # <<< Release 3
# shows initial animation
ver='1.7'
# utils with improved slider sensitivity
ver='1.8'
# fixed for widescreen
# back button ok after correct
ver='1.9'
# rationalised g.py
# removed Esc on XO
# no sound
ver='2.0'
# sugar
ver='3.0'
# redraw implemented
ver='3.1'
# level 1 - all + or x
ver='4.0'
# new sugar cursor etc

def init(): # called by main()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    if pygame.font:
        t=int(64*imgf); font1=pygame.font.Font(None,t)
        t=int(72*imgf); font2=pygame.font.Font(None,t)
    message=''
    active=True # window has focus?
    
    # this activity only
    global sp,sp1,sp2
    sp=sy(.3) # space between digits in single number
    sp1=sy(2) # space between numbers
    sp2=sy(1.5) # space between numbers and symbols
    global nos_k,signs,max_n,buffr,aim,top,level,score
    nos_k=3 # number of numbers offered
    signs=('=','+','*')
    max_n=5 # biggest number
    buffr=[]
    aim=0
    top=[]
    level=1
    score=0
    # images
    global magician,sparkle,target,smiley,plus,times,equals,n,n_glow,n_pale
    magician=utils.load_image('magician.png',True)
    sparkle=utils.load_image('sparkle.png',True)
    target=utils.load_image('target.png',True)
    smiley=utils.load_image('smiley.png',True)
    plus=utils.load_image('plus.png',True)
    times=utils.load_image('times.png',True)
    equals=utils.load_image('equals.png',True)
    n=[] # 0 to 9 images
    n_glow=[] # ... with glow
    n_pale=[]
    for i in range(10):
        img=utils.load_image(str(i)+'.png',True); n.append(img)
        img=utils.load_image(str(i)+'g.png',True); n_glow.append(img)
        img=utils.load_image(str(i)+'s.png',True); n_pale.append(img)

def sx(f): # scale x function
    return int(f*factor)+offset

def sy(f): # scale y function
    return int(f*factor)
