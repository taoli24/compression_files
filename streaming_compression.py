import cv2
import sys
from subprocess import Popen, PIPE
from PIL import Image
import os


class StreamingCompression:
    def __init__(self, device, output_path, output_file_name):
        self.device = device
        self.output_path = output_path
        self.output_file_name = output_file_name
        if "mp4" not in output_file_name:
            raise Exception("The output file names need to contain mp4 extension")

    @staticmethod
    def check_path(path):
        return os.path.isdir(path), os.path.isfile(path)

    def get_bitrate(self, height, width, duration, bitrate, target_size):
        min_audio_bitrate = height * width // 100
        max_audio_bitrate = height * width
        if not self.check_path(self.output_path)[0]:
            raise FileExistsError("output dir not exist")
        target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

        # Target audio bitrate, in bps
        if 10 * bitrate > target_total_bitrate:
            audio_bitrate = target_total_bitrate / 10
            if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                bitrate = min_audio_bitrate
            elif audio_bitrate > max_audio_bitrate:
                bitrate = max_audio_bitrate
        video_bitrate = target_total_bitrate - bitrate
        return video_bitrate

    def stream_video(self, fps=24, codec="mp4v"):
        try:
            cam = cv2.VideoCapture(self.device)
        except Exception as e:
            print("Camera device {} can not be opened: {}".format(self.device, str(e)))

        width = int(cam.get(3))
        height = int(cam.get(4))
        target_size = (width * height) * (1.073741824 * 1 / fps) / (8 * 1024)
        new_bitrate = int(self.get_bitrate(height, width, 1 / fps, cam.get(cv2.CAP_PROP_BITRATE), target_size) / 1000)
        p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-r', str(fps), '-i', '-',
                   '-vcodec', 'h264', '-qscale', '5', '-r', str(fps), '-b:v', str(new_bitrate) + "K",
                   '-maxrate', str(new_bitrate) + "K", "-bufsize", str(int(new_bitrate // 2)) + "K",
                   self.output_path + self.output_file_name], stdin=PIPE)

        cam.set(cv2.CAP_PROP_FPS, fps)
        if not cam.isOpened():
            print("Unable to open camera")
            sys.exit(-1)
        codec = cv2.VideoWriter_fourcc(*codec)
        out = cv2.VideoWriter(str(self.output_path), codec, fps, (width, height))
        out.set(cv2.VIDEOWRITER_PROP_QUALITY, 10)
        image_count = 0
        while True:
            check, frame = cam.read()
            if check:
                # Write to stdin
                cv2.imshow('video', frame)
                image_count += 1
                im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                im.save(p.stdin, 'JPEG')
                key = cv2.waitKey(1)
                # exit on esc
                if key == 27:
                    break
            else:
                break
        cam.release()
        cv2.destroyAllWindows()

    def __call__(self, *args, **kwargs):
        print("start streaming")
        print("---------------------------------------------------------------")
        try:
            self.stream_video()
        except Exception as e:
            print("Unable to stream video: {}".format(str(e)))


if __name__ == '__main__':
    print("start streaming")
    print("------------------------------- -------------------------------")
    StreamingCompression(1, "./output", "/example.mp4")()
