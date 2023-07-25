import socketio
sio = socketio.Client()
provider_id = "PYTHON-CLIENT-SAMPLE"

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

if __name__ == '__main__':
    sio.connect('http://localhost:3091')
    sio.wait()