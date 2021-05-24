import numpy as np
import os
from matplotlib import pyplot as plt
import cv2
import math
import pandas as pd
import pickle
import time
#import tensorflow as tf
from CNN_ModelMaker import Sequential , Dense , Flatten,ReLU , Softmax
from IPython.display import Image
import threading


def loadModel(fileName) :
    f = open(fileName, 'rb') 
    model = pickle.load(f)
    return model

def loadModel_Tf(fileName) :
    return tf.keras.models.load_model(fileName)

#fileName = 'Traffic_Signs_Detection_3.obj' 
#model = loadModel(fileName)

Labels = ['Speed limit (30kmph)', 'Speed limit (60kmph)',
          'Stop', 'Turn right ahead', 'Turn left ahead' ,
          'Negative']

def ROI(img,pos=[0,0,100,100],kernels=[75],stride=5,Model=None) : # [X1 , Y1 , X2 , Y2] ROI for Object Detection
    ROIs = []
    Locs = []
    ratios = [(1,1),(1,1.5),(1.5,1),(2,2)]#,(2,2.5),(2.5,2)]
    for ratio in ratios :
        for x in range(pos[0],pos[2]-kernels[0]+stride,stride) :
            for y in range(pos[1],pos[3]-kernels[0]+stride,stride) :
                a,b,c,d = x,y,int(x+kernels[0]*ratio[0]),int(y+kernels[0]*ratio[1])
                if ( c >= 0 and c <= 150 ) and (c >= 0 and c <= 150) :
                    Locs.append([a,b,c,d])
                    #im = cv2.resize(img[b:d,a:c],(model.input_shape[1],model.input_shape[2]))
                    im = cv2.resize(img[b:d,a:c],(Model.input_shape[0],
                                                  Model.input_shape[1]))
                    ROIs.append(im)
                    
    ROIs = np.array(ROIs)/255.
    preds = Model.predict(ROIs)
    return Locs,preds

def DetectLoc(image,model,best=99.9) :
    Locs,preds = ROI(img=image,Model=model)
    max_ = 75
    ind = 0
    for i in range(len(preds)) :
        k = preds[i].ravel() * 100
        if max_ <= k[np.argmax(k)] :
            max_ = k[np.argmax(k)]
            ind = i
    for ind_,(i,j) in enumerate(zip(preds,Locs)) :
        if ind_ == ind :
            if max_ > best :
                arg = np.argmax(i)
                if arg == 5 :
                    return None
                return (Labels[arg],j[0],j[1],j[2],j[3])
                    
    return None

#t1 = threading.Thread(target=CamView.show)
#t1.start()
