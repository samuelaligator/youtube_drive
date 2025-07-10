from PIL import Image
import math
import os


def file_to_image(input_file, output_image, width=1920, height=1080):
    # Read the hexadecimal values of the file
    with open(input_file, 'rb') as f:
        data = f.read()

    file_size = len(data)
    total_bits = file_size * 8
    pixels_per_img = width * height
    total_img = math.ceil(total_bits / pixels_per_img)

    for img_index in range(total_img):
        # Create an image initialized in black
        img = Image.new('1', (width, height), 0)
        pixels = img.load()

        first_bit_index = img_index * pixels_per_img
        last_bit_index = min((img_index + 1) * pixels_per_img, total_bits)

        # Browse data and update pixels
        for i in range(first_bit_index, last_bit_index):
            byte_index = i // 8
            bit_index = 7 - (i % 8)  # MSB
            bit = (data[byte_index] >> bit_index) & 1

            if bit:
                x = (i % width)
                y = (i // width) % height
                pixels[x, y] = 1

        output_img_no_ext, output_extension = os.path.splitext(output_image)

        img.save(f"{output_img_no_ext}_{img_index + 1}{output_extension}")


# Exemple
file_to_image('text.txt', './output/output.png', width=5, height=5)