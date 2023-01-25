import laspy
import os


class LasCompression:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    @staticmethod
    def check_path(path):
        return os.path.isdir(path), os.path.isfile(path)

    def input_las(self):
        if not self.check_path(self.input_path)[1]:
            raise FileNotFoundError("Input file does not exist.")

        ext = self.input_path.split(".")[-1]

        if ext != "las":
            raise TypeError(f"File type of .{ext} is not supported for las compression.")

        data = laspy.read(self.input_path)
        return data

    def compressed_las(self):
        if not self.check_path(self.output_path):
            raise NotADirectoryError("{} is not a directory.".format(self.output_path))
        return self.input_las().write(self.output_path + self.input_path.split("/")[-1].split(".")[0] + ".laz")

    def __call__(self, *args, **kwargs):
        print("start streaming")
        print("---------------------------------------------------------------")
        try:
            self.compressed_las()
        except Exception as e:
            print("Fail to compress las file: {}".format(str(e)))


if __name__ == '__main__':
    LasCompression("./test_files/test_3d_data.las", "./output/")()
