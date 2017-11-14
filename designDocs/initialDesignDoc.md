# Teapot Wars 2 - Initial Design Document
By Joseph Yankel for the 15-112 Term Project, 2017.

## Project Main Concept
Teapot Wars 2 is a multiplayer grid-based RPG with turn-based game elements.
Players control Teapot characters which have different classes and abilities.
Players must work together to navigate a randomized dungeon and defeat the final boss.

## Game Flow
A player starts out in the main menu and can choose to Host or Join a game.
* The hosting player acts as a server. A host will generate and sync the dungeon, enemies, and player positions.
* The remote client player will send their actions to the server and update their visuals based on server commands.
After joining or hosting a game, the player will be taken to a Character Selection screen where they can:
* Pick a class - determining their abilities and Starts
* Create a character name - This will be displayed to other players.
* Pick their favorite color - This will change the color of the local players character and also some of the UI.
Once the player has finalized their decisions, they are either spawned randomly in the dungeon or near one of their friendly players.
Each client controls their own energy bar. This UI determines what actions can be taken and when. Any abilities or movement decrease the energy bar by various amounts and waiting will increase the bar.
Enemies operate on a similar timer and will attack players. As the players delve deeper into the dungeon, the enemies become tougher.
On the final floor, there is a boss. Once the players defeat this boss, the game ends.

## Visuals
The art will be simple 3D graphics and 2D interface. My target art style is cartoony, or cell-shaded.
The main concept for the project came from my inability to do amazing 3D art; I am not an artist, so I essentially just clicked the "Create Teapot" button in Blender.

## About Open-Source
I want this project to be widely available, modifiable, and fun for both casual and advanced users.
I hosted it on GitHub so that people can play, learn from, and tweak this game to their heart's content.
The only thing I ask is that my name be attributed in any clones of the game. I worked hard on this project and would like to be
credited for it.
Also, feel free to shoot me an email about a modification or project you build from it! It would make me happy to see this game evolve into something new and cool!
