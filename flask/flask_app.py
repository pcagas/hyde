from flask import Flask, render_template, url_for, request, redirect, Response, json
import bokeh
import os
import hyde
import redis
from backend import jobManager
import postgkyl as pg

app = Flask(__name__)

jobManager = jobManager.jobManager()
um = hyde.UserManager()
sm = hyde.SimManager()
guest = um.createNewUser("guest", "guest", "guest@gmail.gov", "127.0.0.5")
files = sm.getExampleSims()
client = redis.Redis()
post_files = []
folder = ''
new_plot=[]

def event_stream(user):
    #user is a string representing the name of the redis pubsub channel
    #the name will correspond to the user running the simulation
    #second user channel meant for displaying workflow status on webpage
    ps = client.pubsub()
    ps.subscribe(user)
    for message in ps.listen():
        print (message)
        if message['type']=='message':
            yield 'data: %s\n\n' % message['data'].decode('utf-8')
#@app.route('/login', methods=['GET','POST'])
#def login():
#    if request.method == 'POST':
#            
#    return render_template('login.html')
#
@app.route('/stream')
def stream():
    #event stream input second channel
    return Response(event_stream(guest.name()+'2'), mimetype="text/event-stream")
#@app.route('/user/')
#def profile(user):
#        return
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
    return render_template('sim.html', selectedSim=selectedSim, sid = simId, simulation=[hyde.Sim(simId) for simId in editing_sim_list])
    
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
    print("publishing flag")
    return "publishing completed"
#@app.route("/sim/<simId>/plot")
@app.route('/sim/<simId>/plot', methods=['GET','POST'])
def pladd(simId):
    print("flag")
    folder = '/home/adaniel99/gkylsoft/sims/'+guest.userId+'/'+simId+'/'
    names = []
    for file in os.listdir(folder):
        if file.endswith(".bp"):
            names.append(file)
            post_files.append(file)

    return render_template('plist.html', plot_files=post_files, iD=simId)

@app.route("/sim/<simId>/plot/display", methods=["GET","POST"])
def plot(simId):
    pfile = request.form.get("plot_form")
    folder = '/home/adaniel99/gkylsoft/sims/'+guest.userId+'/'+simId+'/'
    print(post_files)
    print(guest.userId)
    new_plot.append(folder+pfile)
    return render_template('plot.html')
@app.route('/plot1',methods=["GET","POST"])
def plot1():
    #data = pg.GData('/home/adaniel99/gkyl/Regression/vm-two-stream/p1/rt-two-stream-p1_elc_0.bp')
    data = pg.GData(new_plot[len(new_plot)-1])
    fig = pg.output.blot(data)
    output = json.dumps(bokeh.embed.json_item(fig))
    return output

if __name__ == '__main__':
    app.run(host="0.0.0.0", port='5000')
