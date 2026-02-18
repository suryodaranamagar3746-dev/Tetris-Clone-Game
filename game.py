import pygame
from setting import *
from random import choice
from timer import Timer
from sys import exit


class Game:
    def __init__(self, get_next_shape, update_score):
        # General Setup
        # Create the internal game surface
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        # Get reference to the main window
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(
            topleft=(PADDING, PADDING))  # Position the game area
        # Group to manage all block sprites
        self.sprites = pygame.sprite.Group()

        # Connections to Main.py
        self.get_next_shape = get_next_shape  # Callback to get next piece from Main
        self.update_score = update_score     # Callback to update UI in Main

        # Field Data: 2D list representing the grid (0 = empty, Block = occupied)
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]

        # Movement Timers & Initial State
        self.reset()  # Call reset to initialize all game variables

    def reset(self):
        """Wipes the board and resets all stats for a new game."""
        self.game_active = True             # Set game state to active
        self.sprites.empty()                # Remove all existing block sprites
        self.field_data = [[0 for x in range(COLUMNS)]
                           for y in range(ROWS)]  # Clear grid data

        # Reset Score & Leveling
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.1
        self.down_pressed = False

        # Reset Timers
        self.timers = {
            'vertical move': Timer(self.down_speed, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME)
        }
        self.timers['vertical move'].activate()  # Start the gravity timer

        # Update the UI in Main.py back to zero
        self.update_score(0, 0, 1)

        # Spawn the very first piece
        self.create_new_tetromino()

    def create_new_tetromino(self):
        """Logic to spawn the next piece or trigger Game Over."""
        self.checked_finsihed_rows()  # Clear full lines before spawning next
        next_shape_type = self.get_next_shape()  # Get shape from Main's list

        # Check for Game Over: If the spawn area is already occupied
        for pos in TETROMINOS[next_shape_type]['shape']:
            x = int(pos[0] + COLUMNS // 2)
            y = int(pos[1])
            if y >= 0 and self.field_data[y][x]:  # If grid cell is not 0
                self.game_active = False  # End the game loop
                return

        # If not game over, create the new piece
        self.tetromino = Tetrimono(
            next_shape_type,
            self.sprites,
            self.create_new_tetromino,
            self.field_data
        )

    def input(self):
        """Handles keyboard input for movement and restart."""
        keys = pygame.key.get_pressed()

        # RESTART LOGIC: Check this even if game_active is False
        if not self.game_active:
            if keys[pygame.K_r]:  # If 'R' is pressed during Game Over
                self.reset()     # Re-initialize everything
            return               # Skip movement logic if game is over

        # Horizontal movement (Left/Right)
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

        # Rotation movement (Up)
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

        # Soft Drop (Down)
        if not self.down_pressed and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster
        if self.down_pressed and not (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed

    def calculate_scores(self, num_lines):
        """Calculates points and handles leveling up."""
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        # Level up every 10 lines
        if self.current_lines // 10 >= self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75  # Increase speed
            self.timers['vertical move'].duration = self.down_speed

        self.update_score(self.current_lines,
                          self.current_score, self.current_level)

    def checked_finsihed_rows(self):
        """Checks for full rows, deletes them, and shifts blocks down."""
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):  # If every cell in the row has a block
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                for block in self.field_data[delete_row]:
                    block.kill()  # Remove block from sprite group

                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1  # Move blocks above down by 1

            # Refresh field data grid
            self.field_data = [
                [0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            self.calculate_scores(len(delete_rows))

    def display_game_over(self):
        """Draws the dark overlay, final stats, and restart instructions."""
        # 1. Create a dark semi-transparent overlay surface
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)  # Semi-transparent black
        self.surface.blit(overlay, (0, 0))

        # 2. Setup Fonts
        font = pygame.font.SysFont('Arial', 40, bold=True)
        small_font = pygame.font.SysFont('Arial', 25, bold=False)

        # 3. Render Text surfaces
        title_surf = font.render('GAME OVER', True, 'white')
        score_surf = small_font.render(
            f'Final Score: {self.current_score}', True, 'white')
        level_surf = small_font.render(
            f'Final Level: {self.current_level}', True, 'white')
        restart_surf = small_font.render('Press R to Restart', True, 'yellow')

        # 4. Draw text to the center of the game surface
        # We use a vertical stack to keep it organized
        center_x = GAME_WIDTH / 2

        self.surface.blit(
            title_surf, (center_x - title_surf.get_width() / 2, 150))
        self.surface.blit(
            score_surf, (center_x - score_surf.get_width() / 2, 220))
        self.surface.blit(
            level_surf, (center_x - level_surf.get_width() / 2, 260))
        self.surface.blit(
            restart_surf, (center_x - restart_surf.get_width() / 2, 320))

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (x, 0),
                             (x, self.surface.get_height()), 1)
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (0, y),
                             (self.surface.get_width(), y))

    def run(self):
        """The main update and draw call for the game component."""
        self.surface.fill(GRAY)  # Clear game surface

        self.input()  # Always check input (to catch 'R' key)

        if self.game_active:
            self.timer_update()  # Update timers
            self.sprites.update()  # Update block positions
            self.sprites.draw(self.surface)  # Draw blocks
            self.draw_grid()  # Draw the grid lines
        else:
            self.sprites.draw(self.surface)  # Draw frozen blocks
            self.draw_grid()  # Draw frozen grid
            self.display_game_over()  # Draw restart menu

        # Final blit: Send the game surface to the main display
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

# --- TETROMINO CLASS ---


class Tetrimono:
    def __init__(self, shape, group, create_new_tetromino, field_data):
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data
        self.blocks = [Block(group, pos, self.color)
                       for pos in self.block_positions]

    def next_move_horizontal_collide(self, blocks, amount):
        return any(block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks)

    def next_move_vertical_collide(self, blocks, amount):
        return any(block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks)

    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    def rotate(self):
        if self.shape != 'O':
            pivot_pos = self.blocks[0].pos
            new_block_positions = [block.rotate(
                pivot_pos) for block in self.blocks]
            for pos in new_block_positions:
                if pos.x < 0 or pos.x >= COLUMNS:
                    return
                if pos.y >= ROWS:
                    return
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]


# --- BLOCK CLASS ---

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)
        self.image = pygame.Surface(
            (CELL_SIZE, CELL_SIZE))  # Size of 1 grid cell
        self.image.fill(color)
        # Position is grid-based (e.g., x=5, y=2) rather than pixel-based
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        # Convert grid position to actual screen pixels for drawing
        self.rect = self.image.get_rect(topleft=self.pos * CELL_SIZE)

    def rotate(self, pivot_pos):
        """Calculates rotation around a pivot using Pygame's vector rotate."""
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data):
        """Checks horizontal boundaries and grid data."""
        if not 0 <= x < COLUMNS:
            return True  # Hits side walls
        if field_data[int(self.pos.y)][x]:
            return True  # Hits existing block
        return False

    def vertical_collide(self, y, field_data):
        """Checks vertical floor and grid data."""
        if y >= ROWS:
            return True  # Hits floor
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True  # Hits existing block
        return False

    def update(self):
        """Updates the visual rectangle to match the current grid position."""
        self.rect.topleft = self.pos * CELL_SIZE
