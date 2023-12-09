import pygame


# Interface of the game over screen
def GameOver(score, playerairship, playeraiship2):

    """
    Display the game over screen with options to restart,
    quit, or go back to the main menu interface.

    Parameters:

        - score (int) : The final score of the game
        - player_airship (bool): True if player1 is the winner, False otherwise.
        - player_airship2 (bool): True if player2 is the winner, False otherwise.


    """

    from interface import Interface, GameMode

    # Initialize pygame
    pygame.init()

    # Set the screen size
    size = (800, 700)
    screen = pygame.display.set_mode(size)

    # Setting the caption of the interface screen
    pygame.display.set_caption("Game Over, play again")

    # Adding an icon to the interface screen
    pygame.display.set_icon(pygame.image.load("Images/gameover_icon.png"))

    # Colors to use
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (197, 197, 197)

    # Setting the title of the game screen
    pygame.display.set_caption("Game Over, play more!!!")

    # Text font
    arcade_font = pygame.font.Font('Fonts/arcade_font.ttf', 20)

    # Texts to be displayed
    restart_button = pygame.image.load("Images/restart_pause.png")
    restart_button = pygame.transform.scale(restart_button, [150, 50])

    quit_button = pygame.image.load("Images/quit.png")
    quit_button = pygame.transform.scale(quit_button, [150, 50])

    main_menu_button = pygame.image.load("Images/main_menu.png")
    main_menu_button = pygame.transform.scale(main_menu_button, [150, 50])

    # Load background image
    background_image = pygame.image.load("Images/background_gameover.png")
    background_image = pygame.transform.scale(background_image, [800, 700])

    # Load the sound of the game over screen
    pygame.mixer.music.load("Sounds/game_over.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    # Main loop of the game over screen
    while True:
        screen.fill(BLACK)  # Set the background color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # If the mouse is clicked in any button, it will do what is written in that button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 475 <= mouse[0] <= 625 and 400 <= mouse[1] <= 450:
                    pygame.mixer.music.stop()
                    GameMode()

                if 325 <= mouse[0] <= 475 and 500 <= mouse[1] <= 550:
                    pygame.mixer.music.stop()
                    pygame.quit()

                if 175 <= mouse[0] <= 325 and 400 <= mouse[1] <= 450:
                    pygame.mixer.music.stop()
                    Interface()

        mouse = pygame.mouse.get_pos()
        screen.blit(background_image, [0, 0])

        if score is not None:
            if score < 50:
                score_text = arcade_font.render("Final score: {}".format(score), True, WHITE)
                score_text1 = arcade_font.render("You are a loser, damn!", True, WHITE)
                screen.blit(score_text, (240, 220))
                screen.blit(score_text1, (210, 280))
            else:
                score_text = arcade_font.render("Final score: {}".format(score), True, WHITE)
                screen.blit(score_text, (240, 220))

        if playerairship:
            winner_text = arcade_font.render("Player1 is the winner!", True, WHITE)
            screen.blit(winner_text, (235, 220))

        elif playeraiship2:
            winner_text = arcade_font.render("Player2 is the winner!", True, WHITE)
            screen.blit(winner_text, (235, 220))

        # Create the buttons
        if 475 <= mouse[0] <= 625 and 400 <= mouse[1] <= 450:
            pygame.draw.rect(screen, GREY, [475, 400, 150, 50])
            screen.blit(restart_button, (475, 400))
        else:
            pygame.draw.rect(screen, WHITE, [475, 400, 150, 50])
            screen.blit(restart_button, (475, 400))

        if 325 <= mouse[0] <= 475 and 500 <= mouse[1] <= 550:
            pygame.draw.rect(screen, GREY, [325, 500, 150, 50])
            screen.blit(quit_button, (325, 500))
        else:
            pygame.draw.rect(screen, WHITE, [325, 500, 150, 50])
            screen.blit(quit_button, (325, 500))

        if 175 <= mouse[0] <= 325 and 400 <= mouse[1] <= 450:
            pygame.draw.rect(screen, GREY, [175, 400, 150, 50])
            screen.blit(main_menu_button, (175, 400))
        else:
            pygame.draw.rect(screen, WHITE, [175, 400, 150, 50])
            screen.blit(main_menu_button, (175, 400))

        pygame.display.update()