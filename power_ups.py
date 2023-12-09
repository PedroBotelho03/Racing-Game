import pygame
import random


class PowerUp(pygame.sprite.Sprite):
    """
        Initialize the Power Up.

        Parameters:
        - color (tuple): Tuple representing the RGB color.
        - width (int): Width of the PowerUp.
        - height (int): Height of the PowerUp.
        - image (str): Filename of the power-up image.

        If image is None, a colored surface will be used.
        If image is provided, it will be scaled to the specified width and height.
        """

    def __init__(self, color, width, height, image=None):
        super().__init__()

        if image is None:
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
        else:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()

    def reset_position(self, game_mode):
        if game_mode == "single":
            road = "left"
        elif game_mode == "multi":
            road = random.choice(["left", "right"])
        if road == "left":
            self.rect.x = random.randint(150, 520)
        elif road == "right":
            self.rect.x = random.randint(700, 1100)
        self.rect.y = random.randint(-1000, -300)

    def update(self, speed, game_mode):
        self.rect.y += speed
        if self.rect.y > 600:
            self.reset_position(game_mode)
