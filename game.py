"""
CC BY-NC-ND

To create a LAN two player game, open the game on each computer, have one user
select Host and the other select Join a the main menu. The User who selects
Join will have to go to the console window of their game and enter localhost.

To create an online two player game the Host will have to use the port
forwarding tools on their router to allow outgoing and incoming traffic on port
8000 this only needs to be done once. Then follow the instructions above but
enter the public ip of the host machine instead of local host.
"""


import time, socket
from random import randint as r

#Import pygame and install it if its not installed
try:
    import pygame
except:
    try:
        print('DB > Could not import pygame, attempting to install')
        import pip
        pip.main(['install', 'pygame'])
        import pygame
    except:
        print('Failed to install pygame, try doing this manually by entering\n\n\tpip install pygame\n\ninto your native console (ex:cmd) with the highest permissions (for cmd right click on cmd.exe and select run as administrator)')
        quit()

#import high score and other saved data
try:
    file = open('settings')
    exec(file.read())
    file.close()
except:
    highscore = 0
    file = open('settings','w')
    file.write('highscore = '+str(highscore))
    file.close()

#Socket set up
socket.setdefaulttimeout(10)

#pygame set up
pygame.init()

width,height = 640,320
screen = pygame.display

#create window and loading screen
screen.set_mode((width,height),)
screen.set_caption("Simple Snake")
screen.get_surface().fill((255,255,255))
screen.set_icon(pygame.Surface((32,32)))
text = pygame.font.SysFont("monospace", int(width/12.8)).render("Loading", 1, (0,0,0))
screen.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2))

screen.flip()

#Create Game management vars
gamestate = 'start'
gamemode = 'main'
summary = ''

players = []
foods = []
density = 0.05

#Function to generate all of the food
def generateFoods(d):
    global width
    global height
    global foods
    foods = []
    if d < 1:
        num = range(0,int((width/10)*(height/10)*d))
    else:
        num = range(0,d)
    for x in range(0,d):
        food = [[r(0,width/10-1),r(0,height/10-1)]]
        while food in foods:
            food = [[r(0,width/10-1),r(0,height/10-1)]]
        foods+=food
        

#Function waits for next key press before continuing but also allows the user to quit
def waitForPress():
    while True:
        pygame.event.wait()
        if pygame.event.poll().type == pygame.KEYDOWN:
            return
        elif pygame.event.poll().type == pygame.QUIT:
            gamemode = 'end'

def rrfl(Script=[""]):
    return(Script[r(0,len(Script)-1)])

#Main game loop
while gamemode != 'end':

    #get time
    start = time.time()
    
    #reset screen by drawing background
    screen.get_surface().fill((255,255,255))

    #reset input vars
    keys = ''
    click = [0,0]

    #process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamemode = 'end'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if gamemode == 'single':
                    if gamestate == 'paused': gamestate = 'playing'
                    elif gamestate == 'playing': gamestate = 'paused'
                if gamestate == 'gameover':
                    gamestate = 'start'
                    gamemode = 'main'
            if event.unicode in 'wasd': keys+= event.unicode
            if event.key == 273:
                keys+= 'w'
            elif event.key == 274:
                keys+= 's'
            elif event.key == 275:
                keys+= 'd'
            elif event.key == 276:
                keys+= 'a'
            elif event.unicode == '\r': keys+= 'r'
        elif event.type == pygame.MOUSEBUTTONDOWN: click = event.pos
    
    #Process all activites and game events
    if gamemode in ['single','host'] and gamestate in ['playing']:
        for p in players:
            
            if p['health']:
                
                if p['name'] == 'player1':
                    if 's' in keys.lower() and p['direct'] != 's': p['direct'] = 'n'
                    elif 'w' in keys.lower() and p['direct'] != 'n': p['direct'] = 's'
                    elif 'a' in keys.lower() and p['direct'] != 'e': p['direct'] = 'w'
                    elif 'd' in keys.lower() and p['direct'] != 'w': p['direct'] = 'e'
                
                elif p['name'] == 'player2':
                    if 's' in recived.lower() and p['direct'] != 's': p['direct'] = 'n'
                    elif 'w' in recived.lower() and p['direct'] != 'n': p['direct'] = 's'
                    elif 'a' in recived.lower() and p['direct'] != 'e': p['direct'] = 'w'
                    elif 'd' in recived.lower() and p['direct'] != 'w': p['direct'] = 'e'
                
                if p['tail'][0][0] > 63:
                    p['tail'][0][0] = 0
                elif p['tail'][0][0] < 0:
                    p['tail'][0][0] = 63
                if p['tail'][0][1] > 31:
                    p['tail'][0][1] = 0
                elif p['tail'][0][1] < 0:
                    p['tail'][0][1] = 31
                
                if p['direct'] == 'n': p['tail'] = [[p['tail'][0][0],p['tail'][0][1]+1]] + p['tail'][:p['length']-1]
                elif p['direct'] == 'w': p['tail'] = [[p['tail'][0][0]-1,p['tail'][0][1]]] + p['tail'][:p['length']-1]
                elif p['direct'] == 's': p['tail'] = [[p['tail'][0][0],p['tail'][0][1]-1]] + p['tail'][:p['length']-1]
                elif p['direct'] == 'e': p['tail'] = [[p['tail'][0][0]+1,p['tail'][0][1]]] + p['tail'][:p['length']-1]
                
                for p2 in players:
                    if p2['name'] != p['name']:
                        if p['tail'][0] in p2['tail']:
                            p['health']= False
                            print(p['name']+' struck '+p2['name']+' and died.')
                    else:
                        if p['tail'][0] in p['tail'][1:]:
                            p['health'] = False
                            print(p['name']+' struck '+p2['name']+' and died.')
                
                for f in foods:
                    if f == p['tail'][0]:
                        p['length']+=1
                        foods[foods.index(f)] = [r(0,width/10-1),r(0,height/10-1)]
            
            else:
                p['tail'] = [[-1,-1]] + p['tail'][:p['length']-1]

                gamestate = 'gameover'

                if len(p['tail']) - 5 <= highscore: summary = rrfl(['You can do better than that','did you even try?','good run I guess','no comment',"you really are bad at this aren't you?",'maybe you should play something else'])
                else: summary = rrfl(["New High Score!"]*9+["Fuck You"])
                for pos in p['tail']:
                    if pos != [-1,-1]:
                        gamestate = 'playing'

    #Client networking code
    if gamemode == 'client' and gamestate != 'gameover':
        s.send(('/'+keys).encode('utf-8'))
        recived = s.recv(32704).decode('utf-8').split('|')
        gamestate = recived[0]
        players = eval(recived[1])
        foods = eval(recived[2])
        if gamestate == 'gameover':
            s.close()

    #Host networking code
    elif gamemode == 'host':
        recived = conn.recv(1024).decode('utf-8')
        conn.send((str(gamestate)+'|'+str(players)+'|'+str(foods)).encode('utf-8'))
        if gamestate == 'gameover':
            gamemode = 'client'
            s.close()

    #draw food and players
    if gamemode in ['single','host','client'] and gamestate == 'playing':
        for f in foods:
            pygame.draw.rect(pygame.display.get_surface(), (1,1,1), (f[0]*10,f[1]*10,10,10), 0)
        for p in players:
            for pos in p['tail']:
                pygame.draw.rect(pygame.display.get_surface(), p['color'], (pos[0]*10,pos[1]*10,10,10), 0)

    #draw paused screen
    if gamestate == 'paused' and gamemode == 'single':
        text = pygame.font.SysFont("monospace", int(width/12.8)).render("Paused", 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))

    #draw end game for online
    if gamemode in ['host','client'] and gamestate == 'gameover':
        if players[0]['health'] == False and players[1]['health'] == False:
            summary = 'Tie Game!'
        elif players[0]['health']:
            summary = 'Player 1 Wins!'
        elif players[1]['health']:
            summary = 'player 2 Wins!'
        else:
            esummary = 'Game ended early'
        text = pygame.font.SysFont("monospace", int(width/12.8)).render("Game Over", 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))
        text = pygame.font.SysFont("monospace", int(width/25.6)).render(summary, 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2))
        text = pygame.font.SysFont("monospace", int(width/25.6)).render('player 1 score       '+str(players[0]['length']-5), 1, (0,0,255))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.7))
        text = pygame.font.SysFont("monospace", int(width/25.6)).render('player 2 score       '+str(players[1]['length']-5), 1, (255,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.8))
        text = pygame.font.SysFont("monospace", int(width/25.6)).render('press escape to return to the main menu', 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.9))


    #draw end game for single player
    elif gamemode == 'single' and gamestate == 'gameover':
        if highscore < players[0]['length']-5:
            highscore = players[0]['length']-5
            print('DB > New High Score!')
        file = open('settings','w')
        file.write('highscore = '+str(highscore))
        file.close()
        text = pygame.font.SysFont("monospace", int(width/12.8)).render("Game Over", 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))
        text = pygame.font.SysFont("monospace", int(width/25.6)).render(summary, 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2))
        text = pygame.font.SysFont("monospace", int(width/25.6)).render('your score           '+str(players[0]['length']-5), 1, (0,0,255))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.7))
        text = pygame.font.SysFont("monospace", int(width/25.6)).render('high score           '+str(highscore), 1, (255,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.8))
        text = pygame.font.SysFont("monospace", int(width/25.6)).render('press escape to return to the main menu', 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.9))

    #Main menu
    if gamemode == 'main':
        
        text = pygame.font.SysFont("monospace", int(width/12.8)).render("Simple Snake", 1, (0,0,0))
        pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))
        
        pygame.draw.rect(screen.get_surface(), (0,0,0), (0.015*width,height/3,width/3-0.015*width,height/3), 0)
        pygame.draw.rect(screen.get_surface(), (0,0,0), (0.015*width+width/3,height/3,width/3-0.015*width,height/3), 0)
        pygame.draw.rect(screen.get_surface(), (0,0,0), (0.015*width+width*2/3,height/3,width/3-0.015*width*2,height/3))

        text = pygame.font.SysFont("bold", int(width/25.6)).render('Single', 1, (255,255,255))
        screen.get_surface().blit(text, (width/6-text.get_rect().width/2, height/2-text.get_rect().height/2))
        text = pygame.font.SysFont("bold", int(width/25.6)).render('Host', 1, (255,255,255))
        screen.get_surface().blit(text, (width/3+width/6-text.get_rect().width/2, height/2-text.get_rect().height/2))
        text = pygame.font.SysFont("bold", int(width/25.6)).render('Join', 1, (255,255,255))
        screen.get_surface().blit(text, (width/3*2+width/6-text.get_rect().width/2, height/2-text.get_rect().height/2))

        #option 1
        if click[0]>0.015*width and click[0]<0.015*width+width/3-0.015*width:
            print('DB > Single')
            players = [{'name':'player1','tail':[[r(0,63),r(0,31)]]*5,'length':5,'health':True, 'direct':'n', 'color':(0,255,0)}]
            gamemode = 'single'
            gamestate = 'playing'
            generateFoods(1)

        #option 2
        elif click[0]>0.015*width+width/3-0.015*width and click[0]<0.015*width+width/3+width/3-0.015*width:
            print('DB > 2 Player Host')
            
            screen.get_surface().fill((255,255,255))
            
            text = pygame.font.SysFont("monospace", int(width/12.8)).render("Waiting for Client", 1, (0,0,0))
            pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))

            
            screen.flip()
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            
            s.bind(('',8000))
            print('DB > Listening\nDB > Waiting for client')
            s.listen()
            try:
                conn, addr = s.accept()
                recived = conn.recv(1024).decode('utf-8') 
                if recived == 'WEST/SNAKECLIENT/V4':
                    players = [{'name':'player1','tail':[[r(0,63),r(0,31)]]*5,'length':5,'health':True, 'direct':'n', 'color':(0,0,255)},{'name':'player2','tail':[[r(0,63),r(0,31)]]*5,'length':5,'health':True, 'direct':'n', 'color':(255,0,0)}]
                    gamemode = 'host'
                    gamestate = 'playing'
                    generateFoods(5)
                    conn.send('play'.encode('utf-8'))
                    print('DB > Connected, Starting game')
                    start_time = time.time()
                elif recived.split('/')[1] == 'BROWSER':
                    f = open('gameV4.1.py', 'r')
                    tosend = f.read()
                    f.close()
                    tosend = """s.close()
f = open('gameV4.1.py','w')
f.write('''"""+tosend+"""''')
f.close
f = open("gameV4.1.py")
toexec = f.read()
f.close()
exec(toexec)"""
                    conn.send("print('Script Browser is not supported yet')\ns.close()".encode('utf-8'))
                    s.close()
                    print('DB > Disconnected')
                    gamemode = 'main'
                    gamestate = 'start'
                else:
                    s.close()
                    print('DB > Client supplied an invalid request\n\t'+recived)
                    gamemode = 'main'
                    gamestate = 'start'
            except:
                s.close()
                print('DB > connection failed')
                gamemode = 'main'
                gamestate = 'start'

        #option 3
        elif click[0]>0.015*width+width/3+width/3-0.015*width:
            print('DB > 2 Player Join')

            screen.get_surface().fill((255,255,255))
            
            text = pygame.font.SysFont("monospace", int(width/12.8)).render("Connecting to Host", 1, (0,0,0))
            pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height*.1))
            text = pygame.font.SysFont("monospace", int(width/25.6)).render("Go to the console window", 1, (0,0,0))
            pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2))

            screen.flip()
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            try:
                s.connect((input('Enter host IP: '),8000))
                s.send('WEST/SNAKECLIENT/V4'.encode('utf-8'))
                if s.recv(1024).decode('utf-8') == 'play':
                    gamemode = 'client'
                    gamestate = 'playing'
                    start_time = time.time()
                    print('DB > playing, Host started game')
                else:
                    print('DB > Host did not start the game')
                    s.close()
                    gamemode = 'main'
                    gamestate = 'start'
            except:
                s.close()
                print('DB > connection failed')
                gamemode = 'main'
                gamestate = 'start'

    #update screen 
    screen.flip()

    #slow down game and compensate for lag
    end = time.time()
    if 0.1-(end-start) > 0: time.sleep(0.1-(end-start))

#draw closing screen
pygame.display.get_surface().fill((0,0,0))
text = pygame.font.SysFont("monospace", int(width/12.8)).render("Thanks for playing", 1, (255,255,255))
pygame.display.get_surface().blit(text, (width/2-text.get_rect().width/2, height/2-text.get_rect().height/2))
pygame.display.flip()
