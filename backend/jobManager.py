import hyde
from hyde.lib.Sim import SimManager
from hyde.lib.Sim import Sim
from hyde.lib.User import User
import postgkyl as pg

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

#from fireworks.flask_site.app import app
class jobManager(object):
    def __init__(self):
        self.client = redis.Redis()
        self.WF = WFlowBuilder()
        
    #def listen(self, user):
        #self.client.pubsub().subscribe(user.name())
        #self.client.pubsub().listen()
        
    def process_request(self, user, inpSim):
        ps = self.client.pubsub()
        ps.subscribe(user.name())
        for response in ps.listen():
            if response['data'] == b'run':
                self.client.publish(user.name(), 'message received')
                print('STARTING JOB')
                self.start_job(user, inpSim)
        
    def start_job(self, user, inpSim):
        self.WF.addRunSteps(user, inpSim)
        self.WF.slurm_launch()
        
class WFlowBuilder(object):

    #This class builds and submits workflow(s) for a particular job submission
     
    def __init__(self):

        self.simManager = SimManager()
        #self.mainDir = '/home/adaniel99/hyde/backend/hydeSims/'
        self.worker = FWorker(name='myWorker')
        self.launchpad = LaunchPad()
        self.ids = []
        self.fws = []
        self.last = 0
        #self.queue1 = [[self.simManager.getExampleSims()[0], self.simManager.getExampleSims()[1]], [1, 1]]
     
    def addRunSteps(self, user, inpSim):
        #builds the following workflow for running simulations
        #creates directory for simulation using the sim name and uuid
        #writes gkyl input file to the directory
        #runs file in the directory
        #if run is successful, prints 'Done', if not, prints 'Failed
        #plots task

        #userid --> for folder location
        
        self.last=len(self.launchpad.get_fw_ids())
        i = index

        new_id = str(uuid.uuid4())
            
        #ncores = str(self.queue1[1][i]) 
        #path = self.mainDir+'_'+new_id+'/'
        #print(path)
        path = '/home/adaniel99/gkylsoft/sims/'+str(user.userID)+'/'
        
        #print(path+re.sub('.lua', '_elc_0.bp', self.queue1[0][i].name()))

        desttask = ScriptTask.from_str('mkdir ' + path)
        writetask = FileWriteTask({'files_to_write': ([{'filename': inpSim.name(), 'contents': inpSim.inpFile()}]), 'dest': path})
        runtask = ScriptTask.from_str('mpiexec -n '+ ncores + ' gkyl ' + path+inpSim.name())

        runFlag = ScriptTask.from_str('redis-cli PUBLISH Daniel_1 Done')
        deleteFail = ScriptTask.from_str('lpad defuse_fws -i ' + str(7+self.last))
        flagFail  = ScriptTask.from_str('Failed')
            
        plottask = ScriptTask.from_str('pgkyl -f '+ path+re.sub('.lua', '_elc_0.bp', inpSim.name()) + ' plot')

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
        plot = Firework(plottask, name='plot', fw_id=6+self.last)
        self.ids.append(6+self.last)
        failflag = Firework(flagFail, name='fail flag', fw_id=7+self.last)
        self.ids.append(7+self.last)

        
        self.fws.append(dest)
        self.fws.append(write)
        self.fws.append(run)
        self.fws.append(flag1)
        self.fws.append(delfail)
        self.fws.append(failflag)
        self.fws.append(plot)

        print(self.ids)
        wf = Workflow([dest, write, run, flag1, delfail, failflag, plot], {dest: [write], write: [run], run: [flag1], flag1: [delfail], delfail: [plot]}, name = 'Running '+self.queue1[0][i].name()+'_'+ncores)
        self.launchpad.add_wf(wf)
        
    def addFullQueue(self):

        for Sim in self.queue1:
            self.addRunSteps()
            
    def rerun0(self):
        self.launchpad.rerun_fw(self.ids[self.queue1[0][0].name()+' run'])
        launch_rocket(self.launchpad, self.worker)
        
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
    
    def overload(self):
        #for testing multiple simultaneous runs
        

        task1 = ScriptTask.from_str('gkyl /home/adaniel99/gkyl/Regression/vm-two-stream/p1/rt-two-stream-p1.lua')
        task2 = ScriptTask.from_str('gkyl /home/adaniel99/gkyl/Regression/vm-two-stream/p2/rt-two-stream-p2.lua')

        run1 = Firework(task1, name = 'run1')
        run2 = Firework(task2, name = 'run2')
        run3 = Firework(task1, name = 'run3')
        run4 = Firework(task1, name = 'run4')
        run5 = Firework(task1, name = 'run5')
        run6 = Firework(task1, name = 'run6')
        run7 = Firework(task1, name = 'run7')
        run8 = Firework(task1, name = 'run8')
        run9 = Firework(task1, name = 'run9')

        self.launchpad.add_wf(run1)
        #self.launchpad.add_wf(run2)
        #self.launchpad.add_wf(run3)
        #self.launchpad.add_wf(run4)
        #self.launchpad.add_wf(run5)
        #self.launchpad.add_wf(run6)
        #self.launchpad.add_wf(run7)
        #self.launchpad.add_wf(run8)
        #self.launchpad.add_wf(run9)

        #launch_multiprocess(self.launchpad, self.worker, 'INFO', 1, 2, 1)

    def slurm_launch(self):
        #submit job to SLURM; will be launched upon reaching the front of the queue

        for i in self.ids:
            #os.system('qlaunch -q /home/dalex_99/HYDEPROJECT/my_qadapter.yaml singleshot')
            #os.system('srun --ntasks=1 --cpus-per-task=1 rlaunch singleshot -f '+ str(i))
            os.system('salloc --tasks=1 --core-spec=1 --time=5 --partition=xps rlaunch singleshot -f '+ str(i))
              
    def simStates(self):
        #gets current state (str) for each firework in the queue
        #states: ('READY', 'WAITING', 'RUNNING', or 'COMPLETE')
        
        state = []
        for fWs in self.fws:
            state.append(fWs.state())
        return state
