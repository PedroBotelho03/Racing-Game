""" Interface module for Retro Space Jam.

This module provides several features for creating
and displaying an interactive main menu, with options
such as starting the game, selecting the game mode,
viewing the credits and the instructions of the game,
adjusting settings and play music.

"""
import pygame
from game import SinglePlayer, Multiplayer
from scoreboard import display_scoreboard, load_scores

# Initialize pygame
pygame.init()

# Set the volume
pygame.mixer.music.set_volume(0.1)

# Load the music
pygame.mixer.music.load('Sounds/interface_song.wav')
pygame.mixer.music.play(-1)

"""The function Interface displays the main menu screen, 
with options to start the game, view credits, quit, 
check the instructions of the game (rules), and adjust settings.

"""


def Interface():
    pygame.init()

    # Set the size of the window
    size = (800, 700)
    screen = pygame.display.set_mode(size)

    # Colors to use
    WHITE = (255, 255, 255)
    GREY = (197, 197, 197)

    # Font of the text in the interface
    arcade_font = pygame.font.Font("Fonts/arcade_font.ttf", 20)

    # All the texts in the interface
    welcome_text = arcade_font.render('Welcome, to the Retro Space Jam', True, WHITE)

    button_start = pygame.image.load("Images/game_mode.png")
    button_start = pygame.transform.scale(button_start, [175, 75])

    Scoreboard = pygame.image.load("Images/scoreboard_button.png")
    Scoreboard = pygame.transform.scale(Scoreboard, [175, 75])

    button_credits = pygame.image.load("Images/credits.png")
    button_credits = pygame.transform.scale(button_credits, [175, 75])

    button_quit = pygame.image.load("Images/quit.png")
    button_quit = pygame.transform.scale(button_quit, [150, 50])

    settings = pygame.image.load("Images/settings.png")
    settings = pygame.transform.scale(settings, [175, 75])

    rules = pygame.image.load("Images/instructions.png")
    rules = pygame.transform.scale(rules, [175, 75])

    # Setting the caption of the interface screen
    pygame.display.set_caption("Main Menu")

    # Adding an icon to the interface screen
    pygame.display.set_icon(pygame.image.load("Images/menu_icon.png"))

    # Main loop of the interface screen
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            # If the mouse is clicked in any button, it will do what is writen in that button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= mouse[0] <= 275 and 200 <= mouse[1] <= 275:
                    GameMode()

                if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
                    pygame.quit()

                if 100 <= mouse[0] <= 275 and 500 <= mouse[1] <= 575:
                    Credits()

                if 100 <= mouse[0] <= 275 and 400 <= mouse[1] <= 475:
                    Rules()

                if 100 <= mouse[0] <= 275 and 300 <= mouse[1] <= 375:
                    Settings()

                if 100 <= mouse[0] <= 275 and 600 <= mouse[1] <= 675:
                    display_scoreboard(load_scores())

        # Setting the background color
        screen_image = pygame.image.load("Images/background_interface.jpg").convert()
        screen_image = pygame.transform.scale(screen_image, [800, 700])

        # Setting the texts in the screen
        screen.blit(screen_image, [0, 0])
        screen.blit(welcome_text, (25, 100))

        # Getting the position of the mouse so we know where the player is clicking
        mouse = pygame.mouse.get_pos()

        # The lines below are the buttons of the interface screen
        if 100 <= mouse[0] <= 275 and 200 <= mouse[1] <= 275:
            pygame.draw.rect(screen, GREY, [100, 200, 175, 75])  # [x, y, x1-x2, y1-y2]
            screen.blit(button_start, [100, 200])
        else:
            pygame.draw.rect(screen, WHITE, [100, 200, 175, 75])
            screen.blit(button_start, [100, 200])

        if 100 <= mouse[0] <= 275 and 500 <= mouse[1] <= 575:
            pygame.draw.rect(screen, GREY, [100, 500, 175, 75])
            screen.blit(button_credits, (100, 500))
        else:
            pygame.draw.rect(screen, WHITE, [100, 500, 175, 75])
            screen.blit(button_credits, (100, 500))

        if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
            pygame.draw.rect(screen, GREY, [600, 600, 150, 50])
            screen.blit(button_quit, (600, 600))
        else:
            pygame.draw.rect(screen, WHITE, [600, 600, 150, 50])
            screen.blit(button_quit, (600, 600))

        if 100 <= mouse[0] <= 275 and 400 <= mouse[1] <= 475:
            pygame.draw.rect(screen, GREY, [100, 400, 175, 75])
            screen.blit(rules, (100, 400))
        else:
            pygame.draw.rect(screen, WHITE, [100, 400, 175, 75])
            screen.blit(rules, (100, 400))

        if 100 <= mouse[0] <= 275 and 300 <= mouse[1] <= 375:
            pygame.draw.rect(screen, GREY, [100, 300, 175, 75])
            screen.blit(settings, (100, 300))
        else:
            pygame.draw.rect(screen, WHITE, [100, 300, 175, 75])
            screen.blit(settings, (100, 300))

        if 100 <= mouse[0] <= 275 and 600 <= mouse[1] <= 675:
            pygame.draw.rect(screen, GREY, [100, 600, 175, 75])
            screen.blit(Scoreboard, (100, 600))
        else:
            pygame.draw.rect(screen, WHITE, [100, 600, 175, 75])
            screen.blit(Scoreboard, (100, 600))

        # Updating the screen so the changes can be seen
        pygame.display.update()


"""
The Game Mode function represents the game mode selection screen,
allowing users to choose between Single Player and Multiplayer modes.

"""


def GameMode():
    pygame.init()

    # Set the size of the window
    size = (800, 700)
    screen = pygame.display.set_mode(size)

    # Colors to use
    PURPLE = (128, 0, 128)
    WHITE = (255, 255, 255)
    GREY = (197, 197, 197)

    # Setting the title of the game screen
    pygame.display.set_caption("Game Mode")
    pygame.display.set_icon(pygame.image.load("Images/icon_game.png"))

    # Text font
    title_arcade_font = pygame.font.Font("Fonts/arcade_font.ttf", 40)
    arcade_font = pygame.font.Font("Fonts/arcade_font.ttf", 25)

    # Texts
    title = title_arcade_font.render('CHOOSE A GAME MODE', True, WHITE)
    single_player = arcade_font.render('SINGLE PLAYER', True, WHITE)
    multiplayer = arcade_font.render('MULTIPLAYER', True, WHITE)

    interface = pygame.image.load("Images/main_menu.png")
    interface = pygame.transform.scale(interface, [150, 50])

    # Main loop of the game mode screen
    while True:
        # Getting the position of the mouse so we know where the player is clicking
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
                    Interface()
                if 0 <= mouse[0] <= 399 and 0 <= mouse[1] <= 700:
                    pygame.mixer.music.stop()
                    SinglePlayer()
                if 401 <= mouse[0] <= 800 and 0 <= mouse[1] <= 700:
                    pygame.mixer.music.stop()
                    Multiplayer()

        # Setting the background image
        screen_image = pygame.image.load("Images/gamemode_interface.png")
        screen_image = pygame.transform.scale(screen_image, [800, 700])

        # Setting the texts in the screen with a background rectangle behind the title
        screen.blit(screen_image, [0, 0])

        # Draw background rectangle behind the title
        pygame.draw.rect(screen, PURPLE, [20, 92, 745, 60])
        screen.blit(title, (35, 100))

        # Draw background rectangle behind the text below the title
        pygame.draw.rect(screen, PURPLE, [25, 196, 340, 38])
        screen.blit(single_player, (35, 200))

        # Draw background rectangle behind the text below the title
        pygame.draw.rect(screen, PURPLE, [450, 196, 290, 38])
        screen.blit(multiplayer, (460, 200))

        # The lines below are the buttons of the interface screen
        if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
            pygame.draw.rect(screen, GREY, [600, 600, 150, 50])
            screen.blit(interface, (600, 600))
        else:
            pygame.draw.rect(screen, WHITE, [600, 600, 150, 50])
            screen.blit(interface, (600, 600))

        if 0 <= mouse[0] <= 399 and 0 <= mouse[1] <= 700:
            pygame.draw.rect(screen, PURPLE, [0, 399, 0, 700])
        else:
            pygame.draw.rect(screen, WHITE, [0, 399, 0, 700])

        if 401 <= mouse[0] <= 800 and 0 <= mouse[1] <= 700:
            pygame.draw.rect(screen, PURPLE, [401, 399, 0, 700])
        else:
            pygame.draw.rect(screen, WHITE, [401, 399, 0, 700])

        # Updating the screen so the changes can be seen
        pygame.display.update()


"""
The Credits function displays the credits screen, where users can view the 
information about the game's creators, and return to the main menu.

"""


def Credits():
    pygame.init()

    size = (800, 700)

    # Setting a size to the window of the credits screen
    screen = pygame.display.set_mode(size)

    GREY = (197, 197, 197)
    WHITE = (255, 255, 255)

    # Load background image
    background_image = pygame.image.load("Images/background_credits.png")
    background_image = pygame.transform.scale(background_image, [800, 700])

    interface = pygame.image.load("Images/main_menu.png")
    interface = pygame.transform.scale(interface, [150, 50])

    # Setting the caption of the credits screen
    pygame.display.set_caption("Credits")
    pygame.display.set_icon(pygame.image.load("Images/credits_icon.png"))

    # Adding an icon to the credits screen
    icon = pygame.image.load("Images/caption.png")
    pygame.display.set_icon(icon)

    # Main loop of the credits screen
    while True:

        # If the mouse is clicked in any button, it will do what is writen in that button
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
                    Interface()

        screen.blit(background_image, [0, 0])

        # Getting the position of the mouse so we know where the player is clicking
        mouse = pygame.mouse.get_pos()

        # The lines below are the buttons of the credits screen
        if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
            pygame.draw.rect(screen, GREY, [600, 600, 150, 50])
            screen.blit(interface, (600, 600))
        else:
            pygame.draw.rect(screen, WHITE, [600, 600, 150, 50])
            screen.blit(interface, (600, 600))

        # Updating the screen so the changes can be seen
        pygame.display.update()


"""
The function Rules presents the instructions of the game and 
illustrates the existing power ups, with the option of returning to the main menu

"""


def Rules():
    pygame.init()

    size = (800, 700)
    screen = pygame.display.set_mode(size)

    # Colors to use
    WHITE = (255, 255, 255)
    GREY = (197, 197, 197)
    background = (2, 0, 36)

    # Setting the title of the game screen
    pygame.display.set_caption("Rules of the game")
    pygame.display.set_icon(pygame.image.load("Images/rules_icon.png"))

    background_image = pygame.image.load("Images/rules_background.png")
    background_image = pygame.transform.scale(background_image, [800, 700])

    interface = pygame.image.load("Images/main_menu.png")
    interface = pygame.transform.scale(interface, [150, 50])

    while True:
        screen.fill(background)  # Set the background color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
                    Interface()

        screen.blit(background_image, [0, 0])

        mouse = pygame.mouse.get_pos()

        # The lines below are the buttons of the credits screen
        if 600 <= mouse[0] <= 750 and 625 <= mouse[1] <= 675:
            pygame.draw.rect(screen, GREY, [600, 625, 150, 50])
            screen.blit(interface, (600, 625))
        else:
            pygame.draw.rect(screen, WHITE, [600, 625, 150, 50])
            screen.blit(interface, (600, 625))

        pygame.display.update()


def Settings():
    pygame.init()

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHTSTEELBLUE = (176, 196, 222)
    GREY = (197, 197, 197)

    # Set the size of the window
    size = (800, 700)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Settings")
    pygame.display.set_icon(pygame.image.load("Images/settings_icon.png"))

    # Load font
    arcade_font1 = pygame.font.Font("Fonts/arcade_font.ttf", 30)

    volume_text = arcade_font1.render('Volume', True, LIGHTSTEELBLUE)

    # Load images
    sound_on_image = pygame.image.load("Images/sound_on.png")
    sound_on_image = pygame.transform.scale(sound_on_image, [40, 40])

    sound_off_image = pygame.image.load("Images/sound_off.png")
    sound_off_image = pygame.transform.scale(sound_off_image, [40, 40])

    interface = pygame.image.load("Images/main_menu.png")
    interface = pygame.transform.scale(interface, [150, 50])

    # Initialize volume settings
    volume = 0.1

    music = True
    volume_slider_rect = pygame.Rect(550, 400, 200, 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # Check if the mouse click is within the sound button area
                if 490 <= mouse[0] <= 530 and 390 <= mouse[1] <= 430:
                    if music:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play()
                    music = not music
                elif volume_slider_rect.collidepoint(mouse):
                    volume = (mouse[0] - volume_slider_rect.x) / volume_slider_rect.width
                    volume = max(0.0, min(1.0, volume))
                    pygame.mixer.music.set_volume(volume)

                if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
                    Interface()

        # Draw background
        screen_image = pygame.image.load("Images/background_settings.png")
        screen_image = pygame.transform.scale(screen_image, [800, 700])
        screen.blit(screen_image, [0, 0])
        screen.blit(volume_text, (565, 350))

        # Draw sound button based on the state of music
        if music:
            sound_button_image = sound_on_image
        else:
            sound_button_image = sound_off_image
        screen.blit(sound_button_image, (490, 390))

        # Draw volume slider
        pygame.draw.rect(screen, BLACK, volume_slider_rect)
        pygame.draw.rect(screen, WHITE,
                         (volume_slider_rect.x + volume_slider_rect.width * volume - 2, volume_slider_rect.y, 4, 24))
        pygame.draw.line(screen, WHITE, [550, 410], [750, 410], width=5)
        pygame.draw.line(screen, WHITE, [552, 400], [552, 420], width=6)
        pygame.draw.line(screen, WHITE, [748, 400], [748, 420], width=6)

        mouse = pygame.mouse.get_pos()

        # Draw back to the main menu button
        if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
            pygame.draw.rect(screen, GREY, [600, 600, 150, 50])
            screen.blit(interface, (600, 600))
        else:
            pygame.draw.rect(screen, WHITE, [600, 600, 150, 50])
            screen.blit(interface, (600, 600))

        # Draw sound button with different color based on mouse position
        if 490 <= mouse[0] <= 530 and 390 <= mouse[1] <= 430:
            pygame.draw.rect(screen, GREY, [490, 390, 40, 40])
            screen.blit(sound_button_image, (490, 390))
        else:
            pygame.draw.rect(screen, WHITE, [490, 390, 40, 40])
            screen.blit(sound_button_image, (490, 390))

        # Update the screen
        pygame.display.update()