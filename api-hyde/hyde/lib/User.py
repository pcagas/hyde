r"""Hyde: User management and storage.

Data for users is stored in Redis. Users are identified by a userId, a
32-character UUID. Each user belongs to either 'guest', 'regular' or
'super' user groups. Guest user accounts are temporary and are removed
periodically.

The following information is stored. Here, uid is the UUID for a given
user.

- users : Set of userIds in the system (except deleted users)
- usergroup:guest : Set of all guest users
- usergroup:regular : Set of all regular users
- usergroup:super : Set of all super users
- usergroup:deleted : Set of all deleted users

- user:uid : hash with {name, username, email, group, dateCreated, ip}
- user:uid:editing : set of sim IDs that are editing
- user:uid:running : set of sim IDs that are currently running
- user:uid:completed : set of sim IDs that are completed

There are an additional set of simulations:

- user:uid:template : These are simulations marked by user as template

A template simulation can be copied to create other simulations.

   _______     ___
+ 6 @ |||| # P ||| +

"""

import os
import uuid
import redis
import datetime
import hyde.config
import hyde.lib.utils

# Global configuration information
conf = hyde.config.hydeConfig

class UserManager(object):
    r"""User management interface
    """
    
    def __init__(self):
        self.rHandle = redis.Redis(host=conf.redisServer, port=conf.redisPort)
    
    def createNewUser(self, name, username, email, ipAddress, ugroup=None):
        r"""createNewUser(name : str) -> User object
        """

        group = "regular"
        if name == "guest":
            group = "guest"
        if ugroup:
            group = ugroup

        userId = uuid.uuid4().hex
        self.rHandle.sadd('users', userId)

        self.rHandle.sadd(f'usergroup:{group}', userId)
        self.rHandle.hmset(f'user:{userId}', {
            'name' : name,
            'group' : group,
            'username' : username,
            'email' : email,
            'ipAddress' : ipAddress,
            'dateCreated' : datetime.datetime.now().isoformat()
        })

        # create user directory
        userDir = conf.simRoot+"/"+userId
        os.mkdir(userDir)
        
        return User(userId)
    
    def getUsers(self):
        return hyde.lib.utils.convertToStrSet(
            self.rHandle.smembers("users")
        )

    def removeUser(self, userId):
        if self.rHandle.sismember('users', userId):
            group = self.rHandle.hget(f'user:{userId}', 'group').decode('utf-8')
            if group in ['guest', 'regular', 'super']:
                # just mark user as 'deleted'. Full cleanup can't be
                # done here to avoid issues with running/queued jobs
                self.rHandle.srem(f'usergroup:{group}', userId)
                self.rHandle.hset(f'user:{userId}', 'group', 'deleted')
                self.rHandle.sadd('usergroup:deleted', userId)
            # remove from list of users
            self.rHandle.srem('users', userId)

    def getUsersInGroup(self, group):
        r"""group is one of 'guest', 'regular', 'super'
        """
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

    def ipAddress(self):
        userId = self.userId
        v = self.rHandle.hget(f'user:{userId}', 'ip')
        return v.decode('utf-8')

    def rename(self, newName):
        userId = self.userId
        self.rHandle.hset(f'user:{userId}', 'name', newName)
        return self

    def simList(self, state):
        r"""state is one of 'editing', 'running', 'completed'
        """
        userId = self.userId
        return hyde.lib.utils.convertToStrSet(
            self.rHandle.smembers(f"user:{userId}:{state}")
        )
