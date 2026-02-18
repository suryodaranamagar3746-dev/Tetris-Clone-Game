import pygame


class Timer:
    def __init__(self, duration, repeated=False, func=None):
        """Sets up the timer's properties."""
        self.repeated = repeated  # If True, the timer restarts automatically (like gravity)
        # The function to run when time is up (e.g., move_down)
        self.func = func
        # How long to wait in milliseconds (e.g., 500ms)
        self.duration = duration

        self.start_time = 0      # Stores the exact millisecond the timer was turned on
        self.active = False      # Tracks if the timer is currently 'ticking'

    def activate(self):
        """Starts the timer by recording the current game time."""
        self.active = True
        # pygame.time.get_ticks() returns how many milliseconds have passed since the game started
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        """Stops the timer and clears the start time."""
        self.active = False
        self.start_time = 0

    def update(self):
        """Constantly checks if enough time has passed to trigger the timer."""
        current_time = pygame.time.get_ticks()

        # Check: Is the difference between 'now' and 'start' greater than the duration?
        if current_time - self.start_time >= self.duration and self.active:

            # 1. Trigger the Function: If a function was assigned, run it now.
            if self.func and self.start_time != 0:
                self.func()

            # 2. Stop: Turn the timer off once the event has happened
            self.deactivate()

            # 3. Repeat: If it's a repeating timer (like gravity), start it again immediately
            if self.repeated:
                self.activate()
