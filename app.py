
# imports
from sklearn.cluster import KMeans
import pandas as pd
import plotly.express as px
from numpy import random
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request, redirect, url_for, send_file
import base64
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import time
from flaskwebgui import FlaskUI 
from sklearn.ensemble import IsolationForest




app = Flask(__name__)
#ui = FlaskUI(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#cache = Cache()
#cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['SESSION_COOKIE_SECURE'] = False

# In[19]:
global resp, df, urls, xy, display, k_means


@app.route('/')
def hello_world():
    global resp
    resp = {}
    # When "submit" button is clicked, 
    # print order of names to console,
    # then reorder python names list and render_template.
    return render_template('index.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

    global resp, df, urls,xy, display
    urls = []
    if request.method == 'POST':
        f = request.files['file']
       
        resp['cols'] = list(pd.read_excel(f).columns)
        df = pd.read_excel(f)
    
    resp['ops'] = ['KMeans','IsolationForest']
    display = 0

    #return redirect(url_for('hello_world'))
    return render_template('data.html',resp = resp,display=display)


@app.route('/graph', methods = ['GET', 'POST'])
def graph():
    global resp, df, urls, xy, k_means

    f = None
    if request.method == 'POST':
        f = request.form.to_dict()


    xy = list(f.values())[:-1]

    if f['op'] == 'KMeans':
        lab = KMeans(n_clusters=len(xy), random_state=0).fit_predict(df[xy])

    if f['op'] == 'IsolationForest':
        lab = IsolationForest(random_state=0).fit(df[xy]).predict(df[xy])


    resp['sel'] = f['op']
    df['labels'] = pd.Series(lab)

    display = 1
    return render_template('data.html',resp = resp,display = display)


@app.route('/plt0')
def plt0():
   
    global xy,df

    plt.figure(figsize=(14,7))
    plt.xlabel("Index")
    plt.ylabel("Values")
    plt.plot(df[xy[0]],'--',label=xy[0])
    plt.plot(df[xy[1]],'--',label=xy[1])
    plt.legend(loc="upper left")
    
    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    figfile.seek(0)  # rewind to beginning of file
    plt.clf()
    plt.close()
    time.sleep(1)
    return send_file(figfile,mimetype='img/png')

@app.route('/plt1')
def plt1():
   
    global xy,df

    col_data = []

    for each in list(set(df['labels'])):
        col_data.append(df[df['labels']==each])

    
    fig, axs = plt.subplots(len(xy),1,figsize=(14,9), sharex='all', sharey='all')
    plt.xlabel("Index")
    plt.ylabel("Values")
    
    labs = list(set(df['labels']))

    c = 0

    if resp['sel'] == resp['ops'][0]:
        cond = 1
    elif resp['sel'] == resp['ops'][1]:
        cond = -1


    for row,x in zip(axs,xy):

        for data in col_data:
                
            if list(data['labels'])[0]== cond:    
                row.plot(data[x],'*',color='#AAAAAA',label='Fault '+xy[c],alpha=0.1)
            else:
                row.plot(data[x],'--',color='C'+str(c),label='Normal '+xy[c])
        
        c+=1
        
        row.legend(loc="upper left")        

    
    figfile = BytesIO()
    plt.savefig(figfile,format='png',dpi=1000)
    figfile.seek(0)  # rewind to beginning of file
    plt.clf()
    plt.close()
    return send_file(figfile,mimetype='img/png')

@app.route('/plt2')
def plt2():
   
    global xy,df

    plt.figure(figsize=(14,7))
    colors = []
    data = df
    for x in list(data.index):
        
        if data.iloc[x][-1] == 0:
            colors.append("blue")
        else:
            colors.append("green")
        
    plt.scatter(df[xy[0]],df[xy[1]],c=colors,alpha=0.5)
    plt.xlabel(xy[0])
    plt.ylabel(xy[1])

    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    figfile.seek(0)  # rewind to beginning of file
    plt.clf()
    plt.close()
    time.sleep(1)
    return send_file(figfile,mimetype='img/png')




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    #ui.run()


# In[ ]:





# In[ ]:




