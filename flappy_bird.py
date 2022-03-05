from dis import dis
import pygame
import neat
import time
import os
import random

WIN_WIDTH = 576
WIN_HEIGHT = 1024

# 
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        # Velocity is negative because the position relative to the top left 
        # of the screen is down when increasing y
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    
    # Update the bird's position
    def move(self):
        self.tick_count += 1
        
        # displacement = (velocity)(time) + (initial displacement)(time^2)
        displacement = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        if displacement >= 16:
            displacement = 16
        
        if displacement < 0:
            displacement -= 2.5
        
        self.y = self.y + displacement
        
        # Tilt bird up
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.img_count += 1
        
        if self.img_count < self.ANIMATION_TIME: # if < 5
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2: # if < 10
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3: # if < 15
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4: # if < 20
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1: # if < 21
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        # From stack overflow
        rotated_image = pygame.transform.rotate(self.img, self.tilt) # rotate() rotates the img from the top left
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        
        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if t_point or b_point:
            return True
        
        return False


def draw_window(win, bird):
    win.blit(BG, (0,0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)
    
    pygame.quit()
    quit()

main()