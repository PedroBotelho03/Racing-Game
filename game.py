import random
import pygame
from airship import Airship
from power_ups import PowerUp
from gameover import GameOver
from highscore import load_high_score, save_high_score
from scoreboard import load_scores, save_scores


# Define the colors
GREY = (197, 197, 197)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 204)
VIOLET = (174, 99, 154)
GRENNY = (154, 232, 79)
LIGHTSTEELBLUE = (176, 196, 222)
transparent_color = (197, 197, 197, 0.1)


# Code for the airship racing game single-player mode
def SinglePlayer():

    """
        Run the single-player mode of the airship racing game.

        The game consists in controlling a player airship and avoiding collisions with incoming airships.

        Power-ups can be collected to gain advantages or disadvantages, such as speed boosts, slowing down, invincibility, and confusion.

        Game Controls:

        - Left Arrow: Move the player airship left
        - Right Arrow: Move the player airship right
        - Up Arrow: Move the player airship forward
        - Down Arrow: Move the player airship down

        Power-ups:

        - Slow Down (Purple): Reduces the speed of the player and the incoming airships.
        - Speed Up (Blue): Increases the speed of the player and the incoming airships.
        - Invincibility (Green): Provides temporary invincibility, preventing collisions with incoming airships.
        - Confusion (Purple): Inverts the control directions temporarily.

        Game Features:

        - Level progression every 50 points, resetting the game and increasing difficulty.
        - Pause button in the top-left corner to pause the game.
        - Countdown at the start of the game before "GO!" is displayed.
        - Score, high score, and timers for active power-ups displayed on the screen.
        - Sound effects for crashes, countdown, and in-game music.

        """

    from interface import Interface
    pygame.init()

    # Load the high score and set it
    global high_score
    high_score = load_high_score()
    scoreboard = load_scores()

    # Screen definition
    size = (1300, 600)
    screen = pygame.display.set_mode(size)
    
    # Set the title of the game screen, and the icon
    pygame.display.set_caption("Retro Space Jam")
    icon_game = pygame.image.load("Images/icon_game.png")
    pygame.display.set_icon(icon_game)
    
    # Some fonts to use
    arcade_font = pygame.font.Font("Fonts/arcade_font.ttf", 100)
    arcade_font1 = pygame.font.Font("Fonts/arcade_font.ttf", 20)
    arcade_font2 = pygame.font.Font("Fonts/arcade_font.ttf", 13)

    # Background
    background = pygame.image.load("Images/background_single_player.png")
    background = pygame.transform.scale(background, [1300, 600])

    # Buttons
    paused_display = pygame.image.load("Images/pause_menu.png")
    paused_display = pygame.transform.scale(paused_display, [700, 400])

    quit_button = pygame.image.load("Images/quit_game_pause.png")
    quit_button = pygame.transform.scale(quit_button, [265, 64])

    resume_active = pygame.image.load("Images/resume_pause.png")
    resume_active = pygame.transform.scale(resume_active, [265, 64])

    restart_active = pygame.image.load("Images/restart_pause.png")
    restart_active = pygame.transform.scale(restart_active, [265, 64])

    # Draw the countdown on the screen with a custom font and larger size
    screen_image = pygame.image.load("Images/background_coutdown.jpg").convert()
    screen_image = pygame.transform.scale(screen_image, [1300, 600])
    
    
    # All the airships that appear on the screen
    playerairship = Airship(RED, 65, 80, image="Images/ship_player1.png")
    playerairship.rect.x = 250
    playerairship.rect.y = 400

    airship1 = Airship(BLUE, 75, 80, 1, image="Images/ship1.png")
    airship1.rect.x = 200
    airship1.rect.y = -150

    airship2 = Airship(PURPLE, 75, 80, 2, image="Images/ship2.png")
    airship2.rect.x = 300
    airship2.rect.y = -200

    airship3 = Airship(ORANGE, 75, 80, 2, image="Images/ship3.png")
    airship3.rect.x = 400
    airship3.rect.y = -400

    airship4 = Airship(YELLOW, 75, 80, 2, image="Images/ship4.png")
    airship4.rect.x = 500
    airship4.rect.y = -380
    
    # Initialize a dictionary to map power-up type to the corresponding PowerUp instance
    power_up_instances = {
        'SLOW_DOWN': PowerUp(WHITE, 35, 35, image="Images/slow_down.png"),
        'INVINCIBILITY': PowerUp(WHITE, 35, 35, image="Images/invincibility.png"),
        'SPEED_UP': PowerUp(WHITE, 35, 35, image="Images/speed_up.png"),
        'CONFUSION': PowerUp(WHITE, 35, 35, image="Images/invert_controls.png"),
    }
    
    # Reset positions for all power-ups
    for power_up_instance in power_up_instances.values():
        power_up_instance.reset_position("single")

    # Sprite group for power-ups
    power_up_list = pygame.sprite.Group(power_up_instances.values())

    # The airships that will be moving down
    incoming_airships_list = pygame.sprite.Group(airship1, airship2, airship3, airship4)

    # Everything that is moving on the screen
    all_sprites_list = pygame.sprite.Group(playerairship, airship1, airship2, airship3, airship4, power_up_list)

    # Game variables
    carryOn = True # Game starts running
    paused = False # Game starts unpaused
    playerairship_speed = 5 # Speed of the player airship
    level = 1  # Initialize the level variable

    # Speed of the game
    clock = pygame.time.Clock()

    # Initialize Score
    score = 0

    # Time variables
    start_time = 0

    # Power-up variables
    slowing_down_active = False
    slowing_down_duration = 600
    slowing_down_timer = 0
    invincibility_active = False
    invincibility_duration = 600
    invincibility_timer = 0
    speeding_up_active = False
    speeding_up_duration = 600
    speeding_up_timer = 0
    confusion_active = False
    confusion_duration = 600
    confusion_timer = 0

    # Countdown variables (before the game starts)
    countdown_duration = 4  # 4 seconds countdown because go! also counts as 1 second
    countdown_timer = countdown_duration * 60  # Convert seconds to frames

    #Sound Countdown
    pygame.mixer.music.load('Sounds/countdown.wav')
    pygame.mixer.music.play(0)
    pygame.mixer.music.set_volume(0.5)

    # Countdown loop at the start of the game
    # Countdown stops if the user quits the game
    while countdown_timer > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False


        screen.blit(screen_image, [0, 0])
        # Draw the countdown on the screen with a custom font and larger size
        if countdown_timer > 60:  # Display the countdown numbers
            countdown_text = arcade_font.render(str(countdown_timer // 60), True, WHITE)
        else:  # Display "GO!" after 1
            countdown_text = arcade_font.render("GO!", True, WHITE)
            # Record the start time when "GO!" is displayed
            start_time = pygame.time.get_ticks()

        text_rect = countdown_text.get_rect(center=(size[0] // 2, size[1] // 2)) # Center the text on the screen
        screen.blit(countdown_text, text_rect) # Draw the text on the screen

        pygame.display.flip()
        clock.tick(60)
        # Decrease the countdown timer by 1 frame so it will eventually reach 0 and the game will start
        countdown_timer -= 1

    # Sound game
    pygame.mixer.music.load('Sounds/music_game.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    # Inside the main loop
    while carryOn:
        for event in pygame.event.get():
            # Check if the user wants to quit the game
            if event.type == pygame.QUIT:
                carryOn = False
            # Check if the user wants to pause the game
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                # Check if the mouse is clicking on the pause button
                if 0 <= mouse[0] <= 100 and 0 <= mouse[1] <= 100:
                    paused = not paused  # Toggle the pause state
                    pygame.time.delay(100)
                    if paused:
                        while paused:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    carryOn = False
                                    paused = False
                                mouse = pygame.mouse.get_pos()  # Update the mouse position within the loop
                                # Check if the user interacts with buttons
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if 520 <= mouse[0] <= 785:
                                        if 236 <= mouse[1] <= 300:
                                            paused = False
                                            pygame.time.delay(300)
                                        elif 313 <= mouse[1] <= 377:
                                            pygame.mixer.music.stop()
                                            carryOn = False
                                            SinglePlayer()
                                        elif 390 <= mouse[1] <= 454:
                                            pygame.mixer.music.stop()
                                            carryOn = False
                                            Interface()


                                # Draw the pause display
                                screen.blit(paused_display, (300, 100))

                                if 520 <= mouse[0] <= 785 and 236 <= mouse[1] <= 300:
                                    pygame.draw.rect(screen, GREY, [520, 236, 265, 64]) # (x, y, width, height)
                                    screen.blit(resume_active, (520, 236))
                                else:
                                    pygame.draw.rect(screen, WHITE, [520, 236, 265, 64])
                                    screen.blit(resume_active, (520, 236))
                                    
                                if 520 <= mouse[0] <= 785 and 313 <= mouse[1] <= 377:
                                    pygame.draw.rect(screen, GREY, [520, 313, 265, 64])
                                    screen.blit(restart_active, (520, 313))
                                else:
                                    pygame.draw.rect(screen, WHITE, [520, 313, 265, 64])
                                    screen.blit(restart_active, (520, 313))
                                    
                                if 520 <= mouse[0] <= 785 and 390 <= mouse[1] <= 454:
                                    pygame.draw.rect(screen, GREY, [520, 390, 265, 64])
                                    screen.blit(quit_button, (520, 390))
                                else:
                                    pygame.draw.rect(screen, WHITE, [520, 390, 265, 64])
                                    screen.blit(quit_button, (520, 390))

                                pygame.display.flip()
                            pygame.display.flip()

        # Power-up probability system
        CONFUSION = power_up_instances["CONFUSION"]
        SPEED_UP = power_up_instances["SPEED_UP"]
        SLOW_DOWN = power_up_instances["SLOW_DOWN"]
        INVINCIBILITY = power_up_instances["INVINCIBILITY"]
        
        PROBABILITIES = [
            CONFUSION, CONFUSION, CONFUSION, CONFUSION, CONFUSION, CONFUSION, CONFUSION,
            SPEED_UP, SPEED_UP, 
            SPEED_UP, SLOW_DOWN, SLOW_DOWN, SLOW_DOWN,
            INVINCIBILITY
        ]
        
        if random.random() < 0.05:
            random_power_up_instance = random.choice(PROBABILITIES)
            random_power_up_instance.update(playerairship_speed, "single")
            
        
        # Movement of the player airship
        pressed_keys = pygame.key.get_pressed()
        if not confusion_active:
            if pressed_keys[pygame.K_LEFT] and playerairship.rect.x > 130:
                playerairship.moveLeft(5)
            if pressed_keys[pygame.K_RIGHT] and playerairship.rect.x < 545:
                playerairship.moveRight(5)
            if pressed_keys[pygame.K_UP]:
                playerairship.moveForward(5)
            if pressed_keys[pygame.K_DOWN]:
                playerairship.moveDown(5)
        else:
            if pressed_keys[pygame.K_LEFT] and playerairship.rect.x < 545:
                playerairship.moveRight(5)
            if pressed_keys[pygame.K_RIGHT] and playerairship.rect.x > 130:
                playerairship.moveLeft(5)
            if pressed_keys[pygame.K_UP]:
                playerairship.moveDown(5)
            if pressed_keys[pygame.K_DOWN]:
                playerairship.moveForward(5)

        # This updates the score based on the time elapsed since the start of the game
        elapsed_time = (pygame.time.get_ticks() - start_time) // 500  # 500ms = 0.5s
        score = elapsed_time
        
        # Update the high score if the current score is higher
        if score > high_score:
            high_score = score
            # Save the new high score to the file
            save_high_score(high_score)
            
        for power_up_instance in power_up_list:
            # Check if the player airship collides with any of the power-ups
            if pygame.sprite.collide_mask(playerairship, power_up_instance) is not None:
                
                # If they collide, the power-up will reset its position
                power_up_instance.reset_position("single")
                # If it's the invincibility
                if power_up_instance == power_up_instances['INVINCIBILITY']:
                    invincibility_active = True
                    invincibility_timer = 0
                    playerairship.change_color(GREEN)
                # If it's the slow down
                elif power_up_instance == power_up_instances['SLOW_DOWN']:
                    slowing_down_active = True
                    slowing_down_timer = 0
                    playerairship.change_color(RED)
                    # Disable speed-up if slowing down is active
                    speeding_up_active = False
                    speeding_up_timer = 0
                    playerairship.change_color(BLUE)
                elif power_up_instance == power_up_instances['SPEED_UP']:
                    speeding_up_active = True
                    speeding_up_timer = 0
                    playerairship.change_color(BLUE)
                    # Disable slow-down if speeding up is active
                    slowing_down_active = False
                    slowing_down_timer = 0
                    playerairship.change_color(RED)
                elif power_up_instance == power_up_instances['CONFUSION']:
                    confusion_active = True
                    confusion_timer = 0
                    playerairship.change_color(PURPLE)

        # This updates the position of the airships and the power-ups
        all_sprites_list.update(playerairship_speed, "single")

        # All the background of the game INCLUDING ROAD
        screen.blit(background, [0,0])

        # Drawing three dashed lines on the road
        line_positions = [261, 372, 483]

        for x in line_positions:
            for y in range(20, 630, 100):
                pygame.draw.line(screen, WHITE, (x, y), (x, y + 55), 5)
            
        # Draw the score on the screen
        score_text = arcade_font1.render("Score: {}".format(score), True, WHITE)
        high_score_text = arcade_font1.render("High Score: {}".format(high_score), True, WHITE)
        screen.blit(score_text, (1050, 50))
        screen.blit(high_score_text, (930, 20))

        # Logic for the incoming airships to never stop appearing, including changes in the speed of the airships
        # Depending on the power-ups that are active
        for airship in incoming_airships_list:
            if not slowing_down_active and not speeding_up_active:
                airship.moveDown(playerairship_speed)
            else:
                if slowing_down_active:
                    airship.moveDown(playerairship_speed // 2.5)
                if speeding_up_active:
                    airship.moveDown(playerairship_speed * 2.5)
            
            # If the airship goes off the screen, it will be reset to a random position above the screen
            if airship.rect.y >= 600:
                airship.rect.y = random.randint(-500, -100)
                airship.change_speed(random.randint(1, 7))
                
                # Randomize the x-coordinate within the lane boundaries
                if airship == airship1:
                    airship.rect.x = random.randint(130, 225)
                elif airship == airship2:
                    airship.rect.x = random.randint(230, 325)
                elif airship == airship3:
                    airship.rect.x = random.randint(330, 425)
                elif airship == airship4:
                    airship.rect.x = random.randint(430, 525)

        # Check if the player airship collides with any of the incoming airships
        for airship in incoming_airships_list:
            if not invincibility_active and pygame.sprite.collide_mask(playerairship, airship) is not None:
                pygame.mixer.Sound("Sounds/crash.wav").play()
                pygame.time.delay(500)
                # Add the current score to the scoreboard
                scoreboard.append(score)
                # Sort the scoreboard in descending order
                scoreboard.sort(reverse = True)
                # Keep only the top 10 scores
                scoreboard = scoreboard[:10]
                # Save the updated scoreboard to the file
                save_scores(scoreboard)
                GameOver(score, None, None)
                pygame.mixer.music.stop()


        # Display timers for power-ups while they are active
        if invincibility_active:
            invincibility_timer_text = arcade_font2.render(f"Invincibility Timer: {max(0, (invincibility_duration - invincibility_timer) // 60)}s", True, WHITE)
            screen.blit(invincibility_timer_text, (950, 200))
            invincibility_timer += 1
            if invincibility_timer >= invincibility_duration:
                invincibility_active = False
                invincibility_timer = 0
                playerairship.restore_color()
                
        if not speeding_up_active:
            if slowing_down_active:
                slowing_down_timer_text = arcade_font2.render(f"Speed Down Timer: {max(0, (slowing_down_duration - slowing_down_timer) // 60)}s", True, WHITE)
                screen.blit(slowing_down_timer_text, (950, 230))
                slowing_down_timer += 1
                if slowing_down_timer >= slowing_down_duration:
                    slowing_down_active = False
                    slowing_down_timer = 0
                    playerairship.restore_color()
                
        if not slowing_down_active:        
            if speeding_up_active:
                speedup_timer_text = arcade_font2.render(f"Speed Up Timer: {max(0, (speeding_up_duration - speeding_up_timer) // 60)}s", True, WHITE)
                screen.blit(speedup_timer_text, (950, 260))
                speeding_up_timer += 1
                if speeding_up_timer >= speeding_up_duration:
                    speeding_up_active = False
                    speeding_up_timer = 0
                    playerairship.restore_color()

        if confusion_active:
            confusion_timer_text = arcade_font2.render(f"Confusion Timer: {max(0, (confusion_duration - confusion_timer) // 60)}s", True, WHITE)
            screen.blit(confusion_timer_text, (950, 290))
            confusion_timer += 1
            if confusion_timer >= confusion_duration:
                confusion_active = False
                confusion_timer = 0
                playerairship.restore_color()
                
                
        # Level ups, every 50 points reseting the game basically
        if score > 0 and score % 50 == 0:
            level += 1
            airship1.rect.y = random.randint(-1000, -300)
            airship2.rect.y = random.randint(-1000, -300)
            airship3.rect.y = random.randint(-1000, -300)
            airship4.rect.y = random.randint(-1000, -300)
            playerairship_speed = 5
            confusion_active = False
            speeding_up_active = False
            slowing_down_active = False
            invincibility_active = False
            for power_up_instance in power_up_instances.values():
                power_up_instance.reset_position("single")
            largetext = pygame.font.Font('Fonts/arcade_font.ttf', 80)
            textsurf = largetext.render('LEVEL ' + str(level), True, WHITE)
            textrect = textsurf.get_rect(center=(size[0] // 2, size[1] // 2))
            screen.blit(textsurf, textrect)
            pygame.display.update()
            pygame.time.delay(1000)
            playerairship.restore_color()
            

        # Creating a Pause Button
        mouse = pygame.mouse.get_pos()
        if 0 <= mouse[0] <= 50 and 0 <= mouse[1] <= 50:
            pygame.draw.rect(screen, GREY, [0, 0, 50, 50])
        else:
            pygame.draw.rect(screen, WHITE, [0, 0, 50, 50])
        pause_button = pygame.image.load("Images/pause_button.png")
        pause_button = pygame.transform.scale(pause_button, [50, 50])
        screen.blit(pause_button, (0, 0))

        all_sprites_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    
    
def Multiplayer():

    """
      Multiplayer game mode function using Pygame.

      The function initializes the Pygame window and sets up the multiplayer game mode.
      It handles player controls, power-ups, collisions, and game state transitions.

    Game Controls:
    - Left Arrow and A: Move the player airship left
    - Right Arrow and D: Move the player airship right
    - Up Arrow and W: Move the player airship forward
    - Down Arrow and S: Move the player airship down

    Power-ups:
    - Slow Down (Purple): Reduces the speed of the player airship and the incoming airships.
    - Speed Up (Blue): Increases the speed of the player airship and the incoming airships.
    - Invincibility (Green): Provides temporary invincibility, preventing collisions with incoming airships.
    - Confusion (Purple): Inverts the control directions temporarily.

      """

    from interface import Interface, Settings
    pygame.init()
    
    # Screen definition
    size = (1300, 600)
    screen = pygame.display.set_mode(size)
    
    # Set the title of the game screen, and the icon
    pygame.display.set_caption("Retro Space Jam")
    pygame.display.set_icon(pygame.image.load("Images/icon_game.png"))

    # Background
    background = pygame.image.load("Images/background_multiplayer.png")
    background = pygame.transform.scale(background, [1300, 600])

    # Some fonts to use
    arcade_font = pygame.font.Font("Fonts/arcade_font.ttf", 50)
    arcade_font2 = pygame.font.Font("Fonts/arcade_font.ttf", 13)

    # Buttons
    paused_display = pygame.image.load("Images/pause_menu.png")
    paused_display = pygame.transform.scale(paused_display, [700, 350])

    quit_button = pygame.image.load("Images/quit_game_pause.png")
    quit_button = pygame.transform.scale(quit_button, [255, 60])

    resume_active = pygame.image.load("Images/resume_pause.png")
    resume_active = pygame.transform.scale(resume_active, [255, 60])

    restart_active = pygame.image.load("Images/restart_pause.png")
    restart_active = pygame.transform.scale(restart_active, [255, 60])

    # Draw the countdown on the screen with a custom font and larger size
    screen_image = pygame.image.load("Images/background_coutdown.jpg").convert()
    screen_image = pygame.transform.scale(screen_image, [1300, 600])

    # All the airships that appear on the screen
    playerairship = Airship(RED, 70, 80, image="Images/ship_player1.png")
    playerairship.rect.x = 200
    playerairship.rect.y = 300

    playerairship2 = Airship(RED, 70, 80, image="Images/ship_player2.png")
    playerairship2.rect.x = 800
    playerairship2.rect.y = 300

    airship1 = Airship(BLUE, 75, 80, 1, image="Images/ship1.png")
    airship1.rect.x = 190
    airship1.rect.y = -100

    airship2 = Airship(PURPLE, 75, 80, 2, image="Images/ship2.png")
    airship2.rect.x = 290
    airship2.rect.y = -200

    airship3 = Airship(ORANGE, 75, 80, 2, image="Images/ship3.png")
    airship3.rect.x = 390
    airship3.rect.y = -500

    airship4 = Airship(YELLOW, 75, 80, 2, image="Images/ship4.png")
    airship4.rect.x = 490
    airship4.rect.y = -750

    # Initialize a dictionary to map power-up type to the corresponding PowerUp instance
    power_up_instances = {
        'SLOW_DOWN': PowerUp(WHITE, 35, 35, image="Images/slow_down.png"),
        'INVINCIBILITY': PowerUp(WHITE, 35, 35, image="Images/invincibility.png"),
        'SPEED_UP': PowerUp(WHITE, 35, 35, image="Images/speed_up.png"),
        'CONFUSION': PowerUp(WHITE, 35, 35, image="Images/invert_controls.png"),
    }
    
    # Reset positions for all power-ups on both roads
    for power_up_instance in power_up_instances.values():
        power_up_instance.reset_position("multi")
            
    power_up_list = pygame.sprite.Group(power_up_instances.values())
    
    incoming_airships_list = pygame.sprite.Group()
    incoming_airships_list.add(airship1, airship2, airship3, airship4)

    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(playerairship, playerairship2, airship1, airship2, airship3, airship4, power_up_list)

    # Game Variables
    carryOn = True
    playerairship_speed = 2
    playerairship2_speed = 2
    paused = False
    
    # Speed of the game
    clock = pygame.time.Clock()

    # Power-up variables
    slowing_down_active_playerairship2 = False
    slowing_down_active_playerairship = False
    slowing_down_timer_playerairship2 = 0
    slowing_down_timer_playerairship = 0
    slowing_down_duration = 600
    
    invincibility_active_playerairship2 = False
    invincibility_active_playerairship = False 
    invincibility_timer_playerairship2 = 0
    invincibility_timer_playerairship = 0
    invincibility_duration = 600
    
    speeding_up_active_playerairship2 = False
    speeding_up_active_playerairship = False
    speeding_up_timer_playerairship2 = 0
    speeding_up_timer_playerairship = 0
    speeding_duration = 600

    confusion_active_playerairship2 = False
    confusion_active_playerairship = False
    confusion_timer_playerairship2 = 0
    confusion_timer_playerairship = 0
    confusion_duration = 600

    # Countdown variables (before the game starts)
    countdown_duration = 4  # 4 seconds countdown because go! also counts as 1 second
    countdown_timer = countdown_duration * 60  # Convert seconds to frames

    #Sound Countdown
    pygame.mixer.music.load('Sounds/countdown.wav')
    pygame.mixer.music.play(0)
    pygame.mixer.music.set_volume(0.5)

    # Countdown loop at the start of the game
    # Countdown stops if the user quits the game
    while countdown_timer > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False

        screen.blit(screen_image, [0, 0])
        # Draw the countdown on the screen with a custom font and larger size
        if countdown_timer > 60:  # Display the countdown numbers
            countdown_text = arcade_font.render(str(countdown_timer // 60), True, WHITE)
        else:  # Display "GO!" after 1
            countdown_text = arcade_font.render("GO!", True, WHITE)

        text_rect = countdown_text.get_rect(center=(size[0] // 2, size[1] // 2))  # Center the text on the screen
        screen.blit(countdown_text, text_rect)  # Draw the text on the screen

        pygame.display.flip()
        clock.tick(60)
        # Decrease the countdown timer by 1 frame so it will eventually reach 0 and the game will start
        countdown_timer -= 1

    # Sound game
    pygame.mixer.music.load('Sounds/music_game.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    # Game main loop
    while carryOn:
        # Check if the user wants to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
            # Check if the user wants to pause the game
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if 0 <= mouse[0] <= 100 and 0 <= mouse[1] <= 100:
                    paused = not paused  # Toggle the pause state
                    pygame.time.delay(100)
                    if paused:
                        while paused:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    carryOn = False
                                    paused = False
                                mouse = pygame.mouse.get_pos()  # Update the mouse position within the loop
                                pygame.mixer.music.stop()
                                # Check if the mouse is hovering over the resume button
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    # Check if the user wants to resume the game
                                    if 423 <= mouse[0] <= 678 and 270 <= mouse[1] <= 333:
                                        paused = False
                                        pygame.time.delay(300)
                                        pygame.mixer.music.play()# Small delay
                                    # Check if the user wants to restart the game
                                    elif 423 <= mouse[0] <= 678 and 340 <= mouse[1] <= 300:
                                        carryOn = False
                                        SinglePlayer()
                                    # Check if the user wants to go to the main menu
                                    elif 423 <= mouse[0] <= 678 and 410 <= mouse[1] <= 470:
                                        carryOn = False
                                        Interface()

                                screen.blit(paused_display, (200, 150))
                                if 423 <= mouse[0] <= 678 and 270 <= mouse[1] <= 330:
                                    pygame.draw.rect(screen, GREY, [423, 270, 255, 60])
                                else:
                                    pygame.draw.rect(screen, WHITE, [423, 270, 255, 60])
                                screen.blit(resume_active, (423, 270))

                                if 423 <= mouse[0] <= 678 and 340 <= mouse[1] <= 400:
                                    pygame.draw.rect(screen, GREY, [423, 340, 255, 60])
                                else:
                                    pygame.draw.rect(screen, WHITE, [423, 340, 255, 60])
                                screen.blit(restart_active, (423, 340))

                                if 423 <= mouse[0] <= 678 and 410 <= mouse[1] <= 470:
                                    pygame.draw.rect(screen, GREY, [423, 410, 255, 60])
                                else:
                                    pygame.draw.rect(screen, WHITE, [423, 410, 255, 60])
                                screen.blit(quit_button, (423, 410))


                                pygame.display.flip()

                        pygame.display.flip()

        # Porbability System of the Multiplayer Power-Ups
        CONFUSION = power_up_instances["CONFUSION"]
        SPEED_UP = power_up_instances["SPEED_UP"]
        SLOW_DOWN = power_up_instances["SLOW_DOWN"]
        INVINCIBILITY = power_up_instances["INVINCIBILITY"]
        
        # Probability of the power-ups to appear
        PROBABILITIES = [
            CONFUSION, CONFUSION, CONFUSION, CONFUSION, CONFUSION, CONFUSION, CONFUSION,
            SPEED_UP, SPEED_UP, 
            SPEED_UP, SLOW_DOWN, SLOW_DOWN, SLOW_DOWN,
            INVINCIBILITY
        ]
        
        # Randomly choose a power-up to spawn
        if random.random() < 0.1:
            random_power_up_instance = random.choice(PROBABILITIES)
            random_power_up_instance.update(playerairship_speed, "single") 

            
        # Get the state of all keys for player 1
        keys_player1 = pygame.key.get_pressed()

        # Movement of player 1
        if not confusion_active_playerairship:
            # Normal controls when confusion power-up is not active
            if keys_player1[pygame.K_a] and playerairship.rect.x > 130:
                playerairship.moveLeft(5)
            if keys_player1[pygame.K_d] and playerairship.rect.x < 545:
                playerairship.moveRight(5)
            if keys_player1[pygame.K_w]:
                playerairship.moveForward(5)
            if keys_player1[pygame.K_s]:
                playerairship.moveDown(5)
        else:
            # Controls when confusion power-up is active
            if keys_player1[pygame.K_a] and playerairship.rect.x < 545:
                playerairship.moveRight(5)
            if keys_player1[pygame.K_d] and playerairship.rect.x > 130:
                playerairship.moveLeft(5)
            if keys_player1[pygame.K_w]:
                playerairship.moveDown(5)
            if keys_player1[pygame.K_s]:
                playerairship.moveForward(5)
        all_sprites_list.update(playerairship_speed, "multi")
        
        # Get the state of all keys for player 2
        keys_player2 = pygame.key.get_pressed()

        # Movement of player 2
        if not confusion_active_playerairship2:
            # Normal controls when confusion power-up is not active
            if keys_player2[pygame.K_LEFT] and playerairship2.rect.x > 685:
                playerairship2.moveLeft(5)
            if keys_player2[pygame.K_RIGHT] and playerairship2.rect.x < 1100:
                playerairship2.moveRight(5)
            if keys_player2[pygame.K_UP]:
                playerairship2.moveForward(5)
            if keys_player2[pygame.K_DOWN]:
                playerairship2.moveDown(5)
        else:
            # Controls when confusion power-up is active for player 2
            if keys_player2[pygame.K_LEFT] and playerairship2.rect.x < 1100:
                playerairship2.moveRight(5)
            if keys_player2[pygame.K_RIGHT] and playerairship2.rect.x > 685:
                playerairship2.moveLeft(5)
            # Check if the slowing down power-up is not active
            if keys_player2[pygame.K_UP]:
                playerairship2.moveDown(5)
            if keys_player2[pygame.K_DOWN]:
                playerairship2.moveForward(5)
        all_sprites_list.update(playerairship2_speed, "multi")
        
        
        # Check if the player1 collides with any power-up
        for power_up_instance in power_up_list:
            # Check if the player airship collides with any of the power-ups
            if pygame.sprite.collide_mask(playerairship, power_up_instance) is not None:
                
                # If they collide, the power-up will reset its position
                power_up_instance.reset_position("single")
                # If it's the invincibility
                if power_up_instance == power_up_instances['INVINCIBILITY']:
                    invincibility_active_playerairship = True
                    invincibility_timer_playerairship = 0
                    playerairship.change_color(GREEN)
                # If it's the slow down
                elif power_up_instance == power_up_instances['SLOW_DOWN']:
                    slowing_down_active_playerairship = True
                    slowing_down_timer_playerairship = 0
                    playerairship.change_color(RED)
                    # Disable speed-up if slowing down is active
                    speeding_up_active_playerairship = False
                    speeding_up_timer_playerairship = 0
                    playerairship.change_color(BLUE)
                elif power_up_instance == power_up_instances['SPEED_UP']:
                    speeding_up_active_playerairship2 = True
                    speeding_up_timer_playerairship2 = 0
                    playerairship2.change_color(BLUE)
                    # Disable slow-down if speeding up is active
                    slowing_down_active_playerairship2 = False
                    slowing_down_timer_playerairship2 = 0
                    playerairship2.change_color(RED)
                elif power_up_instance == power_up_instances['CONFUSION']:
                    confusion_active_playerairship2 = True
                    confusion_timer_playerairship2 = 0
                    playerairship2.change_color(PURPLE)

        # Check if the player2 collides with any power-up
        for power_up_instance in power_up_list:
            # Check if the player airship collides with any of the power-ups
            if pygame.sprite.collide_mask(playerairship2, power_up_instance) is not None:
                
                # If they collide, the power-up will reset its position
                power_up_instance.reset_position("multi")
                # If it's the invincibility
                if power_up_instance == power_up_instances['INVINCIBILITY']:
                    invincibility_active_playerairship2 = True
                    invincibility_timer_playerairship2 = 0
                    playerairship2.change_color(GREEN)
                # If it's the slow down
                elif power_up_instance == power_up_instances['SLOW_DOWN']:
                    slowing_down_active_playerairship2 = True
                    slowing_down_timer_playerairship2 = 0
                    playerairship2.change_color(RED)
                    # Disable speed-up if slowing down is active
                    speeding_up_active_playerairship2 = False
                    speeding_up_timer_playerairship2 = 0
                    playerairship2.change_color(BLUE)
                elif power_up_instance == power_up_instances['SPEED_UP']:
                    speeding_up_active_playerairship = True
                    speeding_up_timer_playerairship = 0
                    playerairship.change_color(BLUE)
                    # Disable slow-down if speeding up is active
                    slowing_down_active_playerairship = False
                    slowing_down_timer_playerairship = 0
                    playerairship.change_color(RED)
                elif power_up_instance == power_up_instances['CONFUSION']:
                    confusion_active_playerairship = True
                    confusion_timer_playerairship = 0
                    playerairship.change_color(PURPLE)


        # All the background of the game INCLUDING ROAD (colors only for now)
        screen.blit(background, [0,0])

        # Drawing three dashed lines on the road
        line_positions = [261, 372, 483]

        for x in line_positions:
            for y in range(20, 630, 100):
                pygame.draw.line(screen, WHITE, (x, y), (x, y + 55), 5)

        
        # Drawing three dashed lines on the road
        line_positions2 = [817, 928, 1039]
        
        for x in line_positions2:
            for y in range(20, 630, 100):
                pygame.draw.line(screen, WHITE, (x, y), (x, y + 55), 5)


        # Handling the speeds and the incoming airships to never stop appearing
        for airship in incoming_airships_list:
            # Player 1
            if not slowing_down_active_playerairship and not speeding_up_active_playerairship:
                airship.moveDown(playerairship_speed)
            else:
                if slowing_down_active_playerairship:
                    airship.moveDown(playerairship_speed // 3)
                if speeding_up_active_playerairship:
                    airship.moveDown(playerairship_speed * 3)
            if airship.rect.y >= 600:
                airship.rect.y = random.randint(-250, 0)
                airship.change_speed(random.randint(1, 4))
                if airship == airship1:
                    airship.rect.x = random.randint(140, 200)
                elif airship == airship2:
                    airship.rect.x = random.randint(240, 300)
                elif airship == airship3:
                    airship.rect.x = random.randint(340, 400)
                elif airship == airship4:
                    airship.rect.x = random.randint(440, 500)
                incoming_airships_list.add(airship)
            
            # Player 2
            if not slowing_down_active_playerairship2 and not speeding_up_active_playerairship2:
                airship.moveDown(playerairship2_speed)
            else:
                if slowing_down_active_playerairship2:
                    airship.moveDown(playerairship2_speed // 3)
                if speeding_up_active_playerairship2:
                    airship.moveDown(playerairship2_speed * 3)
            if airship.rect.y >= 600:
                airship.rect.y = random.randint(-250, 0)
                airship.change_speed(random.randint(1, 4))
                if airship == airship1:
                    airship.rect.x = random.randint(685, 750)
                elif airship == airship2:
                    airship.rect.x = random.randint(785, 850)
                elif airship == airship3:
                    airship.rect.x = random.randint(900, 985)
                elif airship == airship4:
                    airship.rect.x = random.randint(1000, 1100)
                incoming_airships_list.add(airship)
                
        for airship in incoming_airships_list:
            #Player 1 collision check
            if (not invincibility_active_playerairship and pygame.sprite.collide_mask(playerairship, airship) is not None):
                pygame.mixer.Sound("Sounds/crash.wav").play()
                pygame.time.delay(500)
                GameOver(None, None, playerairship2)
                pygame.mixer.music.stop()
            #Player 2 collision check
            if (not invincibility_active_playerairship2 and pygame.sprite.collide_mask(playerairship2, airship) is not None):
                pygame.mixer.Sound("Sounds/crash.wav").play()
                pygame.time.delay(500)
                GameOver(None, playerairship, None)
                pygame.mixer.music.stop()

        # Display timers for power-ups while they are active
        if not speeding_up_active_playerairship:
            if slowing_down_active_playerairship:
                slowing_down_timer_text = arcade_font2.render(
                    f"Slowing Down Timer: {max(0, (slowing_down_duration - slowing_down_timer_playerairship) // 60)}s", True, WHITE)
                screen.blit(slowing_down_timer_text, (150, 20))
                slowing_down_timer_playerairship += 1
                if slowing_down_timer_playerairship >= slowing_down_duration:
                    slowing_down_active_playerairship = False
                    slowing_down_timer_playerairship = 0
                    playerairship.restore_color()
                    
        if not speeding_up_active_playerairship2:        
            if slowing_down_active_playerairship2:
                slowing_down_timer_text = arcade_font2.render(
                    f"Slowing Down Timer: {max(0, (slowing_down_duration - slowing_down_timer_playerairship2) // 60)}s", True, WHITE)
                screen.blit(slowing_down_timer_text, (710, 20))
                slowing_down_timer_playerairship2 += 1
                if slowing_down_timer_playerairship2 >= slowing_down_duration:
                    slowing_down_active_playerairship2 = False
                    slowing_down_timer_playerairship2 = 0
                    playerairship2.restore_color()

        if invincibility_active_playerairship:
            invincibility_timer_text = arcade_font2.render(
                f"Invincibility Timer: {max(0, (invincibility_duration - invincibility_timer_playerairship) // 60)}s", True, WHITE)
            screen.blit(invincibility_timer_text, (150, 50))
            invincibility_timer_playerairship += 1
            if invincibility_timer_playerairship >= invincibility_duration:
                invincibility_active_playerairship = False
                invincibility_timer_playerairship = 0
                playerairship.restore_color()
            
        if invincibility_active_playerairship2:
            invincibility_timer_text = arcade_font2.render(
                f"Invincibility Timer: {max(0, (invincibility_duration - invincibility_timer_playerairship2) // 60)}s", True, WHITE)
            screen.blit(invincibility_timer_text, (710, 50))
            invincibility_timer_playerairship2 += 1
            if invincibility_timer_playerairship2 >= invincibility_duration:
                invincibility_active_playerairship2 = False
                invincibility_timer_playerairship2 = 0
                playerairship2.restore_color()

        if slowing_down_active_playerairship:
            if speeding_up_active_playerairship:
                speeding_timer_text = arcade_font2.render(
                    f"Speeding Timer: {max(0, (speeding_duration - speeding_up_timer_playerairship2) // 60)}s", True, WHITE)
                screen.blit(speeding_timer_text, (150, 80))
                speeding_up_timer_playerairship2 += 1
                playerairship2_speed = 3
                if speeding_up_timer_playerairship2 >= speeding_duration:
                    speeding_up_active_playerairship2 = False
                    speeding_up_timer_playerairship2 = 0
                    playerairship2.restore_color()
                    
        if slowing_down_active_playerairship2:     
            if speeding_up_active_playerairship2:
                speeding_timer_text = arcade_font2.render(
                    f"Speeding Timer: {max(0, (speeding_duration - speeding_up_timer_playerairship) // 60)}s", True, WHITE)
                screen.blit(speeding_timer_text, (710, 80))
                speeding_up_timer_playerairship += 1
                playerairship_speed = 3
                if speeding_up_timer_playerairship >= speeding_duration:
                    speeding_up_active_playerairship = False
                    speeding_up_timer_playerairship = 0
                    playerairship.restore_color()
                    
        if confusion_active_playerairship:
            confusion_timer_text = arcade_font2.render(
                f"Confusion Timer: {max(0, (confusion_duration - confusion_timer_playerairship2) // 60)}s", True, WHITE)
            screen.blit(confusion_timer_text, (150, 110))
            confusion_timer_playerairship2 += 1
            if confusion_timer_playerairship2 >= confusion_duration:
                confusion_active_playerairship2 = False
                confusion_timer_playerairship2 = 0
                playerairship2.restore_color()
                        
        if confusion_active_playerairship2:
            confusion_timer_text = arcade_font2.render(
                f"Confusion Timer: {max(0, (confusion_duration - confusion_timer_playerairship) // 60)}s", True, WHITE)
            screen.blit(confusion_timer_text, (710, 110))
            confusion_timer_playerairship += 1
            if confusion_timer_playerairship >= confusion_duration:
                confusion_active_playerairship = False
                confusion_timer_playerairship = 0
                playerairship.restore_color()
            
        # Creating a Pause Button
        mouse = pygame.mouse.get_pos()
        if 0 <= mouse[0] <= 50 and 0 <= mouse[1] <= 50:
            pygame.draw.rect(screen, GREY, [0, 0, 50, 50])
        else:
            pygame.draw.rect(screen, WHITE, [0, 0, 50, 50])
        pause_button = pygame.image.load("Images/pause_button.png")
        pause_button = pygame.transform.scale(pause_button, [50, 50])
        screen.blit(pause_button, (0, 0))

        all_sprites_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        
    pygame.quit()