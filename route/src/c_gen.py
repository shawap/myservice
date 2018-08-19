import os
import onnx
import numpy as np
import zipfile

def c_code_generation(onionPath = '', uid = ''):


    if onionPath == '' or uid == '':
        return '' # return empty string on error
    
    '''
    Below paths are according to route/app.py 
    '''
    nn_tplt = './src/nn_tplt.c'
    nn_head = './src/nn_ONNX2C.h'
    outCode = '../storage/{}/nn_ONNX2C.c'.format(uid)
    outPath = '../storage/{}/{}.zip'.format(uid, uid)
    model = onnx.load(onionPath)
    
    
    inits = []
    for init in model.graph.initializer :
        inits.append(init)

    weights_bias = len(inits)
    # print("weights + bias : {}".format(weights_bias))


    layerdim = []
    for i in range(0, weights_bias):
        if i == weights_bias - 1:
            #print(inits[i].dims[0])
            layerdim.append(inits[i].dims[0])
        elif i % 2 == 0:
            #print(inits[i].dims[0])
            layerdim.append(inits[i].dims[0])

    # print("Structure of each layer : {}".format(layerdim))


    numOfLayer = len(layerdim)
    numOfGap = numOfLayer - 1
    maxLayer = max(layerdim[1:])
    dimOfLayer = str(layerdim).replace('[', '{').replace(']', '}')

    coef = []

    for i in inits:
        coef += (list(i.double_data))

    coef = str(coef).replace('[','{ ').replace(']',' }')

    with open(nn_tplt, 'r') as fp:
        ccode = fp.readlines()

    outputs = ''
    for cline in ccode:
        outputs += cline

    outputs = outputs.format(numOfLayer, numOfGap, maxLayer, '(int [])' + dimOfLayer, coef).replace('lbrace', '{').replace('rbrace', '}')
    with open(outCode, 'w') as fp:
        fp.write(outputs)
    
    with zipfile.ZipFile(outPath, 'w') as zfp:
        zfp.write(nn_head, os.path.basename(nn_head), compress_type = zipfile.ZIP_DEFLATED)
        zfp.write(outCode, os.path.basename(outCode), compress_type = zipfile.ZIP_DEFLATED)
    try:
        os.remove(outCode)
    except:
        pass
    
    return outPath


'''
Notice that all the relative paths are changed according to the app.py,
If you want to test the __main__ function, you have to modify the followings,
    ->  nn_tplt = './src/nn_tplt.c'
    ->  nn_head = './src/nn_ONNX2C.h'
    ->  outCode = '../storage/{}/nn_ONNX2C.c'.format(uid)
    ->  outPath = '../storage/{}/{}.zip'.format(uid, uid)
'''        
if __name__ == "__main__":
    
    c_code_generation('./mnist-perceptron.onnx', 'uid')