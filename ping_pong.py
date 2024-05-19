from pygame import *
from random import *

mixer.init()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font('Arial', 36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        b = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(b)


score = 0
lost = 0
max_lost = 3
goal = 50
text_win = font2.render('ВЫ ВЫИГРАЛИ!!!!!!',    True, (255, 255, 255))
text_losing = font2.render('ВЫ ПРОИГРАЛИ !!!!!!',  True, (255, 255, 255))
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40

            
        

bullets = sprite.Group()
asteroid = sprite.Group()

win_width, win_height = 800, 600
display.set_caption('DUAL')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height-100, 80, 100, 10)
finish = False
run = True
img_bullet = 'bullet.png'
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(6):
    m = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 5))
    monsters.add(m)
for i in range(3):
    n = Asteroid(img_asteroid, randint(80, win_width-80), -40, 80, 50, randint(1, 5))
    asteroids.add(n)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    
    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счет: ' + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Мимо: ' + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        ship.update()
        asteroids.update()
        
        monsters.update()      
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)                       
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(text_losing, (200, 200))

        if score >= goal:
            finish = True
            window.blit(text_win, (200, 200)) 

        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)  
        display.update()
    
    time.delay(50)