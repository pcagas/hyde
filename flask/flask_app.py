from flask import Flask, render_template, url_for, request,redirect
import os
import hyde


app = Flask(__name__)

um = hyde.UserManager()
sm = hyde.SimManager()
guest = um.createNewUser("guest", "guest", "guest@gmail.gov", "127.0.0.5")

@app.route('/')
def main():
    r""" main page. ask users to choose following options
    1. Add : add a new simulation -> name, input file required
    2. Example:
    3. Delete: 
    """
    editing_sim_list = list(sm.getSimsInState('editing'))#returns a list of simulation ids with the state of 'editing'
    return render_template('index.html', simulation=[(simId,hyde.Sim(simId)) for simId in editing_sim_list])
 
@app.route("/sim", methods=['GET','POST'])
def sim(sim=None):
    r"""Add a new simulation from the beginning or through a template"""
    editing_sim_list = list(sm.getSimsInState('editing'))
    id_value = request.args.get('id') 
    #get simulation id from html GET HTTP method.
    selectedSim = "" if id_value == None else [(simIdFound,hyde.Sim(simIdFound)) for simIdFound in editing_sim_list if simIdFound == f'{id_value}'][0]
    # if a user wants to create a new simulation, selectedSim -> blank
    # otherwise, selectedSim -> (sim id, sim object)
    return render_template('sim.html', selectedSim=selectedSim, simulation=[(simId,hyde.Sim(simId)) for simId in editing_sim_list])

    
@app.route("/adding", methods=['POST'])
def adding():
    """adding a new simulation/modifying a new simulation"""
    editing_sim_list = list(sm.getSimsInState('editing'))
    id_value = request.json["id"]# retrieve sim id, name and input file from add.html
    name = request.json["name"]
    inpFile = request.json['inpFile']
    newSim = [(simIdFound,hyde.Sim(simIdFound)) for simIdFound in editing_sim_list if simIdFound == f'{id_value}']#returns list with tuple of simId, sim object
    if (len(newSim) > 0): #if there is a simulation object to be modified, update it
        hyde.Sim(newSim[0][0]).rename(name)
        hyde.Sim(newSim[0][0]).updateInpFile(inpFile)
    else:# if the simulation is something that hasn't made, create a new one
        sm.createNewSim(name, guest.userId, inpFile)

    return {"path": url_for('main')}
