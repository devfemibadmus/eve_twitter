from flask import Flask
import threading
import time

app = Flask(__name__)

# def background_task():
#    while True:
#        print("Background task running...")
#        time.sleep(900)

# def myapp():
#    if not hasattr(app, "background_thread_started"):
#        thread = threading.Thread(target=background_task, daemon=True)
#        thread.start()
#        app.background_thread_started = True
#    return app

# application = myapp()

@app.route("/")
def home():
    return "Background task is running!"


