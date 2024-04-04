from flask import Flask, request, jsonify
from threading import Thread, Lock
import os
import queue

app = Flask(__name__)

# remote KV
result_storage = {"sum": 0}
storage_lock = Lock()

# Task queue
task_queue = queue.Queue()

N_WORKERS = int(os.getenv("N_WORKERS", 3))
workers = []

def worker(worker_id):
    while True:
        numbers = task_queue.get()
        if numbers is None:
            break
        result = sum(numbers)
        with storage_lock:
            result_storage['sum'] += result
        print(f"Worker {worker_id} processed: {result}")

def initiate_workers():
    for worker_id in range(N_WORKERS):
        Thread(target=worker, args=(worker_id,)).start()

def stop_workers():
    for i in range(N_WORKERS):
        task_queue.put(None)
    for t in workers:
        t.join()

@app.route('/submit', methods=['POST'])
def submit_numbers():
    numbers = request.get_json().get('numbers')
    if not all(1 <= num <= 99 for num in numbers):
        return "Numbers must be in the range [1, 99].", 400

    task_queue.put(numbers)
    return jsonify({"message": "Numbers submitted successfully."})

@app.route('/result', methods=['GET'])
def get_result():
    with storage_lock:
        current_sum = result_storage["sum"]
    return jsonify({"sum": current_sum})

if __name__ == '__main__':
    initiate_workers()
    try:
        app.run(debug=True)
    finally:
        stop_workers()

