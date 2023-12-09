import pygame

WHITE = (255, 255, 255)
transparent_color = (197, 197, 197, 0.1)

class Airship(pygame.sprite.Sprite):

    """
    A class to represent a airship on the screen.
    Attributes:

    - color (tuple): RGB color tuple representing the color of the airship.
    - width (int): Width of the airship's image.
    - height (int): Height of the airship's image.
    - speed (int): Movement speed of the airship.
    - image (pygame.Surface): Pygame surface representing the airship's image.
    - rect (pygame.Rect): Rectangular area occupied by the airship's image.


    """

    def __init__(self, color, width, height, speed=0, image=None):

        """ Initialize the Airship instance."""
        super().__init__()

        if image is None:
            self.image = pygame.Surface([width, height])
            self.image.fill(transparent_color)
            self.image.set_colorkey(transparent_color)
            self.width = width
            self.height = height
            self.color = color
            pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])
            self.color = color
        else:
            self.image = pygame.image.load(image)
            self.width = width
            self.height = height
            self.image = pygame.transform.scale(self.image, (width, height))
            self.color = color

        self.rect = self.image.get_rect()
        self.speed = speed

    def moveRight(self, pixels):
        """Move the airship to the right by the specified number of pixels."""
        self.rect.x += pixels

    def moveLeft(self, pixels):
        """Move the airship to the left by the specified number of pixels."""
        self.rect.x -= pixels

    def moveForward(self, pixels):
        """Move the airship forward by the specified number of pixels."""
        self.rect.y -= pixels

    def moveDown(self, pixels):
        """Move the airship down by the specified number of pixels."""
        self.rect.y += pixels

    def repaint(self, color):
        """Repaint the airship with the specified color."""

        self.image.fill(transparent_color)
        self.image.set_colorkey(transparent_color)
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

    def resize(self, width, height):
        """Resize the airship to the specified width and height."""
        self.image = pygame.Surface([width, height])
        self.image.fill(transparent_color)
        self.image.set_colorkey(transparent_color)
        self.width = width
        self.height = height
        pygame.draw.rect(self.image, self.color, [0, 0, width, height])

    def change_speed(self, new_speed):
        self.speed = new_speed

    def change_color(self, new_color):
        if not hasattr(self, 'original_image'):  # Verifica se a imagem original já foi salva
            self.original_image = self.image.copy()  # Salva a imagem original


        """Creates a copy of the original image."""
        self.image = self.original_image.copy()

        # Altera a cor da imagem preservando a transparência
        """Changes the color of the image, keeping the transparency."""
        self.image.fill(new_color, special_flags=pygame.BLEND_MULT)
        self.image.set_colorkey(transparent_color)

    def restore_color(self):
        if hasattr(self, 'original_image'):  # Verifies if the original image was stored
            # Restores the original color of the image
            self.image = self.original_image.copy()
            self.image.set_colorkey(transparent_color)


