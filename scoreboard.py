import pygame


def load_scores():
    """
    Loads scores from the scores.txt file

    :return:
    - list: A list of integer scores
    """

    try:
        with open("Scores/scores.txt", "r") as file:
            lines = file.readlines()
            return [int(line.strip()) for line in lines]
    except FileNotFoundError:
        return []

# Function to save the scores
def save_scores(scores):

    """
    Save the provided scores to the scores.txt file

    Parameters:
    - scores (list): A list of integer scored to be saved
    """

    with open("Scores/scores.txt", "w") as file:
        for score in scores:
            file.write(str(score) + "\n")

# Function to display the scoreboard
def display_scoreboard(scoreboard):

    """
    Displays the scoreboard.

    Parameters:
    - scoreboard (list): A list of integer scores to be displayed

    """

    from interface import Interface
    pygame.init()

    size = (800, 700)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Retro Space Jam - Scoreboard")
    pygame.display.set_icon(pygame.image.load("Images/score_icon.png"))
    

    arcade_font = pygame.font.Font("Fonts/arcade_font.ttf", 30)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    GREY = (197, 197, 197)
    PURPLE = (125, 6, 126)

    background = pygame.image.load("Images/scoreboard.png")
    background = pygame.transform.scale(background, [800, 700])

    interface = pygame.image.load("Images/main_menu.png")
    interface = pygame.transform.scale(interface, [150, 50])

    carry_on = True

    while carry_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carry_on = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carry_on = False
                elif event.key == pygame.K_RETURN:
                    Interface()  # Go back to the main menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
                    Interface()

        # Draw a rounded rectangle for the title background
        screen.blit(background, [0,0])
        pygame.draw.rect(screen, BLACK, [50, 30, 700, 40], border_radius=10)
        title_text = arcade_font.render("Top 10 Scores", True, WHITE)
        screen.blit(title_text, (70, 35))

        mouse = pygame.mouse.get_pos()
        # Draw back to the main menu button
        if 600 <= mouse[0] <= 750 and 600 <= mouse[1] <= 650:
            pygame.draw.rect(screen, GREY, [600, 600, 150, 50])
            screen.blit(interface, (600, 600))
        else:
            pygame.draw.rect(screen, WHITE, [600, 600, 150, 50])
            screen.blit(interface, (600, 600))

        y_position = 100
        for i, top_score in enumerate(scoreboard, start=1):
            # Draw rounded rectangles for score entries
            pygame.draw.rect(screen, PURPLE, [50, y_position, 700, 34], border_radius=5)
            score_text = arcade_font.render(f"{i}. {top_score}", True, BLACK)
            screen.blit(score_text, (70, y_position + 3))
            y_position += 40

        pygame.display.flip()

    pygame.quit()