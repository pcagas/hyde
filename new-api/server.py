#!/usr/bin/env python

r"""Hyde: Server for static website.

   _______     ___
+ 6 @ |||| # P ||| +

"""

from flask import Flask
from flask import jsonify
import os
import bokeh
import json
import postgkyl as pg
from flask_cors import CORS
from flask import request, json
from logic.user import UserManager
from logic.sim import SimManager


userManager = UserManager()
simManager = SimManager()

app = Flask(__name__)
# CORS enabled so react frontend can pull data from python backend
CORS(app)

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + error,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

##
# Top-level entry point
##
@app.route('/')
def index():
    return "Welcome to Gkeyll!"

@app.route("/api/sims/create", methods=['POST'])
def createSimulation():
    """creates a simulation and returns its id
    """
    # fileName = request.json['fileName']
    name = request.json['name']
    uid = "userid"
    sim = simManager.createNewSim(name, uid)
    return json.dumps({'id': sim['simId']})

@app.route("/api/sims")
def getSims():
    uid = "userid"
    sims = simManager.getAllSims(uid)
    return json.dumps({'sims': sims})

@app.route("/api/sims/clone", methods=['POST'])
def cloneSimulation():
    """creates a simulation and returns its id
    """
    simId = request.json['simId']
    name = request.json['name']
    uid = "userid"
    
    newSim = simManager.cloneSim(simId, name, uid)
    return json.dumps({'id': newSim['simId']})


@app.route("/api/sims/createExample", methods=['POST'])
def createExampleSimulation():
    """creates a simulation and returns its id
    """
    example = request.json['example']
    name = request.json['name']
    uid = "userid"
    try:
        sim = simManager.createFromExample(example, name, uid)

        ret = jsonify({'id': sim['simId']})
        ret.status_code = 200
        return ret
    except FileNotFoundError:
        return not_found(error=("%s not found" % example))


@app.route("/api/sim/<simId>/save", methods=['POST'])
def saveSim(simId):
    content = request.json['content']
    uid = "userid"
    sim = simManager.saveSimFile(simId, uid, content)

    ret = jsonify({})
    ret.status_code = 200
    return ret


@app.route("/api/sim/<simId>/load")
def loadFile(simId):
    uid = "userid"
    file = simManager.loadSimFile(simId, uid)

    ret = jsonify({'content': file})
    ret.status_code = 200
    return ret

# @app.route("/api/sim/<id>/start", methods=['POST'])
# def startSim():
#     return "Ok"

# @app.route("/api/sim/<id>/stop", methods=['POST'])
# def stopSim():
#     return "Ok"

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)

