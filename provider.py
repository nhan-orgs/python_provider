import socketio
sio = socketio.Client()
provider_id = "PYTHON-CLIENT-SAMPLE"

def double_me_handle(input):
    return input*2

def math_add_handle(input):
    return input["x"]+input["y"]


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
    if data["cmd"] == "double_me":
        result = double_me_handle(data["data"])
        sio.emit("provider_reply", {
            **data,
            "result": result
        })
        return
    if data["cmd"] == "math_add":
        result = double_me_handle(data["data"])
        sio.emit("provider_reply", {
            **data,
            "result": result
        })
        return
    sio.emit("provider_reply", {
            **data,
            "result": f"cmd {data['cmd']} is not supported"
        })

if __name__ == '__main__':
    sio.connect('https://bridge.digitalauto.tech')
    sio.wait()