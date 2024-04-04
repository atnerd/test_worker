import os
import queue
from threading import Lock, Thread

from remote_storage import remote_storage

N_WORKERS = int(os.getenv("N_WORKERS", 3))

storage_lock = Lock()

# Task queue
task_queue = queue.Queue()


workers = []


def worker(worker_id):
    while True:
        numbers = task_queue.get()
        if numbers is None:
            break
        result = sum(numbers)
        with storage_lock:
            remote_storage["sum"] += result
        print(f"Worker {worker_id} processed: {result}")


def init_workers():
    for worker_id in range(N_WORKERS):
        Thread(target=worker, args=(worker_id,)).start()


def stop_workers():
    for i in range(N_WORKERS):
        task_queue.put(None)
    for t in workers:
        t.join()
