import os
import onnx
import numpy as np
import zipfile

def get_layer_info(onionPath = '', uid = ''):


    if onionPath == '' or uid == '':
        return '' # return empty string on error
    
    model = onnx.load(onionPath)
    
    inits = []
    for init in model.graph.initializer :
        inits.append(init)

    weights_bias = len(inits)

    layerdim = []
    for i in range(0, weights_bias):
        if i == weights_bias - 1:
            #print(inits[i].dims[0])
            layerdim.append(inits[i].dims[0])
        elif i % 2 == 0:
            #print(inits[i].dims[0])
            layerdim.append(inits[i].dims[0])


    return layerdim