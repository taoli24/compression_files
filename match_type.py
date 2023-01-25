import sys
from image_compression import ImageCompression
from las_compression import LasCompression
from streaming_compression import StreamingCompression
from video_compression import VideoCompression
import subprocess


def input_type(input_path):
    image_type_list = ["bmp", "jpeg", "jpg", "jpe", "dib", "jp2", "png", "webp", "pbm", "pgm", "*ppm", "pxm", "pnm",
                       "sr", "ras", "tiff", "tif", "exr", "hdr", "pic"]
    las_type_list = ["las", "laz"]
    video_type_list = ["mp4"]
    if input_path.lower() in image_type_list:
        return 0
    elif input_path.lower() in las_type_list:
        return 1
    elif input_path.lower() in video_type_list:
        return 2
    elif len(input_path) == 1:
        return 3
    else:
        return 4


if __name__ == '__main__':
    parameter = (sys.argv[1]).split(",")
    # print(parameter[0].split(".")[1])
    if "." in parameter[0]:
        data_type = parameter[0].split(".")[1]
    else:
        data_type = parameter[0]
    output = input_type(data_type)
    print(output)
    if output == 0:
        print("                  Start image compression                      ")
        print("------------------------------- -------------------------------")
        if len(parameter) != 4:
            raise Exception("Wrong input parameter")
        ImageCompression(parameter[0], parameter[1], bool(parameter[2]), int(parameter[3]))()
    elif output == 1:
        print("                  Start las compression                        ")
        print("------------------------------- -------------------------------")
        if len(parameter) != 2:
            raise Exception("Wrong input parameter")
        LasCompression(parameter[0], parameter[1])()
    elif output == 2:
        print("                  Start video compression                        ")
        print("------------------------------- -------------------------------")
        if len(parameter) != 3:
            raise Exception("Wrong input parameter")
        VideoCompression(parameter[0], parameter[1], float(parameter[2]))()
    elif output == 3:
        print("                  Start streaming compression                        ")
        print("------------------------------- -------------------------------")
        if len(parameter) != 3:
            raise Exception("Wrong input parameter")
        sc = StreamingCompression(int(parameter[0]), parameter[1], parameter[2])
        sc.stream_video()
    elif output == 4:
        print(parameter)
        subprocess.run(["zstd", str(parameter[0]), "--output-dir-flat", str(parameter[1])])
