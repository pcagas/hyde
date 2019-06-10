"""Hyde: User management and storage.

Data for users is stored in Redis. Users are identified by userIds,
a 32-character UUID. Each user belongs to either 'guest', 'regular' or
'super' user groups. Guest user accounts are temporary and are removed
periodically.

The following information is stored. Here, uid is the UUID for a given
user.

- users : This is a unsorted set of userIds in the system
- usergroup:guest : Set of all guest users
- usergroup:regular : Set of all regular users
- usergroup:super : Set of all super users

- user:uid : hash with keys name, group, datecreated

   _______     ___
+ 6 @ |||| # P ||| +
"""

import uuid
import redis
import datetime
import hyde.config

# Global configuration information
conf = hyde.config.hydeConfig

def _convertToStrSet(byteSet):
    r"""Converts byteSet into a set of strings
    """
    strSet = set()
    for e in byteSet:
        strSet.add(e.decode('utf-8'))
    return strSet

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
    
        rHandle.sadd('users', userId)
        if name == "guest":
            group = "guest"
            self.rHandle.sadd('usergroup:guest', userId)
        else:
            self.rHandle.sadd('usergroup:regular', userId)
    
        self.rHandle.hmset(f'user:{userId}', {
            'name' : name,
            'group' : group,
            'datecreated' : datetime.datetime.now().isoformat()
        })
        
        return User(userId)
    
    def getUsers(self):
        return _convertToStrSet(self.rHandle.smembers("users"))

    def getUsersInGroup(self, group):
        return _convertToStrSet(self.rHandle.smembers(f"usergroup:{group}"))

class User(object):
    """Information about an individual user.
    """
    
    def __init__(self, userId):
        self.userId = userId
        self.rHandle = redis.Redis(host=conf.redisServer, port=conf.redisPort)

    def name(self):
        userId = self.userId
        v = self.rHandle.hmget(f'user:{userId}', 'name')[0]
        return v.decode('utf-8')

    def group(self):
        userId = self.userId
        v = self.rHandle.hmget(f'user:{userId}', 'group')[0]
        return v.decode('utf-8')

    def datecreated(self):
        userId = self.userId
        v = self.rHandle.hmget(f'user:{userId}', 'datecreated')[0]
        return v.decode('utf-8')
