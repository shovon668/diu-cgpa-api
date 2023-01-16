from flask import Flask
from flask import request
import requests

app = Flask("DIU-CGPA Backend")


@app.route('/', methods=['GET'])
def handle_root():
    return ("Web backend running")


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'http://studentportal.diu.edu.bd',
    'Referer': 'http://studentportal.diu.edu.bd/',
    'User-Agent': 'Mozilla/5.0',
    'dnt': '1',
    'sec-gpc': '1',
}


@app.route('/info', methods=['GET'])
def handle_info():
    id = str(request.args.get('id'))  # ?id=1212

    params = {
        'studentId': id,
    }
    response = requests.get('http://software.diu.edu.bd:8189/result/studentInfo',
                            params=params, headers=headers, verify=False)
    data = response.json()
    return data


@app.route('/result', methods=['GET'])
def handle_result():
    id = str(request.args.get('id'))
    semester = str(request.args.get('semester'))
    params = {
        'grecaptcha': '',
        'semesterId': semester,
        'studentId': id,
    }
    response = requests.get('http://software.diu.edu.bd:8189/result',
                            params=params, headers=headers, verify=False)
    data = response.json()
    return data
