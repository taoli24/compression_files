import argparse
from image_compression import ImageCompression


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Image compression")
    parser.add_argument(
        "input_file",
        metavar="input_file",
        type=str,
        help="Path to the original image"
    )
    parser.add_argument(
        "output_folder",
        metavar="output_folder",
        type=str,
        help="Output directory"
    )
    parser.add_argument(
        "--convert_color",
        action="store_true",
        help="Convert to YCbCr",
        dest="convert"
    )
    parser.add_argument(
        "-q",
        metavar="--quality",
        type=int,
        help="Output image quality",
        dest="quality",
        choices=[10, 20, 30, 40, 50, 60, 70, 80, 90]
    )
    parsed_args = parser.parse_args()
    input_file = parsed_args.input_file
    output_folder = parsed_args.output_folder
    convert = parsed_args.convert
    image_quality = parsed_args.quality
    ImageCompression(input_file, output_folder, convert, image_quality)()