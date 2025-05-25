# Lissana Gaha Nagima (Slippery Pole Climbing Game)

A simple 2D game based on the traditional Sri Lankan game "Lissana Gaha Nagima" where players attempt to climb a slippery pole.

## Game Description

In this game, you control a climber trying to reach the top of a slippery pole. The gameplay includes:

- Climb up using the UP arrow key
- Balance yourself when slipping by pressing A or D when prompted
- Avoid falling coconuts that will knock you down
- Reach the top to win!

## Controls

- **UP Arrow**: Climb up the pole
- **A/D Keys**: Balance when slipping (press the key shown on screen)
- **R Key**: Restart the game after winning or losing

## Game Features

- Realistic climbing and slipping mechanics
- Random coconut obstacles
- Score tracking based on height climbed
- Win and lose conditions
- Sound effects and visual feedback

## Setup and Running

1. Make sure you have Python and PyGame installed:
   ```
   pip install pygame
   ```

2. Run the game:
   ```
   python slippery_pole_game.py
   ```

## Assets

For the full experience, create an `assets` folder with the following files:
- background.png - A festive village background
- pole.png - The slippery pole image
- climber.png - The character sprite
- coconut.png - Coconut obstacle
- Sound effects: climb.wav, slip.wav, fall.wav, hit.wav, win.wav

The game will still work without these assets, using colored shapes instead.

## Customization

You can easily modify game parameters by changing the constants at the top of the script:
- Adjust difficulty by changing CLIMB_SPEED, SLIP_SPEED, and COCONUT_SPAWN_RATE
- Change the game dimensions with SCREEN_WIDTH and SCREEN_HEIGHT
- Modify character sizes and other visual elements
