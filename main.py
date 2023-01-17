from typing import Union
from fastapi import FastAPI
import http3
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://shovon.me",
    "http://localhost:3000",
    "https://diu-cgpa.shovon.me"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = http3.AsyncClient()

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


async def call_api(id: str, semester: str):
    r = await client.get("http://software.diu.edu.bd:8189/result?grecaptcha=&semesterId="+semester+"&studentId="+id, headers=headers, verify=False)
    return r


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/info")
async def student_info(id: str):
    params = {
        'studentId': id,
    }
    response = requests.get('http://software.diu.edu.bd:8189/result/studentInfo',
                            params=params, headers=headers, verify=False)
    data = response.json()
    return data


@app.get("/result")
async def semester_info(semester: str, id: str):
    params = {
        'grecaptcha': '',
        'semesterId': semester,
        'studentId': id,
    }
    response = requests.get('http://software.diu.edu.bd:8189/result',
                            params=params, headers=headers, verify=False)
    data = response.json()
    return data


@app.post("/full")
async def full_result(id: str):
    params = {
        'studentId': id,
    }
    response = requests.get('http://software.diu.edu.bd:8189/result/studentInfo',
                            params=params, headers=headers, verify=False)
    studentInfo = response.json()
    startSemester = int(studentInfo["semesterId"])
    studentInfoObj = {
        'name': studentInfo["studentName"],
        'id': studentInfo["semesterId"],
        'program': studentInfo["progShortName"],
        'batch': studentInfo["batchNo"],
        'department': studentInfo["deptShortName"],
        'faculty': studentInfo["facShortName"],
        'campus': studentInfo["campusName"],
        'shift': studentInfo["shift"],
    }
    semesterResults = []
    drop = 0
    while(startSemester):
        if (int(str(startSemester)[-1]) in (1, 2, 3)):
            if(drop > 1):
                break
            response = await call_api(id, str(startSemester))
            try:
                json_data = response.json()
            except:
                pass
            if (json_data):
                semesterResults.append(json_data)
            else:
                drop = drop + 1
        startSemester = startSemester+1

    data = [studentInfoObj, semesterResults]
    return data
