from pygame import *
width = 700
height = 500
win = display.set_mode((width, height))
display.set_caption("Racing")
#задай фон сцены
background = image.load("background.jpg")
background = transform.scale(background, (width, height))

clock = time.Clock()
FPS = 2000

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (80, 80))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < width-80:
            self.rect.x += self.speed
        if key_pressed[K_UP] and self.rect.y > 10:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < height-80:
            self.rect.y += self.speed
        if key_pressed[K_r]:
            self.rect.x = 20
            self.rect.y = height-80

class Enemy(GameSprite):
    diraction = "left"
    def update(self):
        if self.rect.x < 470:
            self.diraction = "right"
        if self.rect.x >= width - 85:
            self.diraction = "left"

        if self.diraction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color1, self.color2, self.color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_rect(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


player = Player("hero.png",20, height-80, 10)
enemy = Enemy("cyborg.png",width-100, 250, 3)
final = GameSprite("treasure.png",width-100, height-100, 0)

wall_1 = Wall(100, 200, 100, 200, 150, 10, 490)
wall_2 = Wall(100, 200, 100, 200, 150, 180, 10)
wall_3 = Wall(100, 200, 100, 530, 30, 10, 250)
wall_4 = Wall(100, 200, 100, 430, 320, 100, 10)
wall_5 = Wall(100, 200, 100, 430, 520, 200, 10 )
wall_6 = Wall(100, 200, 100, 650, 470, 10, 150)

mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()
money = mixer.Sound("money.ogg")

font.init()
font = font.Font(None, 200)
won = font.render("YOU WIN!", True, (0,0,250))

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        win.blit(background, (0,0))
        player.update()
        enemy.update()
        wall_1.draw_rect()
        wall_2.draw_rect()
        wall_3.draw_rect()
        wall_4.draw_rect()
        wall_5.draw_rect()
        wall_6.draw_rect()
        player.reset()
        enemy.reset()
        final.reset()
    
    if sprite.collide_rect(player, final):
        finish = True
        money.play()
        win.blit(won, (50, 200))

    if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, wall_1) or sprite.collide_rect(player, wall_2) or sprite.collide_rect(player, wall_3) or sprite.collide_rect(player, wall_4) or sprite.collide_rect(player, wall_5) or sprite.collide_rect(player, wall_6):
        player.rect.x = 40
        player.rect.y = 600

    display.update()
    clock.tick(FPS)