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
    """
    function retrieves a list of numbers from a globally accessible task queue,
    computes their sum, and adds the result to a cumulative sum stored in a remote storage. This
    process is synchronized using a global lock to ensure thread safety when accessing and modifying
    the remote storage. The function terminates when it retrieves a None value from the task queue,
    indicating no more tasks are available.

    Parameters:
    - worker_id (int): An identifier for the worker, used for logging purposes.

    Returns:
    - None. The function directly modifies the global `remote_storage` and outputs to the console.
    """

    while True:
        numbers = task_queue.get()
        if numbers is None:
            break
        result = sum(numbers)
        with storage_lock:
            remote_storage["sum"] += result
        print(f"Worker {worker_id=} finished processing: {result=}")


def init_workers():
    for worker_id in range(N_WORKERS):
        Thread(target=worker, args=(worker_id,)).start()


def stop_workers():
    for i in range(N_WORKERS):
        task_queue.put(None)
    for t in workers:
        t.join()
