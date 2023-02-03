import threading
import time
import pyrealsense2 as rs


class DepthSensor:
    def __init__(self) -> None:
        # RealSense camera setup
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(
            self.device.get_info(rs.camera_info.product_line))

        for s in self.device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break

        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(
            rs.stream.color, 640, 480, rs.format.bgr8, 30)

        self.running = True
        self.frames = []
        self.frames_count = 10
        self.thread = threading.Thread(target=self.capture_frames)

        # Start streaming
        self.pipeline.start(self.config)

    def capture_frames(self):
        while self.running:
            frame = self.pipeline.wait_for_frames()
            color = frame.get_color_frame()
            depth = frame.get_depth_frame()

            if not depth or not color:
                continue

            self.frames.append((color, depth))

            if len(self.frames) > self.frames_count:
                self.frames.pop(0)

    def get_frames(self):
        while not len(self.frames) == self.frames_count:
            print(
                f'Waiting to capture {self.frames_count} frames from the camera')
            time.sleep(1)
        return self.frames

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        self.pipeline.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        self.pipeline.stop()
