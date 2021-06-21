from flask import Flask, render_template, request, redirect, url_for, send_file
import matlab.engine
import pandas as pd
import json
from random import uniform,randint


application = Flask(__name__)

global eng,model,combinations,fault_index
fault_index = 0

model='latest_ex_9_bus_PMU'
print('matlab starting',end='\r')
eng = matlab.engine.start_matlab()
print('loading the simulink model in the system',end='\r')
eng.eval("load_system('{}')".format(model))
store_path = "./"


# creating combinations of the all possible falut types and removing ABC as it resembeles ABCG or vice versa
def combinations_gen():
    fault_types = ["'FaultA'","'FaultB'","'FaultC'","'GroundFault'"]
    combinations = []

    x = len(fault_types)     

    for i in range(1 << x):
        if len([fault_types[j] for j in range(x) if (i & (1 << j))])>=2:
            combinations.append([fault_types[j] for j in range(x) if (i & (1 << j))])

    
    return combinations[:3]+combinations[4:]

combinations = combinations_gen()

def fault_selector(selection):
    global combinations,fault_index

    if selection<11:
        fault_index += 1
    elif selection==11:
        fault_index = 0

    return combinations[fault_index]



@application.route('/data')
def test_generate():
    global eng,model,combinations,fault_index
    

    time = randint(1,2)

    flush = "set_param('latest_ex_9_bus_PMU/Three-Phase Fault1',{})".format(",0,".join(combinations[-1])+',0')

    print("Setting up...",end='\r')
    eng.eval(flush,nargout=0)


    each = fault_selector(fault_index)


    start_time = str(uniform(0.0, time) + uniform(0.0, time)/10)

    end_time = '0'

    while float(end_time) < float(start_time):
        end_time = str(uniform(0.0, time) + uniform(0.0, time)/10)

    occr_time = "'[" + start_time + " " + end_time+ "]'"
    new_setup = "set_param('latest_ex_9_bus_PMU/Three-Phase Fault1','SwitchTimes',{},{})".format(occr_time,",1,".join(each)+',1')

    
    eng.eval(new_setup,nargout=0)
    print("New setup ready...",end='\r')
    eng.workspace['data'] = eng.sim(model)

    print('Stopping',end='\r')

    
    name = "csvwrite("+"'"+store_path+"ml_test.csv',data.mux_data.Data)"

    print("Success: ",name,"\n\n",end='\r')
    eng.eval(name,nargout=0)

    data = pd.read_csv('ml_test.csv')
    data = data[data.columns[:3]]
    
    response = {}
    response['data'] = json.loads(data.to_json(orient='records'))

    return response


if __name__ == '__main__':
    application.run(host='0.0.0.0',port=5001,debug=False)
















