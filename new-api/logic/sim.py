import redis
import uuid
import rom
import time
import rom.util
import os

rom.util.CONNECTION = redis.Redis(host="localhost", port="6379", db=7)
ROOT = os.getcwd()


class Sim(rom.Model):
    simId = rom.Text(required=True, unique=True, default=str(
        uuid.uuid4()), index=True, keygen=rom.IDENTITY_CI)
    name = rom.Text(required=True)
    user = rom.Text(required=True,  index=True, keygen=rom.FULL_TEXT)
    created_at = rom.Float(default=time.time)
    fileId = rom.Text(required=True)


class File(rom.Model):
    fileId = rom.Text(required=True, unique=True, default=str(
        uuid.uuid4()), index=True, keygen=rom.IDENTITY_CI)
    name = rom.Text(required=True)
    content = rom.Text(default="")


class SimManager(object):
    def createNewSim(self, name, user):
        file = File(name=name)
        file.save()

        sim = Sim(name=name, user=user, fileId=file.fileId)
        sim.save()
        return sim.to_dict()

    def cloneSim(self, cloneId, name, user):
        sim = Sim.get_by(simId=cloneId)
        file = File.get_by(fileId=sim.fileId)

        newFile = File(name=name)
        newFile.save()

        newSim = Sim(name=name, user=user, fileId=newFile.fileId)
        newSim.save()
        return newSim.to_dict()

    def createFromExample(self, example, name, user):
        path = "%s/examples/%s" % (ROOT, example)
        content = open(path).read()
        
        file = File(name=name, content=content)
        file.save()

        sim = Sim(name=name, user=user, fileId=file.fileId)
        sim.save()
        return sim.to_dict()

    def getAllSims(self, uid):
        sims = Sim.get_by(user=uid)
        return [sim.to_dict() for sim in sims]

    def saveSimFile(self, simId, user, content):
        sim = Sim.get_by(simId=simId)
        file = File.get_by(fileId=sim.fileId)
        file.content = content
        file.save()

    def loadSimFile(self, simId, user):
        sim = Sim.get_by(simId=simId)
        file = File.get_by(fileId=sim.fileId)
        return file.content