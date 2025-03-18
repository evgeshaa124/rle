def rle_encode(data):
    if not data:
        return ""
    encoded_data = ""
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data += str(count) + data[i - 1]
            count = 1
    encoded_data += str(count) + data[-1]
    return encoded_data

def rle_decode(encoded_data):
    if not encoded_data:
        return ""
    decoded_data = ""
    i = 0
    while i < len(encoded_data):
        count_str = ""
        while i < len(encoded_data) and encoded_data[i].isdigit():
            count_str += encoded_data[i]
            i += 1
        num_count = int(count_str) if count_str else 1
        if i < len(encoded_data):
            symbol = encoded_data[i]
            decoded_data += symbol * num_count
            i += 1
        else:
            break
    return decoded_data

import os
from PIL import Image

def rle_encode_image(image_path):
    img = Image.open(image_path).convert('1')
    width, height = img.size

    pixels = list(img.getdata())
    pixel_str = ''.join('1' if pixel == 255 else '0' for pixel in pixels)

    encoded_data = rle_encode(pixel_str)

    encoded_image_path = f"{os.path.splitext(image_path)[0]}_imperative.txt"
    with open(encoded_image_path, 'w') as f:
        f.write(f"{width},{height}\n")  
        f.write(encoded_data)  

    return encoded_image_path, encoded_data, width, height

def rle_decode_image(encoded_image_path, original_extension='.png'):

    with open(encoded_image_path, 'r') as f:
        width, height = map(int, f.readline().strip().split(','))  
        encoded_data = f.read()  

    decoded_data = rle_decode(encoded_data)

    pixels = [255 if char == '1' else 0 for char in decoded_data]

    img = Image.new('1', (width, height))
    img.putdata(pixels)

    decoded_image_path = f"{os.path.splitext(encoded_image_path)[0]}_decoded{original_extension}"
    img.save(decoded_image_path)

    return decoded_image_path
