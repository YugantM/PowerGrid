#this file contains code for FLASK app connected with MySQL

from flask import Flask,render_template,url_for,request

app = Flask(__name__)


@app.route("/")
def home():

	temp = ["Tile item: "+str(i) for i in range(100)]
	return render_template('index.html',simulation_list=temp)

@app.route("/selected_item",methods=['POST'])
def selected_item():

	print(request.form['selected'])

	temp = ["Sim"+str(i) for i in range(5)]

	return render_template('data.html',title=request.form['selected'],lista = temp)

@app.route("/selected_simulation",methods=['POST'])
def selected_simulation():

	if request.form['selected'] == 'back':

		return home()

	elif request.form['selected'] == 'run':

		# code to run the simulation named "request.form['selected']"
		return "simulation running"
	else:

		# search for the historical data in MySQL
		return "searching database"




if __name__ == '__main__':
	app.run(debug=True)