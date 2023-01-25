import ffmpeg
import os
import cv2


class VideoCompression:

    def __init__(self, input_path, output_path, target_size):
        self.input_path = input_path
        self.output_path = output_path
        self.target_size = target_size

    @staticmethod
    def check_path(path):
        return os.path.isdir(path), os.path.isfile(path)

    def get_duration(self):
        cap = cv2.VideoCapture(self.input_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        return frame // fps

    def compress_video(self):
        supported = ["mp4", "avi"]

        if not self.check_path(self.input_path)[1]:
            raise FileNotFoundError("Input file does not exist.")

        if not self.check_path(self.output_path)[0]:
            raise NotADirectoryError("Output directory does not exist.")

        if (not isinstance(self.target_size, int)) and (not isinstance(self.target_size, float)):
            raise TypeError("Target size must be integer or float.")

        # self.target_size = float(self.target_size)
        min_audio_bitrate = 32000
        max_audio_bitrate = 256000

        ext = self.input_path.split(".")[-1]

        if ext not in supported:
            raise TypeError(f"File extension of {ext} is not supported.")

        probe = ffmpeg.probe(self.input_path)

        duration = float(probe['format']['duration'])

        audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])

        target_size = (32000 + 100000) * (1.073741824 * duration) / (8 * 1024) \
            if self.target_size < (32000 + 100000) * (1.073741824 * duration) / (8 * 1024) else self.target_size

        target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

        if 10 * audio_bitrate > target_total_bitrate:
            audio_bitrate = target_total_bitrate / 10
            if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                audio_bitrate = min_audio_bitrate
            elif audio_bitrate > max_audio_bitrate:
                audio_bitrate = max_audio_bitrate

        video_bitrate = target_total_bitrate - audio_bitrate
        i = ffmpeg.input(self.input_path)
        print(self.output_path + self.input_path.split("/")[-1].split(".")[0] + ".mp4")
        ffmpeg.output(i, os.devnull,
                      **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                      ).overwrite_output().run()
        ffmpeg.output(i, self.output_path + self.input_path.split("/")[-1].split(".")[0] + ".mp4",
                      **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                      ).overwrite_output().run()

    def __call__(self, *args, **kwargs):
        print("Start video compression")
        print("---------------------------------------------------------------")
        try:
            self.compress_video()
        except Exception as e:
            print("Failed to compress video: {}".format(str(e)))


if __name__ == '__main__':
    VideoCompression("./test_files/Sample-MP4-Video.mp4", "./output/", 9)()
