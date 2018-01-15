import pygame, time, socket, threading
from random import randint as r

#screen set up
pygame.init()

width,height = 640,320

scale = 10

AutoScale = True

#menu setup
tab = 0

tabs = [['Simple Snake','Start','Quit','Settings'],
        ['Gamemode','Single','Double','Online'],
        ['Online Snake','Create','back','Join'],
        ['Offline Settings','Scale','Enable Full Screen','Density']]

#Game set up
ticks = 0

GAMESTATE = "Main"
GAMEMODE = "TwoPlayerOffline"

SUMMARY = ""

DENSITY = 0.025

#create objects
players = []
foods = []

#screen set up
pygame.display.init()
pygame.display.set_mode((width,height),) #pygame.RESIZABLE)
pygame.display.set_caption(" ")
pygame.display.get_surface().fill((255,255,255))
pygame.display.set_icon(pygame.Surface((32,32)))
text = pygame.font.SysFont("monospace", int(width/12.8)).render("Loading", 1, (0,0,0))
pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2))

pygame.display.flip()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

#Handle Client thread
def ClientControlConn(addr,conn):
    players+=[player(str(addr))]
    try:
        while 1:
            for p in players:
                if p.name == str(addr):
                    p.direct = s.recv(1024).decode('utf-8')
    except:
        p.health = False
        conn.close()
                    
#Compare List values
def CompareList(thelist,testvalue):
    if len(thelist) == 0: return False
    for x in thelist:
        if x != testvalue:
            return False
    return True

#populate foods
def populateFoods(density):
    global foods
    if density < 0: density = 0
    if density > 1: density = 1
    for X in range(0,int(((width/scale*height/scale))*density)): foods.append(food())

#player class
class player:
    def __init__(self,name="bot",length=5,color = (r(0,255),r(0,255),r(0,255))):
        global width
        global height
        self.x,self.y = r(0,width/scale-1),r(0,height/scale-1)
        self.trail = []
        self.length = length
        self.initalLength = length
        self.name = name
        self.health = True
        self.direct = r(1,4)
        self.color = color

    def respawn(self):
        self.x,self.y = r(0,width/scale-1),r(0,height/scale-1)
        self.trail = []
        self.length = self.initalLength
        self.health = True
        self.direct = r(1,4)

#food class
class food:
    def __init__(self):
        global width
        global height
        self.x,self.y = r(0,width/scale-1),r(0,height/scale-1)
        self.value = 1
        self.color = (0,0,0)
        
    def respawn(self):
        self.x,self.y = r(0,width/scale-1),r(0,height/scale-1)

while GAMESTATE.lower() != "end":

    #reset vars
    click = 0,0
    
    #Detect End Game for each Gamemode
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
    
    #Process user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMESTATE = "End"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if GAMESTATE == "Paused": GAMESTATE = "Playing"
            elif GAMESTATE == "Playing": GAMESTATE = "Paused"
            elif GAMESTATE == "Main":
                if tab <= 0: GAMESTATE = "End"
                else: tab-= 1
            else: GAMESTATE = "Main"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if GAMESTATE == "Paused": GAMESTATE = "Playing"
                elif GAMESTATE == "Playing": GAMESTATE = "Paused"
                elif GAMESTATE == "Main": GAMESTATE = "END"
                else: GAMESTATE = "Main"
            if GAMESTATE == "Playing":
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

    #Hosting
    if GAMESTATE == "Hosting":
        for x in conns:
            x.sendall(str("players = "+str(players)+"\nfoods = "+str(foods)).encode('utf-8'))

    #Remote
    if GAMESTATE == "Remote":
        for p in players:
            for pos in p.trail:
                pygame.draw.rect(pygame.display.get_surface(), p.color, (pos[0]*scale,pos[1]*scale,scale,scale), 0)
        for f in foods:
            pygame.draw.rect(pygame.display.get_surface(), f.color, (f.x*scale,f.y*scale,scale,scale), 0)
        
    #Calculate Movement
    if GAMESTATE in ["Playing","Hosting"]:
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
                if p.x > width/scale-1:
                    p.x = 0
                elif p.x < 0:
                    p.x = width/scale-1
                elif p.y > height/scale-1:
                    p.y = 0
                elif p.y < 0:
                    p.y = height/scale-1
            else:
                p.x = -1
                p.y = -1

            #Handle player trail
            p.trail = [[p.x,p.y]]+p.trail[:p.length-1]
            
            #Draw Player
            for pos in p.trail:
                pygame.draw.rect(pygame.display.get_surface(), p.color, (pos[0]*scale,pos[1]*scale,scale,scale), 0)

        #mannage/draw food
        for f in foods:
            pygame.draw.rect(pygame.display.get_surface(), f.color, (f.x*scale,f.y*scale,scale,scale), 0)
        
    #Paused
    elif GAMESTATE == "Paused":
        text = pygame.font.SysFont("monospace", int(width/12.8)).render("Paused", 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))

    #Game Over
    elif GAMESTATE == "GameOver":
        text = pygame.font.SysFont("monospace", int(width/12.8)).render("Game Over", 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))
        text = pygame.font.SysFont("monospace", int(width/25.6)).render(SUMMARY, 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2+(height/25.6)))
        players = []
        foods = []
            
    #Main menu
    elif GAMESTATE == "Main":

        text = pygame.font.SysFont("monospace", int(width/12.8)).render("Simple Snake", 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))
        
        pygame.draw.rect(pygame.display.get_surface(), (0,0,0), (0.015*width,height/3,width/3-0.015*width,height/3), 0)
        pygame.draw.rect(pygame.display.get_surface(), (0,0,0), (0.015*width+width/3,height/3,width/3-0.015*width,height/3), 0)
        pygame.draw.rect(pygame.display.get_surface(), (0,0,0), (0.015*width+width*2/3,height/3,width/3-0.015*width*2,height/3))

        text = pygame.font.SysFont("bold", int(width/25.6)).render(tabs[tab][1], 1, (255,255,255))
        pygame.display.get_surface().blit(text, (width/6-text.get_rect().width/2, height/2-text.get_rect().height/2))
        text = pygame.font.SysFont("bold", int(width/25.6)).render(tabs[tab][2], 1, (255,255,255))
        pygame.display.get_surface().blit(text, (width/3+width/6-text.get_rect().width/2, height/2-text.get_rect().height/2))
        text = pygame.font.SysFont("bold", int(width/25.6)).render(tabs[tab][3], 1, (255,255,255))
        pygame.display.get_surface().blit(text, (width/3*2+width/6-text.get_rect().width/2, height/2-text.get_rect().height/2))
        
        if click[0]>0.015*width and click[0]<0.015*width+width/3-0.015*width:
            if tab == 0:
                tab = 1
            elif tab == 1:
                print("Single Player Offlie")
                players = [player('player1',color=(50,50,175))]
                foods = []
                populateFoods(DENSITY)
                GAMEMODE = "SinglePlayerOffline"
                GAMESTATE = "Playing"
            elif tab == 2:
                if True:
                    host = ''
                    port = 8000
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.bind((host,port))
                    s.listen()
                    print("Listening on port", port)
                    s.accept()
                    print("connected to",addr)
                    if conn.recv(1024).decode == "WEST/SNAKECLIENT/V2":
                        tab ==0
                        players = [player('player1',color=(250,0,0)),player('player2',color=(0,0,250))]
                        foods = []
                        populateFoods(DENSITY)
                        GAMEMODE = "TwoPlayerOnline"
                        GAMESTATE = "Playing"
                else:
                    print("Failed to create server and accept client")
                    tab == 0
            elif tab == 3:
                width = 640
                height = 320
                pygame.display.set_mode((width,height))
                try:
                    scale = input("Entering large numbers (>30) may make the game unplayable. Be cautious. Enter AUTO for automatic rescaling\nScale: ")
                    if scale.lower() == "auto":
                        scale = 10
                        height,width = 320,640
                    else:
                        scale = int(scale)
                except:
                    print("ERROR")
                    scale = 10
        elif click[0]>0.015*width+width/3-0.015*width and click[0]<0.015*width+width/3+width/3-0.015*width:
            if tab == 0:
                pass
            elif tab == 1:
                print("Two Player Offline")
                players = [player('player1',color=(250,0,0)),player('player2',color=(0,0,250))]
                foods = []
                populateFoods(DENSITY)
                GAMEMODE = "TwoPlayerOffline"
                GAMESTATE = "Playing"
            elif tab == 2:
                tab = 1
            elif tab == 3:
                width = 640*2
                height = 320*2
                scale = 10*2
                pygame.display.set_mode((width,height),pygame.FULLSCREEN)
        elif click[0]>0.015*width+width/3+width/3-0.015*width:
            if tab == 0:
                tab = 3
            elif tab == 1:
                tab = 2
            elif tab == 2:
                pass
                #join server/start game
            elif tab == 3:
                width = 640
                height = 320
                pygame.display.set_mode((width,height))
                try:
                    DENSITY == ifloat(input("Density %100-0"))/100
                    print("Density is now",DENSITY)
                except:
                    print("ERROR")
        if GAMESTATE != "Main": tab = 0

    #Update Display
    pygame.display.flip()

    #tick delay
    time.sleep(0.1)

#end game screen
pygame.display.get_surface().fill((0,0,0))
text = pygame.font.SysFont("monospace", int(width/12.8)).render("Thanks for playing", 1, (255,255,255))
pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2))
pygame.display.flip()
time.sleep(1)

#end pygame
pygame.quit()
