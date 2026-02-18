import pygame
from setting import *  # Imports constants (WINDOW_WIDTH, COLORS, TETROMINOS)
from sys import exit         # Required to close the window without errors

# Internal components of the Tetris project
from game import Game        # Handles the grid, falling blocks, and collisions
from score import Score      # Handles the UI for points, lines, and level
from preview import Preview  # Handles the UI showing the upcoming shapes

from random import choice    # Used to pick a random shape from the dictionary keys


class Main:
    def __init__(self):
        """Initializes the game engine, window, and game components."""

        # 1. Pygame Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()  # Controls the game's frame rate (FPS)

        # 2. Shape Management
        self.next_shapes = [choice(list(TETROMINOS.keys()))
                            for shape in range(3)]

        # 3. Component Initialization
        # --- IMPORTANT: Create Score and Preview BEFORE Game ---
        self.score = Score()
        self.preview = Preview()

        # Now that self.score exists, we can safely create the Game
        # because the Game's reset() function will try to talk to self.score
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

    def update_score(self, lines, score, level):
        """Updates the Score object with new data coming from the Game logic."""
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        """Pops the first shape from the preview list and adds a new random one."""
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        """The Main Game Loop that runs indefinitely while the game is open."""
        while True:
            # 1. Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # 2. Visual Background
            self.display_surface.fill(GRAY)

            # 3. Component Execution
            # The Game class now handles its own internal "Game Over" state
            # and listens for the 'R' key to call its own reset() method.
            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            # 4. Refresh Screen
            pygame.display.update()

            # Use a fixed FPS (e.g., 60) to prevent the game from running too fast
            self.clock.tick(60)


# This ensures the game only starts if this specific file is executed
if __name__ == "__main__":
    main = Main()
    main.run()
