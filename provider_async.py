import socketio
import asyncio
sio = socketio.AsyncClient()
provider_id = "PYTHON-CLIENT-SAMPLE"

async def double_me_handle(input):
    return input*2

async def simulate_run():
    global sio
    for i in range(0, 10):
        await asyncio.sleep(1)
        print(f"i: {i}")
        await sio.emit("sent_to_my_clients", {
            "provider_id": "PYTHON-CLIENT-SAMPLE",
            "cmd": "showSpeed",
            "data": i
        });

@sio.event
async def connect():
    global sio
    print('connected to server')
    await sio.emit("register_provider", {
        "provider_id": provider_id,
        "name": "Sample provider async"
    });

@sio.event
async def new_request(data):
    global sio
    print('new_request')
    if data["cmd"] == "double_me":
        result = await double_me_handle(data["data"])
        await sio.emit("provider_reply", {
            **data,
            "result": result
        })
        return
    if data["cmd"] == "Start":
        await sio.emit("provider_reply", {
            **data,
            "result": "Staring..."
        })
        await simulate_run()
        return
    await sio.emit("provider_reply", {
            **data,
            "result": f"cmd {data['cmd']} is not supported"
        })

async def connect_to_server():
    global sio
    await sio.connect('https://bridge.digitalauto.tech')
    await sio.wait()

asyncio.run(connect_to_server())