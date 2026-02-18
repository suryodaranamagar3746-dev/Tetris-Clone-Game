# Pygame Tetris

A robust, object-oriented implementation of the classic Tetris game built with Python and the **Pygame** library. This project features high-fidelity mechanics, a modular code architecture, and a dynamic leveling system.

---

## 🚀 Features

* **Authentic Gameplay**: Precise collision detection, tetromino rotation, and line-clearing logic using a 2D grid matrix.
* **Dynamic Difficulty**: Automatic level progression that increases the fall speed as you clear more lines.
* **Advanced UI**: 
    * **Main Game Grid**: Classic 10x20 layout with custom grid line rendering.
    * **Preview Window**: Real-time rendering of the next three upcoming shapes using dedicated image assets.
    * **Scoreboard**: Tracks real-time score, total lines cleared, and current level with custom font support.
* **Responsive Input**: Custom timer system for fluid movement and rotation without "sticky" keys.
* **Game Over State**: Darkened overlay with final stats and an instant restart functionality.

---

## 🏗️ Internal Architecture

The project is divided into several modules to ensure a clean separation of concerns:

### 1. Game Core (`game.py`)
* **Field Data**: Uses a 2D list to track static blocks and manage the game state.
* **Tetromino Logic**: Manages individual block positions using `pygame.Vector2` for seamless 90-degree rotations around a pivot point.
* **Collision System**: Specialized checks for boundaries (walls/floor) and internal collisions with existing blocks.

### 2. UI & Component Management (`main.py`, `score.py`, `preview.py`)
* **Main Hub**: Coordinates communication between the `Game`, `Score`, and `Preview` components.
* **Score Component**: Handles dynamic text rendering of stats using the `Russo_One` font.
* **Preview Component**: Manages the loading and display of `.png` shape images for the "Next Piece" queue.

### 3. Timing & Performance (`timer.py`)
* **Custom Timers**: A specialized class based on `pygame.time.get_ticks()` to manage gravity, movement delays, and rotation cooldowns independently of the frame rate.

### 4. Configuration (`setting.py`)
* **Centralized Settings**: A single source of truth for game constants, including HEX colors, grid dimensions, and coordinate data for all seven tetromino shapes (I, J, L, O, S, T, Z).

---

## 🕹️ Controls & Input Handling

The game utilizes a "Soft Drop" mechanic and specific cooldown timers to ensure a responsive feel.

| Key | Action | Internal Logic |
| :--- | :--- | :--- |
| **Left Arrow / A** | Move Left | Triggers `MOVE_WAIT_TIME` timer; checks grid collision. |
| **Right Arrow / D** | Move Right | Triggers `MOVE_WAIT_TIME` timer; checks grid collision. |
| **Up Arrow / W** | Rotate Shape | Rotates 90° around pivot; includes wall-kick safety checks. |
| **Down Arrow / S** | Soft Drop | Multiplies downward speed by 0.1 for rapid descent. |
| **R Key** | Restart | Resets all game data and stats after a Game Over. |
| **Esc** | Exit | Safely terminates the Pygame instance and system process. |

---

## 🎮 Getting Started

### Prerequisites
* Python 3.x
* Pygame library

### Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/pygame-tetris.git](https://github.com/yourusername/pygame-tetris.git)
   cd pygame-tetris
Install dependencies:

Bash
pip install pygame
Asset Requirement: Ensure your project directory contains a Shapes/ folder with the following files:

Images: I.png, J.png, L.png, O.png, S.png, T.png, Z.png

Font: Russo_One.ttf

Running the Game
Execute the main script to start the application:

Bash
python main.py
