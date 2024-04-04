from flask import Flask, jsonify, request

from remote_storage import remote_storage
from worker import init_workers, stop_workers, storage_lock, task_queue

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit_numbers():
    numbers = request.get_json().get("numbers")
    if not all(1 <= num <= 99 for num in numbers):
        return "Numbers must be in the range [1, 99].", 400

    task_queue.put(numbers)
    return jsonify({"message": "Numbers submitted successfully."})


@app.route("/result", methods=["GET"])
def get_result():
    with storage_lock:
        current_sum = remote_storage["sum"]
    return jsonify({"sum": current_sum})


if __name__ == "__main__":
    init_workers()
    try:
        app.run(debug=True)
    finally:
        stop_workers()
