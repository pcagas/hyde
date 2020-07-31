from flask import Flask, render_template, url_for, request,redirect
import os
import hyde
from backend import jobManager

app = Flask(__name__)

jobManager.jobManager()

path = '/home/hjk6281/2020_Internship/hyde'
os.chdir(path)
files = []

for f in os.listdir(path):
    if f.endswith(".lua"):
        files.append(os.path.splitext(f)[0])
    #end
#end

um = hyde.UserManager()
sm = hyde.SimManager()
guest = um.createNewUser("guest", "guest", "guest@gmail.gov", "127.0.0.5")

@app.route('/')
def main():
    r""" main page. ask users to choose following options
    1. Add : add a new simulation
    2. Example: add new simulation from template
    3. Delete: 
    """
    editing_sim_list = list(sm.getSimsInState('editing'))#returns a list of simulation ids with the state of 'editing'
    return render_template('index.html', simulation=[hyde.Sim(simId) for simId in editing_sim_list])
 
@app.route('/add', methods=['POST','GET'])
def add():
    name_value = request.form.get("example_select")

    if name_value is None:
        newSim = sm.createNewSim("New Simulation", guest.userId, "")
    else:
        for i in files:
            if name_value == i: 
                newSim = sm.createNewSim(name_value, guest.userId, open(f'{name_value}.lua').read())
            #end
        #end
    #end

    # return {"path" : url_for("sim")}
    return redirect("172.23.60.54{}".format(url_for('sim', simId=newSim.simId)))

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
    inpFile = request.json['inpFile']

    for simIdFound in editing_sim_list:
        if simIdFound == id_value:
            hyde.Sim(simIdFound).rename(name)
            hyde.Sim(simIdFound).updateInpFile(inpFile) 
        #end
    #end

    return redirect("http://172.23.60.54{}".format(url_for('sim', simId=simId)))

@app.route("/example")
def example():
    editing_sim_list = list(sm.getSimsInState('editing'))
    return render_template('example.html', example=files, simulation=[hyde.Sim(simId) for simId in editing_sim_list])

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
    return "http://172.23.60.54"

@app.route("/publishing", method=['POST'])
def publishing():
    id_value = request.json["id"]
    editing_sim_list = list(sm.getSimsInState('editing'))
    if id_value is not None:
        for simId in editing_sim_list:
            if simId == id_value:
                sm.pubSim(guest.name(), 'run')
                jobManager.process_request(guest,hyde.Sim(simId))
    return redirect("172.23.60.54{}".format(url_for('sim', simId=newSim.simId)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port='5000')