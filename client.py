import pygame
import random
import math
import cv2
import mediapipe as mp
from pygame import mixer
import time

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


def start_screen():
    s1 = font.render("Single Player", True, (255, 255, 255))
    screen.blit(s1, (100, 100))    
    s2 = font.render("Multi Player", True, (255, 255, 255))
    screen.blit(s1, (100, 100))    
    s3 = font.render("Exit", True, (255, 255, 255))
    screen.blit(s1, (100, 100))    



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

# Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# OpenCV Video Capture
cap = cv2.VideoCapture(1)

accumulated_time=0
n=0
# Game Loop
running = True
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
    #print(str((end-start)*1000)+"\n")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()

print("Average time to render a frame: ",accumulated_time/n)
print("Average fps: ",n/accumulated_time)
