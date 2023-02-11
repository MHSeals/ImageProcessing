import DepthSensor
import cv2

count = 0
frames = []
frames_count = 100

def save_frames():
    for frame in frames:
        # get color and depth frame
        color, depth = frame

        # write to file
        cv2.imwrite(f'./captured-frames/color/color_{count}.jpg', color)
        cv2.imwrite(f'./captured-frames/depth/depth_{count}.jpg', depth)

        count += 1


try:
    with DepthSensor.DepthSensor() as camera:
        while True:
            frames.append(camera.get_frames())
            if len(frames) >= frames_count:
                save_frames()
                frames.clear()
except KeyboardInterrupt:
    save_frames()
    exit(0)
