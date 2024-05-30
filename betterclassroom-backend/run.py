from app.main import app
import eventlet.wsgi

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
