"""Hyde: Simulation management.

Metadata for simulations is stored in Redis, while the simulation
output is stored on disk. Each sim is identified by a simId, a
32-character UUID.

The following information is stored. Here, did is the UUID for a given
simulation.

- sims:running : Set of running simulations
- sims:queued : Set of queued simulations
- sims:pending : Set of pending simulations
- sims:completed : Set of completed simulations

- sim:uid : hash with {name, userID, inpFile, dateCreated, dateEdited}

Note that complete text of input file is stored in the sim:uid hash
table.

Sims IDs are also added to the user's appropriate simulation lists.

   _______     ___
+ 6 @ |||| # P ||| +

"""

import uuid
import redis
import datetime
import hyde.config
import hyde.sim.utils

# Global configuration information
conf = hyde.config.hydeConfig

class SimManager(object):
    r"""Simulation management interface
    """
    
    def __init__(self):
        self.rHandle = redis.Redis(host=conf.redisServer, port=conf.redisPort)
    
    def createNewSim(self, name, userId, inpFile):
        r"""createNewSim(name : str, userId : str, inpFile : str) -> Sim object

        name : Name of simulation
        userId : User ID of user creating simulation
        inpFile : String with input file
        """

        if not self.rHandle.sismember(f'users', userId):
            # do not create simulation if user does not exist
            return None

        group = "pending"
        simId = uuid.uuid4().hex

        now = datetime.datetime.now().isoformat()
    
        self.rHandle.sadd('sims:pending', simId)
        self.rHandle.sadd(f'user:{userId}:pending', simId)
        self.rHandle.hmset(f'sim:{simId}', {
            'name' : name,
            'userId' : userId,
            'inpFile' : inpFile,
            'dateCreated' : now,
            'dateEdited' : now
        })
        
        return Sim(simId)

class Sim(object):
    """Control object for simulation.
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
        if self.rHandle.sismember(f'user:{userId}:pending', simId):
            # only allow editing files in 'pending' state
            self.rHandle.hset(f'sim:{simId}', 'inpFile', inpFile)
            self.rHandle.hset(f'sim:{simId}', 'dateEdited', datetime.datetime.now().isoformat())
            
        return self
