from flask import Flask, render_template, url_for, request,redirect
import os
import hyde


app = Flask(__name__)

path = '/Users/user/2020_Internship/hyde'
os.chdir(path)
files = []
for f in os.listdir(path):
    if f.endswith(".lua"):
        files.append(os.path.splitext(f)[0])

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
    return render_template('index.html', simulation=[hyde.Sim(simId) for simId in editing_sim_list])
 
@app.route('/add', methods=['POST','GET'])
def add():
    name_value = request.form.get("example_select") #two_stream
    if name_value is not None:
        for i in files:
            if name_value == i: 
                newSim = sm.createNewSim(name_value, guest.userId, open(name_value+".lua").read())
    else:
        newSim = sm.createNewSim("New Simulation", guest.userId, "")
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
        else:
            if simIdFound == f'{id_value}':
                selectedSim = hyde.Sim(simIdFound)      
    # if a user wants to create a new simulation, selectedSim -> default name&blank input file
    # otherwise, selectedSim -> sim object
    return render_template('sim.html', selectedSim=selectedSim, simulation=[hyde.Sim(simId) for simId in editing_sim_list])

    
@app.route("/adding", methods=['POST'])
def adding():
    """adding a new simulation/modifying a new simulation"""
    editing_sim_list = list(sm.getSimsInState('editing'))
    id_value = request.json["id"]# retrieve sim id, name and input file from sim.html
    name = request.json["name"]
    inpFile = request.json['inpFile']
    for simIdFound in editing_sim_list:
        if simIdFound == id_value:
            hyde.Sim(simIdFound).rename(name)
            hyde.Sim(simIdFound).updateInpFile(inpFile)

    return {"path": url_for('main')}

@app.route("/example")
def example():
    editing_sim_list = list(sm.getSimsInState('editing'))
    return render_template('example.html', example=files)
