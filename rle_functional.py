from itertools import groupby
from PIL import Image
import os

def rle_encode_functional(data):
    return "".join(f"{sum(1 for _ in group)}{char}" for char, group in groupby(data))

def rle_decode_functional(encoded_data):
    result = []
    i = 0
    while i < len(encoded_data):
        count = ''
        while i < len(encoded_data) and encoded_data[i].isdigit():
            count += encoded_data[i]
            i += 1
        if i < len(encoded_data):
            result.append(encoded_data[i] * int(count))
            i += 1
    return ''.join(result)

def rle_encode_image_functional(image_path):
    img = Image.open(image_path).convert('1')
    width, height = img.size

    pixels = list(img.getdata())
    pixel_str = ''.join('1' if pixel == 255 else '0' for pixel in pixels)

    encoded_data = rle_encode_functional(pixel_str)

    encoded_image_path = f"{os.path.splitext(image_path)[0]}_functional.txt"
    with open(encoded_image_path, 'w') as f:
        f.write(f"{width},{height}\n")  
        f.write(encoded_data)  

    return encoded_image_path, encoded_data, width, height


def rle_decode_image_functional(encoded_image_path, original_extension='.png'):
    
    with open(encoded_image_path, 'r') as f:
        width, height = map(int, f.readline().strip().split(','))  
        encoded_data = f.read() 

    decoded_data = rle_decode_functional(encoded_data)

    pixels = [255 if char == '1' else 0 for char in decoded_data]

    img = Image.new('1', (width, height))
    img.putdata(pixels)

    decoded_image_path = f"{os.path.splitext(encoded_image_path)[0]}_decoded{original_extension}"
    img.save(decoded_image_path)

    return decoded_image_path