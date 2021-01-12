
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





app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#cache = Cache()
#cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['SESSION_COOKIE_SECURE'] = False

# In[19]:
global cols, df, urls, xy, display, k_means


@app.route('/')
def hello_world():
    # When "submit" button is clicked, 
    # print order of names to console,
    # then reorder python names list and render_template.
    return render_template('index.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

    global cols, df, urls,xy, display
    urls = []
    if request.method == 'POST':
        f = request.files['file']
       
        cols = list(pd.read_excel(f).columns)
        df = pd.read_excel(f)
    
    display = 0

    #return redirect(url_for('hello_world'))
    return render_template('data.html',cols = cols,display=display)


@app.route('/graph', methods = ['GET', 'POST'])
def graph():
    global cols, df, urls, xy, k_means

    f = None
    if request.method == 'POST':
        f = request.form.to_dict()


    xy = list(f.values())

    k_means = KMeans(n_clusters=len(xy), random_state=0).fit_predict(df[xy])
    df['labels'] = pd.Series(k_means)

    display = 1
    return render_template('data.html',cols = cols,display = display)


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
    temp1 = df[df['labels']==1]
    temp0 = df[df['labels']==0]

    
    fig, axs = plt.subplots(2,1,figsize=(14,9), sharex='all', sharey='all')
    plt.xlabel("Index")
    plt.ylabel("Values")
    c = 0
    for row in axs:
        row.plot(temp1[xy[c]],'*',color='#AAAAAA',label='Fault '+xy[c])
        row.plot(temp0[xy[c]],'--',color='C'+str(c),label='Normal '+xy[c])
        row.legend(loc="upper left")
        c+=1

    
    figfile = BytesIO()
    plt.savefig(figfile,format='png',dpi=1000)
    figfile.seek(0)  # rewind to beginning of file
    plt.clf()
    plt.close()
    return send_file(figfile,mimetype='img/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


# In[ ]:





# In[ ]:




