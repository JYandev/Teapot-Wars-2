# This file contains configuration defaults for both Panda3d
#  and the game itself. Users will be able to modify some of these in-game and
#  have them persist to the next play-session.

# --- [Display Config] ---
window-title Teapot Wars 2
#fullscreen #t
win-size 1080 720
#win-size 1920 1080
show-frame-rate-meter true
#Prevent user from resizing window at run-time:
win-fixed-size 1

# --- [Networking Config] ---
default-port 9099
max-backlog 1000
tcp-header-size 4

# --- [Debug Config] ---
#TODO REMOVE ALL
direct-gui-edit False
