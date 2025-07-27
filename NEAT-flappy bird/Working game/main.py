import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 288*2
SCREEN_HEIGHT = 1000


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("NEAT-Flappy Bird")

clock = pygame.time.Clock()


bg_raw = pygame.image.load("Working game/Assets/background-day.png").convert()
bg = pygame.transform.scale(bg_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
floor_raw = pygame.image.load("Working game/Assets/base.png").convert()
floor = pygame.transform.scale(floor_raw,(SCREEN_WIDTH, 100))
floor_x = 0

pipe_raw = pygame.image.load("Working game/Assets/pipe-green.png").convert()
pipe_s = pygame.transform.scale(pipe_raw,(100,600))

gravity = 0.25

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height_options = range(250, SCREEN_HEIGHT - 250)

Score = 0

def background():
    global floor_x
    screen.blit(bg,(0,0))
    floor_x -= 1
    if floor_x <= -SCREEN_WIDTH:
        floor_x = 0
    screen.blit(floor, (floor_x, SCREEN_HEIGHT - 100))
    screen.blit(floor, (floor_x + SCREEN_WIDTH, SCREEN_HEIGHT - 100))

class Bird:
    def __init__(self,x,y):
        self.surface = pygame.transform.scale(pygame.image.load("Working game/Assets/bird.png").convert_alpha(), (75, 55))
        self.rect = self.surface.get_rect(center=(x, y))
        self.vel = 0
        self.score = 0

    def update(self):
        self.vel += gravity
        self.rect.centery += self.vel
    
    def jump(self):
        self.vel = -7
        
    def draw(self):
        screen.blit(self.surface, self.rect)

class Pipe:
    def __init__(self,x,height):
        self.top_pipe = pipe_s.get_rect(midbottom=(x, height - 150)) # Adjust gap if needed
        self.bottom_pipe = pipe_s.get_rect(midtop=(x, height + 150)) # Adjust gap if needed
        self.scored = False
    
    def moveP(self):
        self.top_pipe.centerx -= 5
        self.bottom_pipe.centerx -= 5

    def drawP(self, screen):
        flipped_pipe = pygame.transform.flip(pipe_s, False, True)

        screen.blit(flipped_pipe, self.top_pipe)
        screen.blit(pipe_s, self.bottom_pipe)

def create_pipes():
    height = random.choice(pipe_height_options)
    return Pipe(SCREEN_WIDTH,height)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.moveP()
    return [pipe for pipe in pipes if pipe.top_pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        pipe.drawP(screen)

def main():
    Score = 0
    pipe_list = []
    birds = [Bird(50,SCREEN_HEIGHT//2)]

    font = pygame.font.SysFont("comicsansms", 40)

    running = True
    while running:
        clock.tick(60)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(birds) >0:
                        birds[0].jump()
            if event.type == SPAWNPIPE:
                pipe_list.append(create_pipes())

        background()
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        for bird_instance in birds:
            bird_instance.update()

            if bird_instance.rect.top <= 0 or bird_instance.rect.bottom >= SCREEN_HEIGHT - 100:
                birds.remove(bird_instance)
                pygame.QUIT()
                continue
            for pipe_instance in pipe_list:
                if bird_instance.rect.colliderect(pipe_instance.top_pipe) or bird_instance.rect.colliderect(pipe_instance.bottom_pipe):
                    birds.remove(bird_instance)
                    pygame.QUIT()
                    break

                if not pipe_instance.scored and bird_instance.rect.right > pipe_instance.bottom_pipe.left:
                    Score += 1
                    print("Score",Score)
                    print("Pipe Height", pipe_instance.top_pipe.top)
                    pipe_instance.scored = True
                            
            bird_instance.draw()

            score_text_surface = font.render(f"Score: {Score}", True, (255, 255, 255))


            score_text_rect = score_text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))

            screen.blit(score_text_surface, score_text_rect)
        pygame.display.update()




main()