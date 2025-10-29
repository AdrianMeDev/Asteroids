"""
Asteroid Game Main Module

This module implements the main game loop and initialization for an asteroid shooting game.
It handles the game's core mechanics including collision detection, rendering, and event handling.
"""

import pygame
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASTEROID_MIN_RADIUS,
    ASTEROID_KINDS,
    ASTEROID_SPAWN_RATE,
    ASTEROID_MAX_RADIUS,
)

# Initialize the main game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def main():
    """
    Main game function that initializes the game and runs the main game loop.
    Handles sprite groups, collision detection, and frame updates.
    """
    # Initialize Pygame
    pygame.init()

    # Create sprite groups for different game elements
    updatable = pygame.sprite.Group()  # Sprites that need updating each frame
    drawable = pygame.sprite.Group()  # Sprites that need to be drawn
    asteroids = pygame.sprite.Group()  # Group specifically for asteroid sprites
    shots = pygame.sprite.Group()  # Group for player shots

    # Set up sprite containers
    Asteroid.containers = (drawable, updatable, asteroids)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, drawable, updatable)

    # Create initial game objects
    asteroid_field = AsteroidField()
    player = Player(
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    )  # Place player at center of screen

    # Initialize game clock and delta time
    clock = pygame.time.Clock()
    dt: float = 0  # Delta time between frames
    # Main game loop
    while True:
        # Handle events (e.g., window closing)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update all game objects
        updatable.update(dt)

        # Check for collisions between game objects
        for asteroid in asteroids:
            # Check for player collision (game over condition)
            game_over = asteroid.detect_collision(player)
            if game_over:
                print("Game over!")
                return

            # Check for shot collision with asteroids
            for shot in shots:
                hit = asteroid.detect_collision(shot)
                if hit:
                    asteroid.split()  # Split asteroid into smaller pieces
                    shot.kill()  # Remove the shot
                    break

        # Render game objects
        screen.fill("black")  # Clear screen
        for el in drawable:  # Draw all game objects
            el.draw(screen)
        pygame.display.flip()  # Update display

        # Calculate time elapsed since last frame
        dt = clock.tick(60) / 1000  # Target 60 FPS, convert to seconds


if __name__ == "__main__":
    main()
