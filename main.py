from PIL import Image
import numpy as np
import math
import os
import subprocess

def closest_common_divisor(n: int, m: int, x: int) -> int:
    """ Returns the common divisor of n and m that is closest to x. (n and m must be positive) """

    # Find all common divisors of n and m
    g = math.gcd(n, m)
    divisors = set()
    for i in range(1, math.isqrt(g) + 1):
        if g % i == 0:
            divisors.add(i)
            divisors.add(g // i)

    # Find the closest divisor to x
    closest_divisor = min(divisors, key=lambda d: abs(d - x))

    return closest_divisor


def file_to_images(input_file: str, output_image: str, block_length: int = 4, width: int = 1920, height: int = 1080):
    """
    Encodes a file into a sequence of 1-bit images using pixel block representation.

    Args:
        input_file (str): Source file path
        output_image (str): Base output path
        block_length (int): Pixel block size for one-bit
        width (int): Image width
        height (int): Image height

    Behavior:
        - Auto-adjusts block_length if incompatible with dimensions
        - Each bit: block (0=black, 1=white)
        - Generates numbered output files when data exceeds image capacity
        - Processes bits MSB-first in raster order (left→right, top→bottom)
    """

    # Auto-adjusts block_length if incompatible with dimensions
    if width % block_length != 0 or height % block_length != 0:
        block_length = closest_common_divisor(width, height, block_length)
        print(f"Error: width and height must be multiples of bloc_length. \n Automatic block_length change : now block_length = {block_length}\n")

    # Read the hexadecimal values of the file
    with open(input_file, 'rb') as f:
        data = f.read()

    file_size = len(data)
    total_bits = file_size * 8
    bits_per_img = (width * height) // (block_length ** 2)
    total_img = math.ceil(total_bits / bits_per_img)
    print(f"Generation of {total_img} images measuring {width}x{height} with {bits_per_img} bits per image for 1 bit of {block_length}-pixels length.")

    for img_index in range(total_img):
        print(f"{img_index}/{total_img}")

        # Create a numpy array initialized in 0 = black
        arr = np.zeros((height, width), dtype=np.uint8)

        # Browse data and update pixels
        first_bit_index = img_index * bits_per_img
        last_bit_index = min((img_index + 1) * bits_per_img, total_bits)
        for i in range(first_bit_index, last_bit_index):
            byte_index = i // 8
            bit_index = 7 - (i % 8)  # MSB
            bit = (data[byte_index] >> bit_index) & 1
            if bit:
                base_x = ((i - first_bit_index) * block_length) % width
                base_y = ((((i - first_bit_index) * block_length) // width) * block_length)
                # update a block of pixels to white
                arr[base_y:base_y + block_length, base_x:base_x + block_length] = 255

        # convert the numpy array to a pillow image
        img = Image.fromarray(arr).convert('1')

        # Save the image
        output_img_no_ext, output_extension = os.path.splitext(output_image)
        img.save(f"{output_img_no_ext}_{img_index + 1}{output_extension}")

    print(f"{total_img}/{total_img}")
    print(f"{total_img} images generated in {output_image}\n")


def images_to__video(input_pattern: str, output_video: str, frames_per_image: int = 1, output_fps: int = 30):
    """
    Converts a sequence of images into a lossless H.264 video using ffmpeg.

    Parameters:
    - input_pattern (str): Pattern for input images, e.g. 'img_%03d.png'
    - output_video (str): Output video file path
    - frames_per_image (int): How many video frames each image should last
    - output_fps (int): Final framerate of the output video
    """

    # Framerate for image input
    input_fps = output_fps / frames_per_image

    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output file
        "-framerate", str(input_fps),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-crf", "0",  # Lossless mode
        "-preset", "ultrafast",  # Fastest encoding (bigger files)
        "-pix_fmt", "yuv420p",  # For max compatibility (YouTube)
        "-r", str(output_fps),  # Output FPS
        output_video
    ]

    print("Converting image sequence into video:", " ".join(cmd))
    subprocess.run(cmd, check=True)


# Exemple
file_to_images('/home/zamuel/IMG_20210812_144623.jpg', './output/output.png', block_length=4, width=1920, height=1080)
images_to__video('/home/zamuel/PycharmProjects/youtube_drive/output/output_%d.png', 'video.mp4', frames_per_image=10, output_fps=30)