import threading
import time

class thread(threading.Thread):
    def __init__(self, thread_name, thread_ID, *thread_args):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

        def run():
            self.thread_args[0]()
            
        