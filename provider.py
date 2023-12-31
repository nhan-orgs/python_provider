import socketio
import asyncio
sio = socketio.Client()
provider_id = "PYTHON-CLIENT-SAMPLE"

def double_me_handle(input):
    return input*2

async def simulate_run():
    global sio
    for i in range(0, 10):
        await asyncio.sleep(1)
        print(f"i: {i}")
        sio.emit("sent_to_my_clients", {
            "provider_id": "PYTHON-CLIENT-SAMPLE",
            "cmd": "showSpeed",
            "data": i
        });

@sio.event
def connect():
    print('connected to server')
    sio.emit("register_provider", {
        "provider_id": provider_id,
        "name": "Sample provider"
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
    if data["cmd"] == "Start":
        sio.emit("provider_reply", {
            **data,
            "result": "Staring..."
        })
        asyncio.run(simulate_run())
        return
    sio.emit("provider_reply", {
            **data,
            "result": f"cmd {data['cmd']} is not supported"
        })

if __name__ == '__main__':
    sio.connect('https://bridge.digitalauto.tech')
    sio.wait()