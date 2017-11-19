from objects.characterClass.Classes import *
"""
    Python file containing static paths.
    Used by: "from objects/defaultConfig.StaticPaths import *
    Images, models, etc. are stored in public static variables here.
"""

# === [Networking] ===
HOST_MAX_BACKLOG = 1000
CLIENT_TIMEOUT = 3000 # 3 Seconds

# === ===

# === [User Interface] ===
UI_WINDOW = "objects/mainMenu/UIContainer.png"
PIERCEROMAN_FONT = "objects/mainMenu/PierceRoman.otf"
PIERCEROMAN_OFFSET_MC = (0, -0.03)

# --- (Join Party Options) ---
JOPTS_CONTROL_TOP_MARGIN = 0.2
JOPTS_CONTROL_SPACING = 0.3
JOPTS_CONTROL_HEIGHT = 0.2
# --- ---

# --- (Class Picker) ---
CPKR_CONTROL_TOP_MARGIN = 0.031
CPKR_CONTROL_SIDES_MARGIN = 0.04
CPKR_TITLE_HEIGHT_RATIO = 0.1
CPKR_INFO_HEIGHT_RATIO = 0.2
CPKR_PIERCEROMAN_OFFSET_TC = (0, -0.11)
CPKR_PIERCEROMAN_OFFSET_TL = (-0.7, -0.07)
CPKR_INFO_WRAP_DEFAULT = 19
CPKR_INFO_FONT_SIZE_DEFAULT = (0.075, 0.075)
# Represented in a grid:
CPKR_CLASSES_LIST = [
[(Barbarian, "objects/characterClass/icons/BarbarianIcon.png"),
 (BaseClass, "objects/characterClass/icons/WizardIcon.png")],
[(Barbarian, "objects/characterClass/icons/BarbarianIcon.png")]
                    ]
CPKR_BUTTONCONTAINER_MARGIN = 0.1
CPKR_BUTTONCONTAINER_WIDTH_PERCENTAGE = 0.7
# --- ---

# --- (Name Picker) ---
NPKR_WIDTH_PERCENTAGE = 0.5 # In terms of screen width
NPKR_HEIGHT_PERCENTAGE = 0.1 # In terms of screen height
NPKR_ENTRY_WIDTH_PERCENTAGE = 0.6 # How long compared to confirm button.
NPKR_ENTRY_FONT_SIZE = (0.075, 0.075)
NPKR_ENTRY_INITIAL_TEXT = "Enter Name"
NPKR_ENTRY_FONT_OFFSET = (0, -0.03)
# --- ---

#=== ===

# === [Camera] ===
TILEMAP_ORBITER_HEIGHT = 5
TILEMAP_ORBITER_SPEED = 0.25
TILEMAP_ORBITER_MIN_INTERVAL = 3
TILEMAP_ORBITER_MAX_INTERVAL = 5
TILEMAP_ORBITER_MIN_VERTICAL_ANGLE = 1
TILEMAP_ORBITER_MAX_VERTICAL_ANGLE = 1.5
TILEMAP_ORBITER_MIN_DIST = 6
TILEMAP_ORBITER_MAX_DIST = 20
# === ===
