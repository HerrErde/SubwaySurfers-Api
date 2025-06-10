import os
import threading
from queue import Queue
from pathlib import Path


def worker(queue, search_string, results):
    while True:
        filepath = queue.get()
        if filepath is None:
            break
        try:
            with open(filepath, "rb") as f:
                if search_string.encode() in f.read():
                    results.append(filepath)
        except:
            pass
        queue.task_done()


def find_string_in_files_threaded(directory, search_string, num_threads=8):
    if not Path(directory).exists():
        raise ValueError("Directory does not exist.")

    queue = Queue()
    results = []

    # Start worker threads
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(queue, search_string, results))
        t.daemon = True
        t.start()
        threads.append(t)

    # Walk the directory and queue file paths
    for root, _, files in os.walk(directory):
        for name in files:
            queue.put(os.path.join(root, name))

    # Block until all tasks are done
    queue.join()

    # Stop workers
    for _ in threads:
        queue.put(None)
    for t in threads:
        t.join()

    return results


matches = find_string_in_files_threaded(
    "./com.kiloo.subwaysurf_3.47.0-82042_minAPI23(arm64-v8a,armeabi-v7a)(nodpi)_apkmirror.com.apk-decompiled",
    "genuine_app",
)
print("\n".join(matches))
