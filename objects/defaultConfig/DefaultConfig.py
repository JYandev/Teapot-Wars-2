"""
    Python file for default configurations.
    Used in case the Config.prc file has been corrupt or is misplaced.
    Default game settings are set here!
"""
# All variables made public-static for easy access:

#TODO Look into creating a PRC_DIR default (COMPILE-TIME PRC!!!)

# --- [Networking] ---
DEFAULT_PORT = 9099
DEFAULT_MAX_BACKLOG = 1000
DEFAULT_IP_ADDRESS = "127.0.0.1"

def resetConfigToDefaults ():
    """
        Resets the Config.prc file to the default settings contained here.
        If that file does not exist, creates a new one.
    """
    print ("resetConfigToDefaults Unimplemented!") #TODO
