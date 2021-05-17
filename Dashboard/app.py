 #this file contains code for FLASK app connected with MySQL

## Import start
from flask import Flask,render_template,url_for,request,redirect
import mysql.connector
import re
import pandas as pd
import matlab.engine
from datetime import datetime
#---Import end---


# strating matlab
print("Starting matlab...")
eng = matlab.engine.start_matlab()

# slx for simulink files
simulation_list = eng.what('/Users/yuganthadiyal/Documents/MATLAB')['slx']

config = {
  'host':"localhost",
  'user':"root",
  'password':"#Include76002",
  'database' : 'simulation'
}


print("Connecting with database...")
mydb = mysql.connector.connect(**config)

mycursor = mydb.cursor()

tables= None

app = Flask(__name__)


@app.route("/", methods = ['GET'])
def home():
	global tables,mycursor,simulation_list

	mycursor.execute("SHOW TABLES;")
	tables = [x[0] for x in mycursor.fetchall()]

	
	return render_template('index.html',tables=tables,simulation_list=simulation_list)

@app.route("/selected_item",methods=['POST'])
def selected_item():

	global tables,mycursor,simulation_list,selected_value

	meta = {}
	dummy = {"a":"a","b":"b"}

	selected_value = request.form['selected']

	if len(tables)>0:
		if selected_value in tables:
			table_name = selected_value
			df = pd.read_sql("select * from "+str(table_name)+";", mydb)
		elif selected_value in simulation_list:
			df = pd.DataFrame(dummy,index=[0])

	else:
		df = pd.DataFrame(dummy,index=[0])

	


	meta['Dimensions'] = str(df.shape[0])+" x "+str(df.shape[1])+" (rows x columns)" + ", total: "+ str(df.shape[0]*df.shape[1])+" (cells)"
	meta['Columns'] = ",".join(list(df.columns))
	meta['File Name'] = 'Blah'
	meta = pd.DataFrame(meta,index=[0]).T.to_html(header=False)

	html = df.head().to_html(index=False)

	temp = ["Sim"+str(i) for i in range(5)]

	des = df.describe().to_html()

	return render_template('data.html',title=selected_value,lista = temp,data = html,meta=meta,describe=des)

@app.route("/selected_simulation",methods=['POST'])
def selected_simulation():

	global selected_value,mycursor,eng



	if request.form['selected'] == 'back':

		return home()

	elif request.form['selected'] == 'run':

		stamp = "_"+datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

		eng.sim(selected_value)
		# code to run the simulation named "request.form['selected']"
		return "simulation running"
	else:

		# search for the historical data in MySQL
		return "searching database"


@app.route("/configure",methods=['POST'])
def configure():

	

	mycursor.execute("SHOW Databases;")

	dbs = [x[0] for x in mycursor.fetchall()]

	dbs.remove(config['database'])

	return render_template('configure.html',dbs = dbs,config=config)

@app.route("/config_response",methods=['POST'])
def config_response():


	global mydb,mycursor,tables

	if request.form['selected']=='cancel':
		return home() 

	name = request.form['database']
	print(name)

	if name == mydb.database:
		print("No database change")
		return render_template('index.html',simulation_list=tables)
	else:

		global config

		config['database']=request.form['database']

		mydb.close()
		mycursor.close()
		mydb = mysql.connector.connect(**config)

		mycursor = mydb.cursor()


	mycursor.execute("SHOW TABLES;")
	tables = [x[0] for x in mycursor.fetchall()]


	return redirect(url_for("home", tables=tables))


if __name__ == '__main__':
	app.run(debug=True)