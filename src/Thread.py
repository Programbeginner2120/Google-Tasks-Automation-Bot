import threading

class thread(threading.Thread):
    def __init__(self, thread_name, thread_ID, *thread_args):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.thread_args = thread_args

    def run(self):
        self.thread_args[0]()
            
        