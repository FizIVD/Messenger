from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
        <title>Mess</title>
    </head>
    <body>
        <h1 align="middle">Simple echo Messenger</h1>
        <form action="" onsubmit="sendMessage(event)" align="middle">
            <input type="json" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <dl id='messages' align="middle">
        </dl>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var data = JSON.parse(event.data)
                console.log(data)
                if(data.text){
                var messages = document.getElementById('messages')
                var message = document.createElement('dt')
                var content = document.createTextNode(data.text)
                var content_num = document.createTextNode(data.mess_num)
                var sep = document.createTextNode(' : ')
                message.appendChild(content_num)
                message.appendChild(sep)
                message.appendChild(content)
                messages.appendChild(message)
                }
                else {
                alert( "Не посылайте пустой текст" )
                }
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var to_json = JSON.stringify({text: input.value})
                ws.send(to_json)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class Counter:

    def __init__(self):
        self._counter = 0

    def reset(self):
        print("Yea")
        self._counter = 0
        return

    def inc(self):
        self._counter += 1
        return self._counter


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    counter = Counter()
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data["text"] != "":
                payload = {"mess_num": counter.inc(), "text": data["text"]}
                await websocket.send_json(payload)
            else:
                await websocket.send_json({})
    except WebSocketDisconnect:
        counter.reset()
