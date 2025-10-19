from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
import mouse

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      margin: 0;
      background: black;
      height: 100vh;
      overflow: hidden;
      touch-action: none;
    }
  </style>
</head>
<body>
  <script>
    const ws = new WebSocket(`ws://${window.location.host}/ws`);
    let lastX = 0, lastY = 0, active = false;
    let clickTimeout = null;

    document.body.addEventListener('touchstart', e => {
      if (e.touches.length === 1) {
        active = true;
        const t = e.touches[0];
        lastX = t.clientX;
        lastY = t.clientY;
        clickTimeout = setTimeout(() => clickTimeout = null, 200);
      } else if (e.touches.length === 2) {
        ws.send(JSON.stringify({type: "right_click"}));
      }
    });

    document.body.addEventListener('touchmove', e => {
      if (!active) return;
      const t = e.touches[0];
      let dx = (t.clientX - lastX) * 2;
      let dy = (t.clientY - lastY) * 2;
      lastX = t.clientX;
      lastY = t.clientY;
      ws.send(JSON.stringify({type: "move", dx, dy}));
      e.preventDefault();
    });

    document.body.addEventListener('touchend', e => {
      active = false;
      if (clickTimeout) {
        ws.send(JSON.stringify({type: "click"}));
        clickTimeout = null;
      }
    });
  </script>
</body>
</html>
"""

@app.get("/")
async def get_index():
    return HTMLResponse(content=HTML_PAGE)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            if msg["type"] == "move":
                mouse.move(msg["dx"], msg["dy"], absolute=False)
            elif msg["type"] == "click":
                mouse.click()
            elif msg["type"] == "right_click":
                mouse.right_click()
    except Exception:
        pass
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        http="h11",
        ws="websockets",
        log_config=None,  # <--- disables Uvicorn’s custom logger
        log_level="info"
    )
