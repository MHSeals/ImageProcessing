import cv2
import threading
import time

class Webcam:
    def __init__(self):
        self.frames = []
        self.running = True
        self.capture = cv2.VideoCapture()
        self.frames_count = 10
        self.thread = threading.Thread(target=self.capture_frames)


    def capture_frames(self):
        while self.running:
            returnVal, frame = self.capture.read()

            # Don't do anything if frames weren't captured
            if not returnVal:
                continue

            self.frames.append(frame)
            
            if len(self.frames) > self.frames_count:
                self.frames.pop(0)


    def get_frames(self):
        while not len(self.frames) == self.frames_count:
            print(f'Waiting to capture {self.frames_count} frames from the camera')
            time.sleep(1)

        return self.frames


    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        self.capture.release()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        self.capture.release()

