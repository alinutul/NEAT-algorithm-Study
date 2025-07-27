def eval_genomes(genomes, config):
    nets = []
    ge = []
    birds = []
    
    # Start with one pipe on screen to give the birds something to look at
    pipes = [create_pipes()]
    
    # Set up the font for displaying the score
    font = pygame.font.SysFont("comicsansms", 40)
    
    # Create the population of birds, nets, and genomes
    for _, genome in genomes:
        net = neat.nn.FeedforwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(50, SCREEN_HEIGHT // 2))
        ge.append(genome)
        genome.fitness = 0

    running = True
    while running and birds: # Loop as long as there are birds alive
        clock.tick(60)

        # --- 1. Handle Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == SPAWNPIPE:
                pipes.append(create_pipes())

        # Determine which pipe is the 'next' pipe for the AI
        next_pipe = None
        if pipes:
            # Find the first pipe that hasn't passed the bird's x position
            next_pipe = pipes[0]
            if len(pipes) > 1 and birds[0].rect.right > pipes[0].top_pipe.left:
                next_pipe = pipes[1]

        # --- 2. Update all objects and check for collisions/scoring ---
        # Iterate backwards to safely remove dead birds
        for i in range(len(birds) - 1, -1, -1):
            bird_instance = birds[i]
            
            # AI Decision Making
            if next_pipe:
                output = nets[i].activate((
                    bird_instance.rect.y,
                    abs(bird_instance.rect.y - next_pipe.top_pipe.bottom),
                    abs(bird_instance.rect.y - next_pipe.bottom_pipe.top)
                ))
                if output[0] > 0.5:
                    bird_instance.jump()

            # Physics Update
            bird_instance.update()
            ge[i].fitness += 0.1 # Reward for staying alive
            
            # Collision Check & Fitness Update
            is_dead = False
            for pipe_instance in pipes:
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
            
            # Scoring for live birds
            for pipe_instance in pipes:
                if not pipe_instance.scored and bird_instance.rect.right > pipe_instance.bottom_pipe.left:
                    bird_instance.score += 1
                    ge[i].fitness += 5
                    pipe_instance.scored = True
                    # Print only for the best bird to avoid spam
                    if i == 0:
                        print(f"Score: {bird_instance.score}")
            
        # Move pipes after all birds have interacted with them
        pipes = move_pipes(pipes)

        # --- 3. Draw Everything on the screen in the correct order ---
        background()
        draw_pipes(pipes)
        
        # Draw all remaining live birds
        for bird_instance in birds:
            bird_instance.draw()

        # Display the score of the best bird
        if birds:
            best_bird_score = max(bird.score for bird in birds)
            score_text_surface = font.render(f"Score: {best_bird_score}", True, (255, 255, 255))
            score_text_rect = score_text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(score_text_surface, score_text_rect)
        
        # --- 4. Update the Display ---
        pygame.display.update()