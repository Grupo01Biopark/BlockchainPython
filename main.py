from app.routes import app
from app.broadcast import broadcast_sync_request, listen_for_broadcast
import threading

if __name__ == "__main__":
    threading.Thread(target=listen_for_broadcast, daemon=True).start()
    broadcast_sync_request()
    app.run(host="0.0.0.0", port=5001)
