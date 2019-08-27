# Teapot-Wars-2
A Python Panda3D video game project I am building for CMU's 15-112 and beyond!

Note: the instructions below are for development only. If you are looking just
to play the game, see "releases." (Currently not available)

## About
In its current state, Teapot Wars 2 features a multiplayer game mode where
players must compete to defeat AI and retrieve a Legendary Bag of Tea. The
first player to defeat an AI opponent and retrieve the item will win the game,
displaying a message to all other players connected.

Features:
* Three classes with descriptions that are cool but do nothing.
* Name, health, and stamina systems which display to other connected players.
* AI with ranged-based vision that will pathfind to the players to fight them.
* Player-versus-player
* Main-menu, instructions, death, failure, respawn timer, and victory screens.
* Enemies drop items. The only implemented item however is the Legendary Bag of
Tea. The drop rate is 100% to speed up demos.

## Prerequisites:
- Python 3.6 with pip (I used Miniconda and conda env).
- Git

## Getting it Running:
First, open a command prompt.
`git clone` the project if you haven't already.
Then `cd` into the root and type `pip install -r requirements.txt`

Also, the project requires my PyBSP Dungeon Generator. To set it up, `cd` into the root folder of Teapot-Wars-2 and type `mkdir external`. `cd` into external and `git clone https://github.com/JYandev/PyBSP_Dungeon_Generator.git`

Assuming you change back to the root folder, we are now ready to run `python main.py` to start up the game!
