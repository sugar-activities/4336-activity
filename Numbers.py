#!/usr/bin/python
# Numbers.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,random,utils,buttons,gtk,sys,slider

class Numbers:
    
    def __init__(self):
        self.level=1
        self.journal=True # set to False if we come in via main()

    def display(self): # called each loop
        g.screen.fill((255,255,192))
        g.screen.blit(g.magician,(g.sx(0),g.sy(18.0)))
        cx=g.sx(26); cy=g.sy(5.0); utils.centre_blit(g.screen,g.target,(cx,cy));
        if g.aim>0: self.display_n_glow(g.aim,(cx,cy))
        x=g.sx(3);y=g.sy(3.0)
        pale=False
        if buttons.active('plus'): pale=True
        for i in range(len(g.top)):
            x=self.display_n(g.top[i],(x,y),True,False,pale);x+=g.sp1
        x=g.sx(3);y=g.sy(13)
        for i in range(len(g.buffr)):
            m=g.buffr[i]
            if m=='plus':
               g.screen.blit(g.plus,(x,y));x+=g.plus.get_width()
            elif m=='times':
               g.screen.blit(g.times,(x,y));x+=g.times.get_width()
            elif m=='equals':
               g.screen.blit(g.equals,(x,y));x+=g.equals.get_width()
            else:
                x=self.display_n(g.buffr[i],(x,y))
            x+=g.sp2
        buttons.draw()
        self.slider.draw()
        if self.correct(): utils.centre_blit(g.screen,g.smiley,(g.sx(16),g.sy(12)))
        if g.score>0: utils.display_score()
        
    def display_n(self,n,(x,y),display=True,glow=False,pale=False): # returns x of right edge
        s=str(n)
        for i in range(len(s)):
            n1=int(s[i:i+1]); img=g.n[n1]
            if glow: img=g.n_glow[n1]
            if pale: img=g.n_pale[n1]
            if display: g.screen.blit(img,(x,y))
            x+=g.n[n1].get_width()+g.sp
        return x-g.sp

    def display_n_glow(self,n,(cx,cy)): # for target
        w=self.display_n(n,(0,0),False)
        extra_w_for_glow=g.n_glow[0].get_width()-g.n[0].get_width()
        x=cx-(w+extra_w_for_glow)/2
        h=g.n_glow[0].get_height(); y=cy-h/2
        self.display_n(n,(x,y),True,True)
        x=cx-w/2
        h=g.n[0].get_height(); y=cy-h/2
        self.display_n(n,(x,y),True,False)

    def do_button(self,button):
        if button=='equals':
            self.calc()
            buttons.off(['plus','times','equals'])
            if self.correct():
                if not g.correct: g.score+=g.level
                g.correct=True
        elif button=='back':
            self.reset()
        elif button=='new':
            self.new1()
        else:
            g.buffr.append(button)
            buttons.off(['plus','times','equals'])

    def reset(self):
        g.top=utils.copy_list(g.nos); g.buffr=[]
        buttons.off(['back','plus','times','equals'])

    def calc(self):
        a=[]
        for i in range(len(g.buffr)):
            if g.buffr[i]=='times':
                ind=len(a)-1; a[ind]*=g.buffr[i+1]; g.buffr[i+1]='ignore'
            elif g.buffr[i]=='ignore':
                pass
            elif g.buffr[i]<>'plus':
                a.append(g.buffr[i])
        n=0
        for i in range(len(a)):
            n+=a[i]
        g.buffr=[];g.top.append(n)

    def check_numbers(self):
        if not buttons.active('plus') and not self.correct():
            (mx,my)=pygame.mouse.get_pos()
            x1=g.sx(3);y1=g.sy(3.5);h=g.n[0].get_height()
            for i in range(len(g.top)):
                x=self.display_n(g.top[i],(x1,y1),False)
                w=x-x1
                rect=pygame.Rect(x1,y1,w,h)
                if rect.collidepoint(mx,my):
                    g.buffr.append(g.top[i]); del g.top[i]
                    buttons.on(['back','plus','times'])
                    if len(g.buffr)>1: buttons.on('equals')
                    return True#****
                x1=x+g.sp1
        return False

    def gen_nos(self):
        l=[]
        for i in range(g.nos_k): l.append(random.randint(1,g.max_n))
        return l

    def gen_aim(self):
        l=utils.copy_list(g.nos)
        #shuffle nos
        lt=utils.shuffle(l)
        #generate answer
        buff=""
        r=random.randint(1,2) # for level 1
        while True:
            n=lt[0]; lt.remove(n); buff+=str(n)
            if len(lt)==0: break
            if g.level>1: r=random.randint(0,2)
            if g.signs[r]=='=':
                n=eval(buff); buff=""; lt.append(n); lt=utils.shuffle(lt)
            else:
                buff=buff+g.signs[r]
        return eval(buff)

    def new1(self):
        g.nos=self.gen_nos();g.aim=self.gen_aim()
        g.top=utils.copy_list(g.nos); g.buffr=[]
        buttons.off(['back','plus','times','equals'])
        g.correct=False
        self.animate()

    def animate(self):
        l=utils.copy_list(g.top); k=g.aim; g.aim=0
        for i in range(len(l)):
             g.top=l[:i+1]; self.display()
             pygame.display.flip(); pygame.time.wait(700)
        g.top=utils.copy_list(g.nos)
        mx=1
        for i in range(g.nos_k): mx*=g.max_n
        for i in range(15):
            g.aim=random.randint(5,mx); self.display()
            pygame.display.flip(); pygame.time.wait(150)
        g.aim=k
        pygame.event.clear()

    def correct(self):
        if len(g.buffr)==0 and len(g.top)==1:
            if g.aim in g.top: return True #****
        return False

    def level1(self):
        g.nos_k=3; l=g.level
        if l>5: g.nos_k=4;l-=5
        g.max_n=l+4
        self.new1()
            
    def run(self):
        g.init()
        if not self.journal:
            utils.load(); self.level=g.level
        else:
            g.level=self.level
        x=g.sx(26); y=g.sy(11.2)
        buttons.Button("new",(x,y))
        x=g.sx(4); y=g.sy(10); dx=g.sy(4)
        buttons.Button("back",(x,y)); x+=dx
        buttons.Button("plus",(x,y)); x+=dx
        buttons.Button("times",(x,y)); x+=dx
        buttons.Button("equals",(x,y))
        self.slider=slider.Slider(g.sx(20.5),g.sy(20.5),10,utils.GREEN)
        if self.journal: # Sugar only
            a,b,c,d=pygame.cursors.load_xbm('my_cursor.xbm','my_cursor_mask.xbm')
            pygame.mouse.set_cursor(a,b,c,d)
        self.level1() # initial animation
        going=True
        while going:
            self.level=g.level
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.redraw=True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display; break
                    bu=buttons.check()
                    if bu=='':
                        if not self.check_numbers():
                            if self.slider.mouse(): self.level1()
                    else: self.do_button(bu) # eg do_button('plus')
            if not going: break
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                pygame.display.flip()
                g.redraw=False
            tf=False
            if pygame.mouse.get_focused(): tf=True
            pygame.mouse.set_visible(tf)
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    game=Numbers()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
