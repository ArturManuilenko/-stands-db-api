import queue
import time
import os
import uuid

UPDATE_TIMEOUT = 100

class TaskException(Exception):
    pass

class EmptyTask:
    def __init__(self, args=(), kwargs={}):
        self.uid = str(uuid.uuid1())
        self.args = args
        self.kwargs = kwargs
        self.error = None
        self.progress = 0.0
        self.files = {}
        self.file_handlers = []
        self.data = {}
        self.end_timeout = UPDATE_TIMEOUT
        self.last_time = time.time()

    def __del__(self):
        self.clear()

    def checkBreak(self):
        return False

    def setProgress(self, value):
        self.progress = 1.0 if value > 1.0 else value

    def updateTime(self):
        self.last_time = time.time()

    def setError(self, text):
        raise TaskException()

    def open(self, file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        filename = self.uid + '__' + file
        f = open('tmp/' + filename, mode, buffering, encoding, errors, newline, closefd, opener)
        self.file_handlers.append(f)
        self.files[file] = filename
        return f

    def createFile(self, file):
        filename = self.uid + '__' + file
        f = open('tmp/' + filename, 'w')
        self.files[file] = filename
        f.close()
        return 'tmp/' + filename

    def clear(self):
        for f in self.file_handlers:
            f.close()
        self.file_handlers.clear()
        for filename in self.files.values():
            try:
                os.remove('tmp/'+filename)
            except Exception: pass
        self.files={}
        self.data={}

class Task(EmptyTask):
    def __init__(self, handler, *args, **kwargs):
        self.handler = handler
        self.enable = True
        self.kill_flag = False
        self.ready = False
        super().__init__(*args, **kwargs)


    def run(self):
        try:
            self.data = self.handler(self, *self.args, **self.kwargs)
        except Exception as e:
            self.error = e

        self.progress = 1.0
        self.ready = True

    def checkBreak(self):
        if self.kill_flag:
            raise TaskException()
        return not self.enable

    def kill(self):
        self.clear()
        self.enable = False
        self.kill_flag = True

    def stop(self):
        self.enable = False

    def clear(self):
        super().clear()
