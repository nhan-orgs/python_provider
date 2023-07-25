import socketio
sio = socketio.Client()
provider_id = "PYTHON-CLIENT-SAMPLE"

import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque

def detect_function(data):
    print("detect_function")
    return "result"


@sio.event
def connect():
    print('connected to server')
    sio.emit("register_provider", {
        "provider_id": provider_id,
        "name": "Face Angle Detection"
    });

@sio.event
def new_request(data):
    print('new_request')
    if data["cmd"] == "detect-face":
        result = detect_function(data["data"])
        sio.emit("provider_reply", {
            **data,
            "result": result
        })
    else:
        sio.emit("provider_reply", {
            **data,
            "result": f"cmd {data['cmd']} is not supported"
        })

@sio.event
def disconnect():
    print('disconnected from server')


@sio.event
def hello(a):
    print("Receive message from server")


if __name__ == '__main__':
    sio.connect('http://localhost:3091')
    sio.wait()