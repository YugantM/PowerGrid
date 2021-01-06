#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, request, redirect, url_for


# In[2]:


import pandas as pd


# In[10]:


from flask_caching import Cache


# In[18]:


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#cache = Cache()
#cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['SESSION_COOKIE_SECURE'] = False

# In[19]:


@app.route('/')
def hello_world():
    # When "submit" button is clicked, 
    # print order of names to console,
    # then reorder python names list and render_template.
    return render_template('index.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
       
        cols = list(pd.read_excel(f).columns)
    

    #return redirect(url_for('hello_world'))
    return render_template('data.html',cols = cols)


# In[ ]:


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


# In[ ]:





# In[ ]:




