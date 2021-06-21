from sklearn.cluster import KMeans
import pandas as pd
import plotly.express as px
import random
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request, redirect, url_for, send_file,jsonify
import base64
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import time
from keras.models import load_model
from collections import Counter
import numpy as np
import pandas as pd
import requests
from random import uniform,randint
from io import BytesIO
from flask_cors import CORS, cross_origin
from base64 import encodebytes
import json
import imageio
from PIL import Image, ImageDraw, ImageFont



binary_model = load_model('models/range_gru_binary_clf.pkl')
multi_model = load_model('models/range_gru_multi_clf.pkl')




global data,image_counter,dat,temp,maxy,zeroy

data = 0


def plotter(plot_data,unique_labels,n_plots,save=False,number=0,stream=False):
    
    dat = pd.read_csv('ml_test.csv')
    zeroy = sorted(dat[min(dat.columns[:3])])[0]
    maxy = sorted(dat[max(dat.columns[:3])])[-1]
    del dat

    data = plot_data.copy()
    predicted_labels = data['label']
    col_len=6
    #print(len(set(predicted_labels)),unique_labels)
    #print(Counter(predicted_labels).values(),[unique_labels[each] for each in Counter(predicted_labels).keys()])
    
    matrics = sorted(zip([unique_labels[each] for each in Counter(predicted_labels).keys()],Counter(predicted_labels).values() ), key=lambda x: x[1])
    cols = ['A'+str(each+1) for each in range(int(col_len/2))] + ['V'+str(each+1) for each in range(int(col_len/2))]
    score = [list(j) for j in matrics][::-1]
    
    
    
    total = sum([i[1] for i in score])

    c=0
    for i in score:

        score[c][1] = float(round(i[1]*100/total,2))
        
        c+=1

    print(pd.DataFrame.from_records(score,columns=['Fault type','Percentage']))
    y = pd.DataFrame.from_records(score,columns=['Fault_type','Percentage'])
    if 'NML' in list(y.Fault_type):
        
        nml_percent = float(y[y.Fault_type =='NML']['Percentage'])
    else:
        nml_percent = 0
    
    if nml_percent == 100:
        signal_color='green'
    elif nml_percent > 80:
        signal_color='yellow'
    else:
        signal_color='red'
    
    if 'FAULT' in list(y.Fault_type):    
        flt_percent = float(y[y.Fault_type =='FAULT']['Percentage'])
    
        if flt_percent > 60:
            signal_color = 'red'

    
    #print("changing numbers to labels again")
    data['label'] = [unique_labels[i] for i in predicted_labels]

    fig, ax = plt.subplots(n_plots,figsize=(15,4*n_plots))
    canvas = FigureCanvas(fig)
    #plt.ylim(zeroy,maxy)

    for j in range(n_plots):

        legend_list = []
        available_labels = [each[0] for each in score ]
        
        for i in range(len(available_labels)):

            extract = data[data.label==available_labels[i]][cols[j]]    

            if len(unique_labels)==2:
                
                if available_labels[i]=='FAULT':
                    temp = ax[j].scatter(extract.index,extract,marker='+',s=40) 
                elif available_labels[i]=='NML':
                    temp = ax[j].scatter(extract.index,extract,marker='.',s=10) 
            else:
                #print(available_labels[i],score[i][0],score[i][1])
                if available_labels[i]==score[0][0]:
                    temp = ax[j].scatter(extract.index,extract,marker='+',s=40)
                else:
                    temp = ax[j].scatter(extract.index,extract,marker='.',s=10)


            legend_list.append(temp)

        ax[j].legend(legend_list,available_labels,scatterpoints=3,ncol=1,fontsize=15)
        ax[j].set_ylim(zeroy,maxy)

    fig.tight_layout()
    if save:
        #plt.savefig('static/'+str(number)+'.png')
        canvas.draw()  
        image = np.array(canvas.renderer.buffer_rgba())
        #image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        signal = imageio.imread('./'+signal_color+'.png')

        plt.clf()
        plt.close('all')
        return image,signal

    if stream:
        figfile = BytesIO()
        plt.savefig(figfile,format='png',dpi=1000)
        plt.clf()
        plt.close()

        #image_64_encode = base64.encodebytes(figfile)
        #response = {'image': image_64_encode.decode('utf-8')}
        
        #return json.dumps(response)
        return figfile



    return score,0


def tester(model,frame):
    
    data = frame
    col_len=6
    cols = ['A'+str(each+1) for each in range(int(col_len/2))] + ['V'+str(each+1) for each in range(int(col_len/2))]
    
    if data.shape[1]==6:
        data.columns = cols
    elif data.shape[1]==7:
        data.columns = cols + ['label']
        data = data[cols]
    elif data.shape[1]==3:
        data.columns = cols[:3]
    elif data.shape[1]==4:
        data.columns = cols[:3]+['label']
        
    else:
        print("columns length is ",data.shape[1])
    
    #test_preds = model.predict(data)
    if frame.shape[1]<=4:
        tup = 3
    elif frame.shape[1]>=6:
        tup = 6
    test_preds = model.predict(data.values.reshape(-1,1,tup).tolist())
    predicted_labels = np.argmax(test_preds,axis=1)
    
    data['label'] = predicted_labels
    
    return data
    





application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
application.config['SESSION_COOKIE_SECURE'] = False
random.seed()  # Initialize the random number generator



@application.route('/')
def index():
    global data
    data = 10
    return render_template('index.html',data=data)


@application.route('/chart')
def chart_data():
    global data
    binary_labels_list = ['NML','FAULT']
    multi_labels_list = ['AB', 'AC', 'BC','AG', 'BG', 'ABG', 'CG', 'ACG', 'BCG', 'ABCG']
    
    resp = requests.get('http://localhost:5001/data')
    dat = pd.DataFrame(json.loads(resp.text)['data'])
    plt.figure(figsize=(10,5))
    dat = dat[dat.columns[:3]]


    frame_size = 1000
    speed = 100
    start = 0
    end = start+frame_size
    gif = []
    signal_list = []
    fault_list = []
    temp = tester(binary_model,dat.copy())
    for i in range(len(dat)):

        if end>len(dat):
            break

        #print(int(start),int(end))
        #temp = tester(binary_model,dat.iloc[int(start):int(end)].copy())
        
        #print(temp,temp.shape)
        slic = temp.iloc[int(start):int(end)]
        print(slic.shape)
        x,signal = plotter(slic,binary_labels_list,3,True,i)
        

        img = Image.new('RGB', (200, 100), color = (255, 255, 255))
     
        fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 40)
        d = ImageDraw.Draw(img)
        
        if len(slic[slic.label!=0][slic.columns[:3]])>0:
            slic = tester(multi_model,slic[slic.label!=0][slic.columns[:3]])
            #print(temp,temp.shape)
            y,_ = plotter(slic,multi_labels_list,3,False,i)
            #print("y:",y)
            d.text((20,20), y[0][0], font=fnt, fill=(255, 0, 0))
        else:
            d.text((20,20), 'Normal', font=fnt, fill=(0, 255, 0))

        fault_list.append(np.array(img))
        gif.append(x)
        signal_list.append(signal)

        
        del x
        del img
        start=start+speed
        end = start+frame_size
        
        
    dura = 0.9
    imageio.mimsave('static/mygif.gif', gif, format='GIF', duration=dura)
    imageio.mimsave('static/signal.gif', signal_list, format='GIF', duration=dura)
    imageio.mimsave('static/fault.gif', fault_list, format='GIF', duration=dura)
    #with imageio.get_writer(, mode='I') as writer:
        #for each in gif:
            #writer.append_data(each)

    return "done"


if __name__ == '__main__':
    application.run(debug=True)