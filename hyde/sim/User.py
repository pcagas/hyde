"""Hyde: User management and storage.

Data for users is stored in Redis. Users are identified by a userId, a
32-character UUID. Each user belongs to either 'guest', 'regular' or
'super' user groups. Guest user accounts are temporary and are removed
periodically.

The following information is stored. Here, uid is the UUID for a given
user.

- users : Set of userIds in the system
- usergroup:guest : Set of all guest users
- usergroup:regular : Set of all regular users
- usergroup:super : Set of all super users

- user:uid : hash with {name, group, dateCreated}
- user:uid:runningsims : set of sim IDs that are currently running
- user:uid:pendingsims : set of sim IDs that are pending
- user:uid:completedsims : set of sim IDs that are completed

   _______     ___
+ 6 @ |||| # P ||| +

"""

import os
import uuid
import redis
import datetime
import hyde.config
import hyde.sim.utils

# Global configuration information
conf = hyde.config.hydeConfig

class UserManager(object):
    r"""User management interface
    """
    
    def __init__(self):
        self.rHandle = redis.Redis(host=conf.redisServer, port=conf.redisPort)
    
    def createNewUser(self, name):
        r"""createNewUser(name : str) -> User object
        """

        group = "regular"
        userId = uuid.uuid4().hex
    
        self.rHandle.sadd('users', userId)
        if name == "guest":
            group = "guest"
            self.rHandle.sadd('usergroup:guest', userId)
        else:
            self.rHandle.sadd('usergroup:regular', userId)
    
        self.rHandle.hmset(f'user:{userId}', {
            'name' : name,
            'group' : group,
            'dateCreated' : datetime.datetime.now().isoformat()
        })

        # create user directory
        userDir = conf.simRoot+"/"+userId
        os.mkdir(userDir)
        
        return User(userId)
    
    def getUsers(self):
        return hyde.sim.utils.convertToStrSet(
            self.rHandle.smembers("users")
        )

    def getUsersInGroup(self, group):
        return hyde.sim.utils.convertToStrSet(
            self.rHandle.smembers(f"usergroup:{group}")
        )

class User(object):
    """Information about a user.
    """
    
    def __init__(self, userId):
        self.userId = userId
        self.rHandle = redis.Redis(host=conf.redisServer, port=conf.redisPort)

    def name(self):
        userId = self.userId
        v = self.rHandle.hget(f'user:{userId}', 'name')
        return v.decode('utf-8')

    def group(self):
        userId = self.userId
        v = self.rHandle.hget(f'user:{userId}', 'group')
        return v.decode('utf-8')

    def dateCreated(self):
        userId = self.userId
        v = self.rHandle.hget(f'user:{userId}', 'dateCreated')
        return v.decode('utf-8')

    def simList(self, state):
        userId = self.userId
        return hyde.sim.utils.convertToStrSet(
            self.rHandle.smembers(f"user:{userId}:{state}")
        )
