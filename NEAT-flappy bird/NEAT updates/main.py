import pygame
import sys
import random
import neat
import os

pygame.init()

SCREEN_WIDTH = 288*2
SCREEN_HEIGHT = 1000


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("NEAT-Flappy Bird")

clock = pygame.time.Clock()


bg_raw = pygame.image.load("Assets/background-day.png").convert()
bg = pygame.transform.scale(bg_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
floor_raw = pygame.image.load("Assets/base.png").convert()
floor = pygame.transform.scale(floor_raw,(SCREEN_WIDTH, 100))
floor_x = 0

pipe_raw = pygame.image.load("Assets/pipe-green.png").convert()
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
        self.surface = pygame.transform.scale(pygame.image.load("Assets/bird.png").convert_alpha(), (75, 55))
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
        self.top_pipe = pipe_s.get_rect(midbottom=(x, height - 110)) # Adjust gap if needed
        self.bottom_pipe = pipe_s.get_rect(midtop=(x, height + 110)) # Adjust gap if needed
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

def stats(birds, generation):
    font = pygame.font.SysFont("comicsansms", 30)
    text1 = font.render(f'Birds Alive: {len(birds)}', True, (255, 255, 255))
    text2 = font.render(f'Generation: {generation}', True, (255, 255, 255))

    screen.blit(text1, (10, 800))
    screen.blit(text2, (10, 840))

def eval_genomes(genomes,config):
    #background()
    #Score = 0
    #global generation
    #generation += 1
    pipe_list = [create_pipes()]
    birds = []
    ge = []
    nets = []

    font = pygame.font.SysFont("comicsansms", 40)

    for _,genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(50, SCREEN_HEIGHT//2))
        ge.append(genome)
        genome.fitness = 0

    running = True
    while running and birds:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #running = False
                sys.exit()
            if event.type == SPAWNPIPE:
                pipe_list.append(create_pipes())

        next_pipe = None
        if pipe_list:
            if len(pipe_list) > 1 and birds[0].rect.left > pipe_list[0].top_pipe.right:
                next_pipe = pipe_list[1]
            else:
                next_pipe = pipe_list[0]

        for i in range(len(birds) -1, -1, -1):
            bird_instance = birds[i]

            if next_pipe:
                output = nets[i].activate((
                    bird_instance.rect.y,
                    abs(bird_instance.rect.y - next_pipe.top_pipe.bottom),
                    abs(bird_instance.rect.y - next_pipe.bottom_pipe.top) 
                ))
                if output[0] > 0.5:
                    bird_instance.jump()
            
            bird_instance.update()
            ge[i].fitness += 0.1

            is_dead = False
            for pipe_instance in pipe_list:
                if bird_instance.rect.colliderect(pipe_instance.top_pipe) or bird_instance.rect.colliderect(pipe_instance.bottom_pipe):
                    is_dead = True
                    break
            
            if bird_instance.rect.top <= 0 or bird_instance.rect.bottom >= SCREEN_HEIGHT - 100:
                is_dead = True
            
            # Remove dead birds, nets, and genomes
            if is_dead:
                nets.pop(i)
                ge.pop(i)
                birds.pop(i)
                continue

            for pipe_instance in pipe_list:
                if not pipe_instance.scored and bird_instance.rect.right > pipe_instance.bottom_pipe.left:
                    bird_instance.score += 1
                    ge[i].fitness += 5
                    pipe_instance.scored = True
#if i == 0:
#                      print(f"Score: {bird_instance.score}")

            bird_instance.draw()
        
        pipe_list = move_pipes(pipe_list)
        background()
        
        draw_pipes(pipe_list)
        stats(birds, net)
        for bird_instance in birds:
            bird_instance.draw()
        if birds:
            best_bird_score = max(bird.score for bird in birds)
            score_text_surface = font.render(f"Score: {best_bird_score}", True, (255, 255, 255))
            score_text_rect = score_text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(score_text_surface, score_text_rect)
        
        pygame.display.update()

    #score_text_surface = font.render(f"Score: {Score}", True, (255, 255, 255))
    #score_text_rect = score_text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    #screen.blit(score_text_surface, score_text_rect)





def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)
    
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.run(eval_genomes, 50)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)