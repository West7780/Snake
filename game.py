import pygame, time
from random import randint as r

timer = time.clock

#screen set up
pygame.init()

width,height = 640,320

Scale = 10

pygame.display.init()
pygame.display.set_mode((width,height),pygame.RESIZABLE)
pygame.display.set_caption(" ")
pygame.display.get_surface().fill((255,255,255))
pygame.display.set_icon(pygame.Surface((32,32)))
pygame.display.flip()

#player class
class player:
    def __init__(self,name="bot",length=5,color = (r(0,200),r(0,200),r(0,200))):
        global width
        global height
        self.x,self.y = r(0,width/Scale-1),r(0,height/Scale-1)
        self.trail = []
        self.length = length
        self.initalLength = length
        self.name = name
        self.health = True
        self.direct = r(1,4)
        self.color = color

    def respawn(self):
        self.x,self.y = r(0,width/Scale-1),r(0,height/Scale-1)
        self.trail = []
        self.length = self.initalLength
        self.health = True
        self.direct = r(1,4)

#food class
class food:
    def __init__(self):
        global width
        global height
        self.x,self.y = r(0,width/Scale-1),r(0,height/Scale-1)
        self.value = 1
        self.color = (0,0,0)
        
    def respawn(self):
        self.x,self.y = r(0,width/Scale-1),r(0,height/Scale-1)

#game set up
log = ""
DEBUG = 0
GAMESTATE = 1
GAMEMODE = 0

while GAMESTATE != -1:

    #create objects
    players = [player('player1',color=(250,0,0)),player('player2',color=(0,0,250))]
    foods = []
    if GAMEMODE in [0,1]: pygame.display.set_mode((width,height),pygame.RESIZABLE)
    else: pygame.display.set_mode((width,height))

    for X in range(0,int(((width/Scale)*(height/Scale))/500)): foods.append(food())
    #for X in range(0,23): players.append(player())
    
    while GAMESTATE == 1:
        #log
        if DEBUG == 1: log+=str(int(timer()*10)/10)
        
        #event handling
        for event in pygame.event.get():
            if event.type not in [pygame.MOUSEMOTION,pygame.ACTIVEEVENT] and DEBUG == 1:
                log+="\t"+str(timer())+str(event)
            if event.type == pygame.QUIT:
                GAMESTATE = -1
            if(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pass
                #ADD PAUSE CODE HERE
            if event.type == 16:
                width = int(event.w/Scale)*Scale
                height = int(event.h/Scale)*Scale
                if width < 150:
                    width = 15*Scale
                elif height < 150:
                    height = 15*Scale
                pygame.display.set_mode((width,height),pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                for p in players:
                    if p.name == "player1":
                        if event.unicode == "w" and p.direct != 3:
                            p.direct = 1
                        elif event.unicode == "s" and p.direct != 1:
                            p.direct = 3
                        elif event.unicode == "d" and p.direct != 4:
                            p.direct = 2
                        elif event.unicode == "a" and p.direct != 2:
                            p.direct = 4
                    if p.name == "player2" and GAMEMODE == 1:
                        if event.key == 273 and p.direct != 3:
                            p.direct = 1
                        elif event.key == 274 and p.direct != 1:
                            p.direct = 3
                        elif event.key == 275 and p.direct != 4:
                            p.direct = 2
                        elif event.key == 276 and p.direct != 2:
                            p.direct = 4
                                
        #Reset background       
        pygame.display.get_surface().fill((255,255,255))

        #mannage/draw players
        for p in players:

            if p.health:
                #movement
                if p.direct == 1:
                    p.y-=1
                if p.direct == 2:
                    p.x+=1
                if p.direct == 3:
                    p.y+=1
                elif p.direct == 4:
                    p.x-=1

                #player v player collision
                for p2 in players:
                    if p2 != p:
                        if [p.x,p.y] in p2.trail:
                            p.health = False
                            p.x,p.y = -1,-1
                    else:
                        if [p.x,p.y] in p.trail[1:]:
                            p.health = False
                            p.x,p.y = -1,-1

                #player v food collisions
                for f in foods:
                    if [p.x,p.y] == [f.x,f.y]:
                        p.length+=1
                        f.respawn()
                
                #Handle edge of screen
                if p.x > width/Scale-1:
                    p.x = 0
                elif p.x < 0:
                    p.x = width/Scale-1
                elif p.y > height/Scale-1:
                    p.y = 0
                elif p.y < 0:
                    p.y = height/Scale-1

            #Handle player trail
            p.trail = [[p.x,p.y]]+p.trail[:p.length-1]
            
            #Draw Player
            for pos in p.trail:
                pygame.draw.rect(pygame.display.get_surface(), f.color, (pos[0]*10,pos[1]*10,10,10), 0)

            #DEBUG extra info for the log
            if DEBUG == 1:
                log+=("\t"+str(p.x)+","+str(p.y))

        #mannage/draw food
        for f in foods:
            pygame.draw.rect(pygame.display.get_surface(), f.color, (f.x*10,f.y*10,10,10), 0)
            
        #Update Display
        pygame.display.flip()

        #tick delay
        time.sleep(0.1)

#end game screen
pygame.display.get_surface().blit(pygame.font.SysFont("monospace", 50).render("Game Over", 1, (0,0,0)), (width/2-110, height/2-110))
pygame.display.flip()
time.sleep(3)

#end pygame
pygame.quit()
