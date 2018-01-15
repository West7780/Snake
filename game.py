import pygame, time
from random import randint as r

timer = time.clock

#pygame.font.Font.set_bold(True)

#screen set up
pygame.init()

width,height = 640,320

Scale = 10

#Compare List values
def CompareList(thelist,testvalue):
    if len(thelist) == 0: return False
    for x in thelist:
        if x != testvalue:
            return False
    return True

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

#create objects
players = [player('player1',color=(0,255,0)),player('player2',color=(255,0,0))]
foods = []

for X in range(0,int(((width/Scale)*(height/Scale))/500)): foods.append(food())
#for X in range(0,23): players.append(player())

#screen set up
pygame.display.init()
pygame.display.set_mode((width,height))
pygame.display.set_caption(" ")
pygame.display.get_surface().fill((255,255,255))
pygame.display.set_icon(pygame.Surface((32,32)))
pygame.display.flip()

#game set up
log = ""
DEBUG = 0
GAMESTATE = "Main"
GAMEMODE = "TwoPlayerOffline"
SUMMARY = ""

while GAMESTATE != "End":

    #reset vars
    click = 0,0
    
    #Update Game State
    if GAMEMODE == "TwoPlayerOffline" and GAMESTATE == "Playing":
        for p in players:
            if CompareList(players[0].trail,[-1,-1]) and CompareList(players[1].trail,[-1,-1]):
                GAMESTATE = "GameOver"
                SUMMARY= "Tie Game!\n P1 "+str(players[0].trail-5)+"\n P2 "+str(players[0].trail-5)
            elif CompareList(players[1].trail,[-1,-1]):
                GAMESTATE = "GameOver"
                SUMMARY= "Player 1 Wins!\n P1 "+str(players[0].length-5)+"\n P2 "+str(players[0].length-5)
            elif CompareList(players[0].trail,[-1,-1]):
                GAMESTATE = "GameOver"
                SUMMARY= "Player 2 Wins!\n P1 "+str(players[0].length-5)+"\n P2 "+str(players[0].length-5)
    elif GAMEMODE == "SinglePlayerOffline" and GAMESTATE == "Playing":
        if CompareList(players[0].trail,[-1,-1]):
            GAMESTATE = "GameOver"
            SUMMARY = "Score: "+str(players[0].length-5)
            
    #log
    if DEBUG == 1: log+=str(int(timer()*10)/10)
    
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMESTATE = "End"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if GAMESTATE == "Paused": GAMESTATE = "Playing"
            elif GAMESTATE != "GameOver": GAMESTATE = "Paused"
            else: GAMESTATE = "Main"
        if event.type == pygame.KEYDOWN and event.key == 13:
            GAMESTATE = "Main"
        elif event.type == 16:
            if GAMEMODE == "SinglePlayerOffline":
                width = int(event.w/Scale)*Scale
                height = int(event.h/Scale)*Scale
            if width < 150:
                width = 15*Scale
            elif height < 150:
                height = 15*Scale
            pygame.display.set_mode((width,height))
        elif event.type == pygame.KEYDOWN:
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
                elif p.name == "player2":
                    if event.key == 273 and p.direct != 3:
                        p.direct = 1
                    elif event.key == 274 and p.direct != 1:
                        p.direct = 3
                    elif event.key == 275 and p.direct != 4:
                        p.direct = 2
                    elif event.key == 276 and p.direct != 2:
                        p.direct = 4
        elif event.type == pygame.MOUSEBUTTONUP:
            click = event.pos
                            
    #Reset background       
    pygame.display.get_surface().fill((255,255,255))
    
    #Game Play
    if GAMESTATE == "Playing":
        #mannage/draw players
        for p in players:

            if p.health:
                #movement
                if p.direct == 1:
                    p.y-= 1
                elif p.direct == 2:
                    p.x+= 1
                elif p.direct == 3:
                    p.y+= 1
                elif p.direct == 4:
                    p.x-= 1

                #player v player collision
                for p2 in players:
                    if p2 != p:
                        if [p.x,p.y] in p2.trail:
                            p.health = False
                            p2.length+= p.length-5
                            p.x,p.y = -1,-1
                    else:
                        if [p.x,p.y] in p.trail[1:]:
                            p.health = False
                            p.x,p.y = -1,-1

                #player v food collisions
                for f in foods:
                    if [p.x,p.y] == [f.x,f.y]:
                        p.length+= 1
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
            else:
                p.x = -1
                p.y = -1

            #Handle player trail
            p.trail = [[p.x,p.y]]+p.trail[:p.length-1]
            
            #Draw Player
            for pos in p.trail:
                pygame.draw.rect(pygame.display.get_surface(), p.color, (pos[0]*10,pos[1]*10,10,10), 0)

        #mannage/draw food
        for f in foods:
            pygame.draw.rect(pygame.display.get_surface(), f.color, (f.x*10,f.y*10,10,10), 0)
        
    #Paused
    elif GAMESTATE == "Paused":
        text = pygame.font.SysFont("monospace", int(width/12.8)).render("Paused", 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))

    #Game Over
    elif GAMESTATE == "GameOver":
        if GAMEMODE == "TwoPlayerOffline":
            text = pygame.font.SysFont("monospace", int(width/12.8)).render("Game Over", 1, (0,0,0))
            pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))
            text = pygame.font.SysFont("monospace", int(width/25.6)).render(SUMMARY, 1, (0,0,0))
            for x in range(len(SUMMARY.split("\n"))-1):
                pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2+(height/25.6)))
            
    #Main menu
    elif GAMESTATE == "Main":
        pygame.draw.rect(pygame.display.get_surface(), (0,0,0), (0.015*width,height/3,width/3-0.015*width,height/3), 0)
        pygame.draw.rect(pygame.display.get_surface(), (0,0,0), (0.015*width+width/3,height/3,width/3-0.015*width,height/3), 0)
        pygame.draw.rect(pygame.display.get_surface(), (0,0,0), (0.015*width+width*2/3,height/3,width/3-0.015*width*2,height/3), 0)

        if click[0]>0.015*width and click[0]<0.015*width+width/3-0.015*width:
            print("Option 1")
        elif click[0]>0.015*width+width/3-0.015*width and click[0]<0.015*width+width/3+width/3-0.015*width:
            print("Two Player Offline")
            players = [player('player1',color=(250,0,0)),player('player2',color=(0,0,250))]
            foods = []
            for X in range(0,int(((width/Scale)*(height/Scale))/500)): foods.append(food())
            GAMEMODE = "TwoPlayerOffline"
            GAMESTATE = "Playing"
        elif click[0]>0.015*width+width/3+width/3-0.015*width:
            print("Option 3")
        
    #Update Display
    pygame.display.flip()

    #tick delay
    time.sleep(0.1)

#end game screen
pygame.display.get_surface().fill((0,0,0))
text = pygame.font.SysFont("monospace", int(width/12.8)).render("Thanks for playing", 1, (255,255,255))
pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2))
pygame.display.flip()
time.sleep(3)

#end pygame
pygame.quit()
