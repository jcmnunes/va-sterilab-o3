import threading
import time

class SerialThread(threading.Thread):
    '''
    This is the thread that deals with serial communication with arduino.
    The method run() reads a line from the buffer and puts it in the queue.
    '''
    def __init__(self, queue, device):
        threading.Thread.__init__(self)
        self.queue = queue
        self.device = device
        self._stop_req = False
    def run(self):
        while not self._stop_req:
            self.device.flushInput()
            text = self.device.readline().decode('utf-8').rstrip('\r\n')
            # Test the validity of the data from the arduino. If data passes
            # the test put it in the queue.
            if text[:4] == 'temp' and self.queue.empty():
                self.queue.put(text)
                self.queue.join()
    def stop(self):
        self._stop_req = True