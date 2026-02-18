from setting import *  # Import game constants (colors, sizes, etc.)
from pygame.image import load       # Import the function to load image files
from os import path   # Import path to handle folder/file directories safely


class Preview:
    def __init__(self):

        # --- General Setup ---
        # Get a reference to the main window surface
        self.display_surface = pygame.display.get_surface()

        # Create the preview surface based on sidebar width and a fraction of game height
        self.surface = pygame.Surface(
            (SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))

        # Create a rectangle to position the preview box at the top-right of the window
        self.rect = self.surface.get_rect(
            topright=(WINDOW_WIDTH - PADDING, PADDING))

        # --- Shapes Setup ---
        # Dictionary comprehension: Load and convert the .png image for every Tetromino type
        # It looks in the 'Shapes' folder for files like 'I.png', 'O.png', etc.
        self.shape_surfaces = {shape: load(path.join(
            'Shapes', f'{shape}.png')).convert_alpha() for shape in TETROMINOS.keys()}

        # --- Image Position Data ---
        # Divide the preview surface height by 3 to create slots for the 3 upcoming pieces
        self.increment_height = self.surface.get_height() / 3

    def display_pieces(self, shapes):
        """Draws the upcoming shapes onto the preview surface."""
        for i, shape in enumerate(shapes):
            # Pick the correct image from our pre-loaded dictionary
            shape_surface = self.shape_surfaces[shape]

            # Calculate the horizontal center of the preview box
            x = self.surface.get_width() / 2

            # Calculate the vertical center for each slot (i=0, 1, or 2)
            y = self.increment_height / 2 + i * self.increment_height

            # Create a rect for the image and center it at our calculated x, y
            rect = shape_surface.get_rect(center=(x, y))

            # Draw (blit) the piece image onto the preview surface
            self.surface.blit(shape_surface, rect)

    def run(self, next_shapes):
        """The main method to update and draw the preview UI."""
        # Fill the background of the preview box with gray
        self.surface.fill(GRAY)

        # Draw the images of the next shapes
        self.display_pieces(next_shapes)

        # Draw the preview surface onto the main display window
        self.display_surface.blit(self.surface, self.rect)

        # Draw a border around the preview box
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
