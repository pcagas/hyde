from flask import Flask, render_template, url_for, request, redirect, Response
import os
import hyde
import redis
from backend import jobManager

app = Flask(__name__)

jobManager = jobManager.jobManager()
um = hyde.UserManager()
sm = hyde.SimManager()
guest = um.createNewUser("guest", "guest", "guest@gmail.gov", "127.0.0.5")
files = sm.getExampleSims()
client = redis.Redis()

def event_stream(user):
    ps = client.pubsub()
    ps.subscribe(user)
    for message in ps.listen():
        print (message)
        if message['type']=='message':
            yield 'data: %s\n\n' % message['data'].decode('utf-8')
            
@app.route('/stream')
def stream():
    return Response(event_stream(guest.name()+'2'), mimetype="text/event-stream")

@app.route('/')
def main():
    r""" main page. ask users to choose following options
    1. Add : add a new simulation
    2. Example: add new simulation from template
    3. Delete: delete simulations from the sidebar/DB
    """
    editing_sim_list = list(sm.getSimsInState('editing'))#returns a list of simulation ids with the state of 'editing'
    return render_template('index.html', simulation=[hyde.Sim(simId) for simId in editing_sim_list])
 
@app.route('/add', methods=['POST','GET'])
def add():
    name_value = request.form.get("example_select")
    print(name_value)

    if name_value is None: # add button
        newSim = sm.createNewSim("New_Simulation", guest.userId, "") #a new sim
    else: # if a user clicks a butoon example and choose one of the example files
        for i in files:
            if name_value == i.name(): 
                newSim = sm.createNewSim(i.name(), guest.userId, i.inpFile())
            #end
        #end
    #end
    return redirect((url_for('sim', simId=newSim.simId)))

@app.route("/sim/<simId>", methods=['GET','POST'])
def sim(simId):
    r"""Add a new simulation from the beginning or through a template"""

    editing_sim_list = list(sm.getSimsInState('editing'))
    id_value = request.args.get('id')#get simulation id from html GET HTTP method.

    for simIdFound in editing_sim_list:
        if id_value is None:
            if simIdFound == simId:
                selectedSim = hyde.Sim(simIdFound)
            #end
        else:
            if simIdFound == f'{id_value}':
                selectedSim = hyde.Sim(simIdFound)
            #end
        #end
    #end

    # if a user wants to create a new simulation, selectedSim -> default name&blank input file
    # otherwise, selectedSim -> sim object
    return render_template('sim.html', selectedSim=selectedSim, simulation=[hyde.Sim(simId) for simId in editing_sim_list])
    
@app.route("/adding", methods=['POST'])
def adding():
    """adding a new simulation/modifying a new simulation"""

    editing_sim_list = list(sm.getSimsInState('editing'))

    id_value = request.json["id"]# retrieve sim id, name and input file from sim.html
    name = request.json["name"]
    print(name)
    inpFile = request.json['inpFile']

    for simIdFound in editing_sim_list:
        if simIdFound == id_value:
            hyde.Sim(simIdFound).rename(name)
            hyde.Sim(simIdFound).updateInpFile(inpFile)
            simId = simIdFound 
        #end
    #end
    return "adding completed"

@app.route("/example")
def example():
    #editing_sim_list = list(sm.getSimsInState('editing'))
    editing_sim_list=list(sm.getExampleSims())
    #return render_template('example.html', example=files, simulation=[hyde.Sim(simId) for simId in editing_sim_list])
    return render_template('example.html', example=files, simulation=files)

@app.route("/deleting", methods=['POST'])
def deleting():
    id_value = request.json['id']
    editing_sim_list = list(sm.getSimsInState('editing'))
    if id_value is not None:
        for simId in editing_sim_list:
            if simId == id_value: 
                sm.removeSim(hyde.Sim(simId))
            #end
        #end
    #end
    return "deleted"

@app.route("/publishing", methods=['POST'])
def publishing():
    id_value = request.json["id"]
    editing_sim_list = list(sm.getSimsInState('editing'))
    if id_value is not None:
        for simId in editing_sim_list:
            if simId == id_value:
                sm.pubSim(guest.name(), 'user')
                sm.pubSim(guest.name(), f'{guest.userId}')
                sm.pubSim(guest.name(), 'run')
                sm.pubSim(guest.name(), f'{simId}')
                sm.pubSim(guest.name()+'2', 'Run Order Sent')
    return "publishing completed"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='5000')
