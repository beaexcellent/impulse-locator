import sys
sys.path.append("/srv/impulse")
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time

from event_queue import event_queue

## Import the shared event queue from the receiver
#from receiver.udp_listener import event_queue

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

def forward_events():
    """Background thread: forward events from queue to Socket.IO clients."""
    while True:
        event = event_queue.get()
        socketio.emit("event", event)

def start_forwarder():
    t = threading.Thread(target=forward_events, daemon=True)
    t.start()

if __name__ == "__main__":
    start_forwarder()
    socketio.run(app, host="0.0.0.0", port=8000, allow_unsafe_werkzeug=True)