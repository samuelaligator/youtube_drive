from PIL import Image
import math
import os


def file_to_image(input_file, output_image, pixel_length=4, width=1920, height=1080):
    # Read the hexadecimal values of the file
    with open(input_file, 'rb') as f:
        data = f.read()

    file_size = len(data)
    total_bits = file_size * 8
    pixels_per_img = (width * height) // (pixel_length ** 2)
    total_img = math.ceil(total_bits / pixels_per_img)
    print(f"total_img : {total_img}")
    for img_index in range(total_img):
        print(img_index)
        # Create an image initialized in black
        img = Image.new('1', (width, height), 0)
        pixels = img.load()

        first_bit_index = img_index * pixels_per_img
        last_bit_index = min((img_index + 1) * pixels_per_img , total_bits)
        bits = ""

        # Browse data and update pixels
        for i in range(first_bit_index, last_bit_index):
            byte_index = i // 8
            bit_index = 7 - (i % 8)  # MSB
            bit = (data[byte_index] >> bit_index) & 1
            bits = bits + str(bit)
            if bit:
                for j in range(pixel_length ** 2):
                    x = ((i - first_bit_index) * pixel_length) % width + (j % pixel_length)
                    y = ((((i - first_bit_index) * pixel_length) // width) * pixel_length) + (j // pixel_length)
                    pixels[x, y] = 1

        output_img_no_ext, output_extension = os.path.splitext(output_image)
        img.save(f"{output_img_no_ext}_{img_index + 1}{output_extension}")
        print(bits)


# Exemple
file_to_image('./text.txt', './output/output.png', pixel_length=4, width=1920, height=1080)