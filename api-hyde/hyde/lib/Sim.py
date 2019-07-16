r"""Hyde: Simulation management.

Metadata for simulations is stored in Redis, while the simulation
output is stored on disk. Each sim is identified by a simId, a
32-character UUID.

The following information is stored. Here, did is the UUID for a given
simulation.

- sims:running : Set of running simulations
- sims:queued : Set of queued simulations
- sims:editing : Set of editing simulations
- sims:completed : Set of completed simulations

- sim:uid : hash with {name, userID, inpFile, dateCreated, dateEdited}

Note that complete text of input file is stored in the sim:uid hash
table.

Sims IDs are also added to the user's appropriate simulation lists.

A special set of simulations are marked as "examples":

- sims:examples : Set of sytem provided examples

   _______     ___
+ 6 @ |||| # P ||| +

"""

import datetime
import glob
import hyde.config
import hyde.lib.utils
import ntpath
import redis
import uuid

# Global configuration information
conf = hyde.config.hydeConfig

class SimManager(object):
    r"""Simulation management interface
    """
    
    def __init__(self):
        self.rHandle = redis.Redis(host=conf.redisServer, port=conf.redisPort, decode_responses=True)
    
    def createNewSim(self, name, userId, inpFile):
        r"""createNewSim(name : str, userId : str, inpFile : str) -> Sim object

        name : Name of simulation
        userId : User ID of user creating simulation
        inpFile : String with input file
        """

        simId = uuid.uuid4().hex
        now = datetime.datetime.now().isoformat()
    
        self.rHandle.sadd('sims:editing', simId)
        self.rHandle.sadd(f'user:{userId}:editing', simId)
        self.rHandle.hmset(f'sim:{simId}', {
            'name' : name,
            'userId' : userId,
            'inpFile' : inpFile,
            'dateCreated' : now,
            'dateEdited' : now
        })
        
        return Sim(simId)

    def getAllSims(self):
        sims = []
        for key in self.rHandle.scan_iter("sim:*"):
            sims.append(self.rHandle.hgetall(key))
        return sims

    def createNewTemplateSim(self, sim):
        r"""createNewTemplateSim(sim : Sim) -> Sim

        Create a template simulation from given simulation
        """

        userId = sim.userId
        s = self.createNewSim(sim.name(), userId, sim.inpFile())
        # remove from 'editing' and add to 'template'
        self.rHandle.srem('sims:editing', s.simId)
        self.rHandle.srem(f'user:{userId}:editing', s.simId)
        self.rHandle.sadd(f'user:{userId}:template', s.simId)

        return s

    def _createNewExampleSim(self, exampleFile):
        r"""_createNewExampleSim(exampleFile : str) -> Sim

        Create an example simulation from full path to input file
        """
        
        h, name = ntpath.split(exampleFile)
        inpFile = open(exampleFile).read()

        simId = name # use name as ID for example sims
        now = datetime.datetime.now().isoformat()

        # add simulation to DB
        self.rHandle.hmset(f'sim:{simId}', {
            'name' : name,
            'userId' : '__gkyl__12345$#@__', # one hopes no user has this strange name
            'inpFile' : inpFile,
            'dateCreated' : now,
            'dateEdited' : now
        })
        # add to list of examples
        self.rHandle.sadd('sims:examples', simId)
        
        return Sim(simId)

    def getSimsInState(self, state):
        r"""state is one of 'running', 'editing', 'completed', 'queued'
        """
        return hyde.lib.utils.convertToStrSet(
            self.rHandle.smembers(f"sims:{state}")
        )

    def getExampleSims(self):
        r"""getExampleSims() -> [] Sim

        Returns list of example sim object. This call clears out the
        list and recreates it everytime it is called.

        """
        
        self.rHandle.delete('sims:examples') # remove existing examples
        return [self._createNewExampleSim(f) for f in glob.glob(
            conf.gkylRoot+"/bin/Tool/examples**/*.lua" # files from gkyl/bin/Tool/examples
        )]

class Sim(object):
    """Data container for simulation.
    """
    
    def __init__(self, simId):
        self.simId = simId
        self.rHandle = redis.Redis(host=conf.redisServer, port=conf.redisPort)
        self.userId = self.rHandle.hget(f'sim:{simId}', 'userId').decode('utf-8')

    def name(self):
        simId = self.simId
        v = self.rHandle.hget(f'sim:{simId}', 'name')
        return v.decode('utf-8')

    def dateCreated(self):
        simId = self.simId
        v = self.rHandle.hget(f'sim:{simId}', 'dateCreated')
        return v.decode('utf-8')

    def dateEdited(self):
        simId = self.simId
        v = self.rHandle.hget(f'sim:{simId}', 'dateEdited')
        return v.decode('utf-8')

    def inpFile(self):
        simId = self.simId
        v = self.rHandle.hget(f'sim:{simId}', 'inpFile')
        return v.decode('utf-8')

    def rename(self, name):
        simId = self.simId
        self.rHandle.hset(f'sim:{simId}', 'name', name)
        return self

    def updateInpFile(self, inpFile):
        simId = self.simId
        userId = self.userId
        if self.rHandle.sismember(f'user:{userId}:editing', simId):
            self.rHandle.hset(f'sim:{simId}', 'inpFile', inpFile)
            self.rHandle.hset(f'sim:{simId}', 'dateEdited', datetime.datetime.now().isoformat())
            
        return self
