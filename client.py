import pygame
import random
import math
import cv2
import mediapipe as mp
from pygame import mixer
import time
import socket
import random
import pygame_gui


# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Sound
#mixer.music.load('background.wav')
#mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player Class
class Player:
    def __init__(self):
        self.image = pygame.image.load('space.png')
        self.x = 370
        self.y = 480
        self.x_change = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

# Enemy Class
class Enemy:
    def __init__(self):
        self.image = pygame.image.load('enemy.png')
        self.x = random.randint(0, 735)
        self.y = random.randint(50, 150)
        self.x_change = 2
        self.y_change = 40

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 2
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -2
            self.y += self.y_change

# Bullet Class
class Bullet:
    def __init__(self):
        self.image = pygame.image.load('bullet.png')
        self.x = 0
        self.y = 480
        self.y_change = 10
        self.state = 'ready'

    def fire(self, x):
        self.state = 'fire'
        self.x = x
        screen.blit(self.image, (self.x + 16, self.y + 10))

    def move(self):
        if self.y <= 0:
            self.y = 480
            self.state = 'ready'
        if self.state == 'fire':
            self.fire(self.x)
            self.y -= self.y_change

# Collision Detection
def is_collision(enemy, bullet):
    distance = math.sqrt(math.pow((enemy.x - bullet.x), 2) + math.pow((enemy.y - bullet.y), 2))
    return distance < 27

# Pinch Detection
def is_pinch(landmarks):
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    distance = math.sqrt(
        (thumb_tip.x - index_tip.x) ** 2 +
        (thumb_tip.y - index_tip.y) ** 2 +
        (thumb_tip.z - index_tip.z) ** 2
    )
    return distance < 0.05  



# Initialize player, enemies, and bullet
player = Player()
enemies = [Enemy() for _ in range(6)]
bullet = Bullet()

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX, textY = 10, 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    score = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(score, (200, 250))

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# OpenCV Video Capture
cap = cv2.VideoCapture(1)


def start_screen():
    s1 = font.render("Single Player", True, (255, 255, 255))
    screen.blit(s1, (280, 150))    
    s2 = font.render("Multi Player", True, (255, 255, 255))
    screen.blit(s2, (280, 250))    
    s3 = font.render("Exit", True, (255, 255, 255))
    screen.blit(s3, (280, 350))    

def draw_selection(option):
    arrow = font.render("->", True, (255, 255, 255))
    screen.blit(arrow, (245, 148+option*100))  

def multiplayer_screen():
    s1 = font.render("Create Room", True, (255, 255, 255))
    screen.blit(s1, (280, 150))    
    s2 = font.render("Join Room", True, (255, 255, 255))
    screen.blit(s2, (280, 250))    

def create_room_screen(code):
    s=font.render(f"The code is: {code}", True, (255, 255, 255))
    screen.blit(s, (200, 100)) 
    s1 = font.render("Start", True, (255, 255, 255))
    screen.blit(s1, (280, 250))     

# Game Loop

def final_screen(text):
    temp=font.render("->", True, (255, 255, 255))
    screen.blit(temp,(200,200))

def single_player(max_score):
    # pygame.init()
    accumulated_time=0
    n=0
    running=True
    global score_value
    score_value=0
    st=time.time()
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        
        
        ret, frame = cap.read()
        if not ret:
            break
        start=time.time()
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                height, width, _ = frame.shape
                cx, cy = int(index_finger_tip.x * width), int(index_finger_tip.y * height)

                
                player.x = int((cx / width) * 800) - 32

                
                if is_pinch(hand_landmarks) and bullet.state == 'ready':
                    bullet.fire(player.x)

        cv2.imshow('Frame', frame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.move()
        player.draw()

        for enemy in enemies:
            if enemy.y > 400:
                
                for e in enemies:
                    e.y = 2000
                game_over_text()
                break

            enemy.move()
            if is_collision(enemy, bullet):
                #explosion_sound = mixer.Sound('explosion.wav')
                #explosion_sound.play()
                bullet.y = 480
                bullet.state = 'ready'
                score_value += 1
                enemy.x = random.randint(0, 735)
                enemy.y = random.randint(50, 150)
            enemy.draw()

        bullet.move()
        show_score(textX, textY)
        pygame.display.update()
        end=time.time()
        accumulated_time+=end-start
        n+=1
        if(score_value>max_score):
            return int(time.time()-st)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
def start_multiplayer(client):
    
    # host = '127.0.0.1'  # Server IP address
    # port = 8888         # Server port

    complete_time=single_player(2)
    client_name=str(random.randint(0,100))
    message = f"FINISH-{client_name}-{complete_time}"
    client.sendall(message.encode())
    
    wait_text = font.render("Waiting for the server...", True, (255, 255, 255))
    screen.blit(background,(0,0))
    screen.blit(wait_text, (250, 250))
    pygame.display.update()
    data = client.recv(1024)
    data=data.decode()
    temp1=data.strip().split('-')
    text=""
    rank=0
    dist=[]
    print(temp1)
    for index,i in enumerate(temp1):
    
        text=""
        print(i)
        temp2=i.strip().split(' ')
        
        print(temp2)
        if(len(temp2)<2):
            continue
        id=temp2[0]
        tm=temp2[1]
        text=text+id+"  "+tm
        if(id==client_name):
            rank=index
            text+="<-"
        dist.append(text)
    run=True
    pygame.display.update()
    
    print("\n\n\n\n")
    print(text)
    print(dist)
    while run:
  
        screen.blit(background,(0,0))
        score_text=font.render("The rankings are: ",True,(255,255,255))
        screen.blit(score_text,(200,200))
        for i,pr in enumerate(dist):
            score_text=font.render(str(i+1)+(") ")+pr,True,(255,255,255))
            screen.blit(score_text,(200,300+50*(i)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                print("hey")
                run=False
        
    print("we lost")

def create_room():
    
    host = '127.0.0.1'  # Server IP address
    port = 8888         # Server port

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    
    
    running = True
    opt=0
    code=random.randint(1000,9999)
    message=f"CREATE {str(code)}"
    client.sendall(message.encode())
    
    mess=client.recv(1024)
    print(mess.decode())

    
    while running:
        screen.fill((100,120,0))
        #bgimg
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
        time.sleep(0.1)
        create_room_screen(code)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if opt==0:
                        message=f"START"
                        client.sendall(message.encode())
                        
                        mess=client.recv(1024)
                        print(mess.decode())
                        start_multiplayer(client)
                        time.sleep(100)
                
        draw_selection(opt)
        pygame.display.update()

def join_room():
    manager = pygame_gui.UIManager((800, 600))

    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 250), (400, 50)), manager=manager,
                                                     object_id='#main_text_entry')

    clock = pygame.time.Clock()
    
    running=True
    while running:
        UI_REFRESH_RATE = clock.tick(60)/1000
        screen.fill((100,120,0))
        #bgimg
        screen.blit(background,(0,0))
        time.sleep(0.08)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                host = '127.0.0.1'  
                port = 8888         

                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((host, port))
                mess=f"JOIN {event.text}"
                client.sendall(mess.encode())
                
                mess=client.recv(1024)
                print(mess.decode())
                mess=client.recv(1024)
                print(mess.decode())    
                
                start_multiplayer(client)
            
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)

        screen.fill((100,120,0))

        manager.draw_ui(screen)

        pygame.display.update()        

def multi_player():
    running = True
    opt=0
    while running:
        screen.fill((100,120,0))
        #bgimg
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            time.sleep(0.08)
            #print("hey")
            multiplayer_screen()
            
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opt=(opt-1)%2
                    if(opt<0):
                        opt=1
                if event.key == pygame.K_DOWN:
                    opt=(opt+1)%2
                if event.key == pygame.K_RIGHT:
                    if opt==0:
                        create_room()
                    if opt==1:
                        join_room()
                
        
            draw_selection(opt)
            pygame.display.update()
    

        
        
running = True
opt=0
while running:
    screen.fill((100,120,0))
    #bgimg
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        time.sleep(0.08)
        start_screen()
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                opt=(opt-1)%3
                if(opt<0):
                    opt=2
            if event.key == pygame.K_DOWN:
                opt=(opt+1)%3
            if event.key == pygame.K_RIGHT:
                if opt==0:
                    single_player(100000)
                if opt==1:
                    multi_player()
                else:
                    running=False
                    break
        
        draw_selection(opt)
        pygame.display.update()




cap.release()
cv2.destroyAllWindows()
pygame.quit()