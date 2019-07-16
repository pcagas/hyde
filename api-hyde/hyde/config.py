"""Hyde: System-wide configuration.

   _______     ___
+ 6 @ |||| # P ||| +
"""

import json
import os

class Config(object):
    r"""Stores global configuration information to run Hyde
    """
    
    def __init__(self, confFile=None):
        r"""configure(confFile : str)
        
        Configure system using supplied configure file. File must be
        specified with full path.

        """

        self.redisServer = 'localhost' # redis server URL
        self.redisPort = 6379 # redis server port
        self.gkylRoot = os.path.expandvars('$HOME/gkylsoft/gkyl') # gkyl installation
        self.simRoot = os.path.expandvars('$HOME/gkylsoft/sims') # root directory

        # load data from configure file if specified
        if confFile:
            f = open(confFile)
            cvals = json.load(f)

            self.redisServer = cvals["redis-server"]
            self.redisPort = cvals["redis-port"]
            self.gkylRoot = cvals["gkyl-root"]
            self.simRoot = cvals["sim-root"]


# load default configuration
hydeConfig = Config()
def configure(confFile):
    r"""configure(confFile : str)

    Load file to set global configuration
    """
    global hydeConfig
    hydeConfig = Config(confFile)
    
