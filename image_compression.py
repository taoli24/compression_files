import cv2
import numpy as np
import os
import sys


class ImageCompression:
    def __init__(self, input_path, output_path, apply_color_convert, quality):
        self.input_path = input_path
        self.output_path = output_path
        self.apply_color_convert = apply_color_convert
        self.quality = quality

    @staticmethod
    def check_path(path):
        return os.path.isdir(path), os.path.isfile(path)

    def input_image(self):
        supported = ["png", "jpeg", "jpg"]
        file_ext = self.input_path.split(".")[-1]
        if not self.check_path(self.input_path)[1]:
            raise FileNotFoundError("Input file does not exist.")

        if file_ext not in supported:
            raise TypeError("Input file with file extension .{} is not supported.".format(file_ext))

        image = cv2.imread(self.input_path)

        return image

    def encode_image(self):
        assert type(self.apply_color_convert) == bool, f"Boolean expected, got: {type(self.apply_color_convert)}"
        assert self.quality > 10 & self.quality < 100, f"Quality should be between 10 and 100, got: {self.quality}"
        if self.apply_color_convert:
            image = cv2.cvtColor(self.input_image(), cv2.COLOR_BGR2YCrCb)
        else:
            image = self.input_image()
        return np.array(cv2.imencode('.jpeg', image, [cv2.IMWRITE_JPEG_QUALITY, self.quality])[1])

    def output_image(self):
        if not self.check_path(self.output_path)[0]:
            raise NotADirectoryError("{} is not a directory.".format(self.output_path))
        np.save(
            self.output_path + self.input_path.split("/")[-1].split(".")[0],
            self.encode_image(),
            allow_pickle=True
        )

    def __call__(self, *args, **kwargs):
        print("start image compression")
        print("---------------------------------------------------------------")
        try:
            self.output_image()
        except Exception as e:
            print("Failed to compress image: {}".format(str(e)))

        print("Image compression finished(0)")
        sys.exit(0)


if __name__ == '__main__':
    print(sys.argv)
    # ImageCompression("./test_files/Sample_jpg.jpg", "./output/", True, 50)()

