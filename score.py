from setting import *  # Import game-wide variables like COLORS and dimensions
from os.path import join  # Used to combine folder and file names for the font path


class Score:
    def __init__(self):

        # --- General Setup ---
        # Create the surface for the score box based on settings
        self.surface = pygame.Surface(
            (SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))

        # Position the score box at the bottom-right corner of the window
        self.rect = self.surface.get_rect(bottomright=(
            WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))

        # Get a reference to the main game window to draw onto
        self.display_surface = pygame.display.get_surface()

        # --- Font Setup ---
        # Load the custom font from the 'Shapes' folder at size 30
        self.font = pygame.font.Font(join('Shapes', 'Russo_One.ttf'), 30)

        # --- Layout Logic ---
        # Divide the surface into 3 equal vertical sections for Score, Level, and Lines
        self.increment_height = self.surface.get_height() / 3

        # --- Game Data ---
        # Initialize the starting values for the display
        self.score = 0
        self.level = 1
        self.lines = 0

    def display_text(self, pos, text):
        """Converts raw data into a text image and draws it."""
        # Create a text surface (render) with the format "Label:Value" in white
        text_surface = self.font.render(f'{text[0]}: {text[1]}', True, 'white')

        # Create a rectangle for the text and center it at the provided position
        text_rect = text_surface.get_rect(center=pos)

        # Draw the text image onto the score box surface
        self.surface.blit(text_surface, text_rect)

    def run(self):
        """Updates and draws the score UI every frame."""
        # Clear the score box with a gray background
        self.surface.fill(GRAY)

        # Loop through the three data points to calculate their positions
        for i, text in enumerate([('Score', self.score), ('Level', self.level), ('Lines', self.lines)]):
            # Horizontal center of the box
            x = self.surface.get_width() / 2
            # Vertical position: centers the text within its 1/3 section
            y = self.increment_height / 2 + i * self.increment_height

            # Call the helper function to draw this specific line of text
            self.display_text((x, y), text)

        # Draw the finished score box onto the main game window
        self.display_surface.blit(self.surface, self.rect)

        # Draw a border around the score box for better visibility
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
