# Shark Swim 🦈

A fast-paced, arcade-style 2D side-scrolling game built with Pygame. Control a speedy shark swimming through a hazardous ocean filled with sliding ice barriers 🧊 and hungry fish 🐟. Eat the fish to gain points, avoid obstacles to survive, and aim for a high score! 🏆

## Features ✨

- Smooth, responsive shark movement with up/down controls ⬆️⬇️
- Randomly spawning fish as collectible targets to increase score 🐠
- Challenging ice barriers attached to screen edges with alternating gap sizes for varied difficulty 🧊
- Dynamic floating text effects for eating fish and crashing 💥
- Background scrolling for ocean ambiance 🌊
- Sound effects and background music (optional) 🎶
- Start screen with blinking "Press Space to Start" prompt ▶️
- Game over screen with final score and option to restart with 'R' key 🔄

## Controls 🎮

- Up Arrow: Move shark upward ⬆️
- Down Arrow: Move shark downward ⬇️
- Space: Start the game from title screen ▶️
- R: Restart the game after game over 🔄
- Close Window: Quit the game ❌

## Installation 🛠️

1. Make sure you have Python 3.x and Pygame installed:

   pip install pygame

2. Download the game assets:

   - background.png 🌅
   - shark.png 🦈
   - fish.png 🐟
   - ice.png 🧊
   - eat.mp3 🍽️
   - crash.mp3 💥
   - music.mp3 🎵

3. Place the assets alongside the Python script.

## Running the Game ▶️

Run the main Python script:

   python game.py

The game window opens with a title screen. Press Space to begin playing.

## Gameplay Tips 💡

- Use smooth, careful movements to avoid the ice barriers 🧊.
- Collect as many fish as possible for a higher score 🐠🏆.
- Pay attention to alternating gap sizes; some are smaller and more difficult ⚠️.
- Enjoy vibrant floating texts and sound effects 🎉.

## Code Structure Highlights 🧩

- Shark, Fish, and Barrier classes handle game objects 🦈🐟🧊.
- FloatingText sprites display on-screen feedback ✨.
- Event timers spawn fish and barriers regularly ⏳.
- Game states manage start, playing, and game over 🔄.
- Pygame mixer controls music and effects 🎵.

## License 📜

Open source and free to use for learning or personal projects.
