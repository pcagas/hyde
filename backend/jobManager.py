import hyde
from hyde.lib.Sim import SimManager
from hyde.lib.Sim import Sim
from hyde.lib.User import User
#import postgkyl as pg

from fireworks import Firework, Workflow, LaunchPad, ScriptTask, PyTask, FileWriteTask, FWorker
from fireworks.core.rocket_launcher import rapidfire, launch_rocket
from fireworks.features.multi_launcher import launch_multiprocess, rapidfire_process, ping_multilaunch, start_rockets, split_node_lists
from fireworks.scripts.qlaunch_run import qlaunch, do_launch

import os
import uuid
import re
import matplotlib.pyplot as plt

import redis
import sys
import multiprocessing

#from fireworks.flask_site.app import app
class jobManager(object):
    def __init__(self):
        self.client = redis.Redis()
        self.WF = WFlowBuilder()
        self.userID=''
        self.simID=''
        self.rerun= False
        
    def start_job(self, inpSim, userID):
        self.WF.addRunSteps(inpSim, userID)
        self.WF.slurm_launch()

    def process_request(self):
        ps = self.client.pubsub()
        ps.subscribe('guest')
        
        simBool = False
        userBool = False
        for response in ps.listen():
            print('listening')
            if userBool == True and response['data'] is not None:
                self.userID = response['data'].decode('ascii')
                userBool = False
                print('user processed')

            if simBool == True and userBool == False and response['data'] is not None:
                self.simID = response['data'].decode('ascii')
                inpSim = Sim(self.simID)
                userId = self.userID
                p1 = multiprocessing.Process(target=jobManager.start_job, args=(self, self.simID, userId))
                p1.start()
                simBool = False
                print('sim processed')

            if response['data'] == b'user':
                userBool = True
                print('user flag recieved')
           
            if response['data'] == b'run':
                simBool = True
                print('run order recieved')
                
class WFlowBuilder(object):

    #This class builds and submits workflow(s) for a particular job submission
     
    def __init__(self):

        self.simManager = SimManager()
        self.launchpad = LaunchPad()
        self.ids = []
        self.fws = []
        self.last = 0
        self.rerun = False
     
    def addRunSteps(self, inpSim, userID):
        #builds the following workflow for running simulations
        #creates directory for simulation using the sim name and uuid
        #writes gkyl input file to the directory
        #runs file in the directory
        #if run is successful, prints 'Done', if not, prints 'Failed
        #plots task

        #userid --> for folder location
        self.fws = []
        print(inpSim)
        self.last=len(self.launchpad.get_fw_ids())
#        for fwork in self.launchpad.get_fw_ids():
#            self.launchpad.delete_fws([fwork])       
        sim = Sim(inpSim)

        ncores=str(1)

        path = '/home/adaniel99/gkylsoft/sims/'+str(userID)+'/'+inpSim+'/'
        n = 0
        for f in os.listdir('/home/adaniel99/gkylsoft/sims/'):
            if f==str(userID):
                for f in os.listdir('/home/adaniel99/gkylsoft/sims/'+str(userID)+'/'):
                    if f == inpSim:
                        n=n+1
                        self.rerun=True
          
        if n ==0:
            desttask = ScriptTask.from_str('mkdir ' + path)
            writetask = FileWriteTask({'files_to_write': ([{'filename': sim.name(), 'contents': sim.inpFile()}]), 'dest': path})
            runtask = ScriptTask.from_str('redis-cli PUBLISH ' + User(userID).name()+'2 "Running Simulation"; gkyl ' + path+sim.name())
            runFlag = ScriptTask.from_str('redis-cli PUBLISH '+User(userID).name()+'2'+ ' Done')
            deleteFail = ScriptTask.from_str('lpad defuse_fws -i ' + str(6+self.last))
            flagFail  = ScriptTask.from_str('redis-cli PUBLISH '+User(userID).name()+'2' + ' Failed')
            self.ids.clear()
            dest = Firework(desttask, name= 'Make Folder', fw_id=1+self.last)
            self.ids.append(1+self.last)
            write = Firework(writetask, name= 'Write', fw_id=2+self.last)
            self.ids.append(2+self.last)
            run = Firework(runtask, name='Run', fw_id=3+self.last)
            self.ids.append(3+self.last)
            flag1 = Firework(runFlag, name='done?', fw_id=4+self.last)
            self.ids.append(4+self.last)
            delfail = Firework(deleteFail, name='remove fail flag', fw_id=5+self.last)
            self.ids.append(5+self.last)
            failflag = Firework(flagFail, name='fail flag', fw_id=6+self.last)
            self.ids.append(6+self.last)

            self.fws.append(dest)
            self.fws.append(write)
            self.fws.append(run)
            self.fws.append(flag1)
            self.fws.append(delfail)
            self.fws.append(failflag)
            wf = Workflow(self.fws, {dest: [write], write: [run], run: [flag1], flag1: [delfail]}, name = 'Running '+sim.name())
            self.launchpad.add_wf(wf)
            
        if n ==1:
            writetask = FileWriteTask({'files_to_write': ([{'filename': sim.name(), 'contents': sim.inpFile()}]), 'dest': path})
            runtask = ScriptTask.from_str('redis-cli PUBLISH '+User(userID).name()+'2 "Running Simulation"; gkyl ' + path+sim.name())
            runFlag = ScriptTask.from_str('redis-cli PUBLISH '+ User(userID).name()+'2'+ ' Done')
            deleteFail = ScriptTask.from_str('lpad defuse_fws -i ' + str(5+self.last))
            flagFail  = ScriptTask.from_str('redis-cli PUBLISH '+ User(userID).name()+'2' + ' Failed')
            self.ids.clear()
            write = Firework(writetask, name= 'Write', fw_id=1+self.last)
            self.ids.append(1+self.last)
            run = Firework(runtask, name='Run', fw_id=2+self.last)
            self.ids.append(2+self.last)
            flag1 = Firework(runFlag, name='done?', fw_id=3+self.last)
            self.ids.append(3+self.last)
            delfail = Firework(deleteFail, name='remove fail flag', fw_id=4+self.last)
            self.ids.append(4+self.last)
            failflag = Firework(flagFail, name='fail flag', fw_id=5+self.last)
            self.ids.append(5+self.last)
            wf = Workflow([write, run, flag1, delfail, failflag], {write: [run], run: [flag1], flag1: [delfail]}, name = 'Running '+sim.name())
            self.launchpad.add_wf(wf)

    def runAll(self):
        for i in self.ids:
            launch_rocket(self.launchpad, self.worker, fw_id=i)      
    def runParallel(self):
        #test
        #launch two jobs simultaneously (2, one on each core)
        launch_multiprocess(self.launchpad, self.worker, 'INFO', 0, 2, 10)

    def getFWs(self):
        fws1 = []
        for ids in self.ids:
            fws1.append[self.launchpad.get_fw_by_id(ids)]
        self.fws = fws1
        return self.fws
    
    def slurm_launch(self):
        print("slurm_launch method")
        if self.rerun==True:
            print(self.launchpad.get_fw_ids())
            print(self.rerun)
            for i in self.ids:
                #os.system('salloc --core-spec=1 --time=5 --partition=VME lpad rerun_fws -i '+str(i))
                os.system('salloc --core-spec=1 --time=5 --partition=VME rlaunch singleshot -f '+ str(i))
        if self.rerun==False:
            print(self.launchpad.get_fw_ids())
            print(self.rerun)
            for i in self.ids:
                os.system('salloc --core-spec=1 --time=5 --partition=VME rlaunch singleshot -f '+ str(i))
    def simStates(self):
        #gets current state (str) for each firework in the queue
        #states: ('READY', 'WAITING', 'RUNNING', or 'COMPLETE')
        
        state = []
        for fWs in self.fws:
            state.append(fWs.state())
        return state
