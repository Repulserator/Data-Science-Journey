from celery import Celery

# Create a Celery instance
app = Celery('zerodha', broker='zmq://localhost:5555')

# Define your Celery tasks
@app.task
def add(x, y):
    return x + y
