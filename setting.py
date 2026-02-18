import pygame

# --- Game Board Dimensions ---
COLUMNS = 10  # Number of vertical lanes in the grid
ROWS = 20    # Number of horizontal lanes in the grid
CELL_SIZE = 30  # The pixel size of a single square block
# Total pixel dimensions of the playable game area
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

# --- Sidebar (UI) Dimensions ---
SIDEBAR_WIDTH = 200  # Width of the area holding the next piece and score
PREVIEW_HEIGHT_FRACTION = 0.7  # Top 70% of sidebar is for the piece preview
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION  # Bottom 30% is for the score

# --- Window Layout ---
PADDING = 20  # Space between the game board, sidebar, and window edges
# Total width of the window (Game + Sidebar + 3 gaps of padding)
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
# Total height of the window (Game height + top and bottom padding)
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

# --- Game Physics & Timing ---
UPDATE_START_SPEED = 700  # Initial milliseconds between automatic downward moves
MOVE_WAIT_TIME = 500     # Delay in ms before a held key moves the piece again
ROTATE_WAIT_TIME = 200   # Delay in ms to prevent accidental double-rotations
# The starting coordinate for every new piece (Centered X, just above screen Y)
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

# --- Visual Identity (Colors) ---
YELLOW = "#f1e60d"
RED = "#e51b20"
BLUE = "#204b9b"
GREEN = "#65b32e"
PURPLE = "#7b217f"
CYAN = "#6cc6d9"
ORANGE = "#f07e13"
GRAY = "#1C1C1C"      # Background color
LINE_COLOR = "#FFFFFFFF"  # Grid line color (White)

# --- Tetromino Shapes & Data ---
# 'shape' defines the relative grid coordinates of the 4 blocks in the piece
# (0,0) is the pivot point the piece rotates around

TETROMINOS = {
    'T': {'shape': [(0, 0), (-1, -1), (1, -1), (0, -1)], 'color': PURPLE},
    'O': {'shape': [(0, 0), (0, -1), (1, 0), (1, -1)], 'color': YELLOW},
    'J': {'shape': [(0, 0), (0, -1), (0, 1), (-1, 1)], 'color': BLUE},
    'L': {'shape': [(0, 0), (0, -1), (0, 1), (1, 1)], 'color': ORANGE},
    'I': {'shape': [(0, 0), (0, -1), (0, -2), (0, 1)], 'color': CYAN},
    'Z': {'shape': [(0, 0), (1, 0), (0, -1), (-1, -1)], 'color': GREEN},
    'S': {'shape': [(0, 0), (-1, 0), (0, -1), (1, -1)], 'color': RED},
}

# --- Scoring System ---
# Points awarded based on how many lines are cleared simultaneously
# 1 line = 40, 2 = 100, 3 = 300, 4 = 1200 (The "Tetris")
SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}
