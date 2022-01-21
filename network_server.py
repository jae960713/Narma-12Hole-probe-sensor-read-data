# app.py

from flask import Flask, redirect, render_template, make_response, request
from requests.models import Response
import json, requests
import time
import random

app = Flask(__name__)
data_12=[]
data_5=[]
temp_data = [None,None]

@app.route('/live-5hole-data', methods = ['POST', 'GET'])
def send5holedata():
    
    if request.method == 'POST': 
        data = request.get_json()
        response = make_response(json.dumps(data, ensure_ascii = False).encode('utf-8'))
        response.content_type = 'application/json ; charset=utf-8'
        data_5.append(data['data'])
        return response

@app.route('/live-12probe-data', methods = ['POST', 'GET'])
def send12holedata():
    
    if request.method == 'POST': 
        data = request.get_json()
        response = make_response(json.dumps(data, ensure_ascii = False).encode('utf-8'))
        response.content_type = 'application/json ; charset=utf-8'
        data_12.append(data['data'])
        return response

@app.route('/get-temp-data', methods = ['GET'])
def get_data():
    d = []
    if request.method == 'GET':
        print(temp_data[0])
        d = [time.time()*1000, temp_data[0]]
        response = make_response(json.dumps(d))

        response.content_type = 'application/json'
        print(response.json)
        return response
       
    
@app.route('/live-temp-data', methods = ['POST','GET'])
def live_data():
    if request.method == 'POST':
        data = request.get_json()

    if(temp_data[0] == None):

        temp_data[0] = float(data['temp'])

    elif(temp_data[0] != None):

        temp_data[1] =  float(data['temp'])
        temp_data[0] = temp_data[1]
 
    response = make_response(json.dumps(temp_data[0], ensure_ascii = False).encode('utf-8'))
    response.content_type = 'application/json ; charset=utf-8'
    return response

@app.route('/mainwin_12')
def show12holedata():

    return render_template('datastream.html', data = data_12)

@app.route('/mainwin_5')
def show5holedata():

    return render_template('datastream.html', data = data_5)

@app.route('/mainwin_temp',methods = ['POST', 'GET'])
def showtempdata():
    return render_template('index.html')
    
@app.route('/')
def mainwindow():
         
    return "server connected"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
