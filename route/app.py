import os
import re
import json
import uuid
import pathlib
import random
import string
import importlib
from flask_cors import CORS, cross_origin
from flask import Flask, request, send_from_directory, send_file, make_response, render_template, jsonify
from src.c_gen import c_code_generation
from src.get_layer_info import get_layer_info

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods = ['GET', 'POST'])
@cross_origin()
def index():
  if request.method == 'POST':
    return 'Bro, don\'t do that shit.'
  return 'Welcome to our service'



@app.route("/uploadOnion", methods = ['POST'])
@cross_origin()
def uploadOnion(): 

    try:
        f = request.files['file']
        uid = str(uuid.uuid1())
        dest = '../storage/{}/'.format(uid)
        pathlib.Path(dest).mkdir(parents = True, exist_ok = True)
        f.save(dest + uid + '.onnx')
        struct = get_layer_info(dest + uid + '.onnx', uid)
        return jsonify(stat = 1, uid = uid, layer = struct)

    except:
        return jsonify(stat = 0, msg = 'Something went wrong')



@app.route("/genC", methods = ['get'])
@cross_origin()
def CcodeGenerator():
    uid = request.args.get('uid', None)
    if uid is None:
        return 'Something went wrong'


    dest = '../storage/{}/{}.onnx'.format(uid, uid)
    # genC function should return the address of the zip file
    # , which includes a .c file and a .h file
    zipPath = c_code_generation(dest, uid) # return '' empty string on error

    if zipPath is '':
        return jsonify(stat = 0, msg = 'Zip file doesn\'t exist')
    
    response = make_response(send_file(zipPath, 'application/zip'))
    response.headers['Content-Disposition'] = "attachment; filename=onion-{}.zip".format(uid)
    return response


@app.route("/getWmap", methods = ['get'])
@cross_origin()
def getWmap():
    uid = request.args.get('uuid', None)
    if uid is None:
        pass #return 'Something went wrong'

    '''
    # function genWmap() should return the destination of the wmap.jpg
    wmapPath = genWmap(dest)
    '''
    wmapPath = '../storage/example.png'
    response = make_response(send_file(wmapPath, 'image/png'))
    # response.headers['Content-Disposition'] = "attachment; filename=example.jpg"
    return response




@app.route('/<path:udf>', methods = ['GET', 'POST'])
@cross_origin()
def fallback(udf):
  return 'ehh, don\'t try'


if __name__ == "__main__":

  #app.run(port=5000, debug=True)
  app.run(host='0.0.0.0', port=5006, debug = True)
