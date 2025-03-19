from PIL import Image
import os
import sys

sys.set_int_max_str_digits(1000000)

def rle_encode(data):

    if not data:
        return ""
    encoded_data = ""
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data += f"{count}{data[i - 1]}"  
            count = 1
    encoded_data += f"{count}{data[-1]}"  
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
        if i < len(encoded_data):
            symbol = encoded_data[i]
            i += 1
            decoded_data += symbol * int(count_str)
    return decoded_data

def rle_encode_image(image_path):

    img = Image.open(image_path).convert('L')  
    width, height = img.size

    pixels = list(img.getdata()) 

    encoded_data = ""
    count = 1
    for i in range(1, len(pixels)):
        if pixels[i] == pixels[i - 1]:
            count += 1
        else:
            encoded_data += f"{count},{pixels[i - 1]};"  
            count = 1
    encoded_data += f"{count},{pixels[-1]};" 

    encoded_image_path = f"{os.path.splitext(image_path)[0]}_imperative.txt"
    with open(encoded_image_path, 'w') as f:
        f.write(f"{width},{height}\n")
        f.write(encoded_data)  

    return encoded_image_path, encoded_data, width, height

def rle_decode_image(encoded_image_path, original_extension='.png'):
   
    with open(encoded_image_path, 'r') as f:
        width_height = f.readline().strip().split(',') 
        width = int(width_height[0])
        height = int(width_height[1])
        encoded_data = f.read()  

    decoded_data = []
    parts = encoded_data.split(";") 
    for part in parts:
        if part:
            count, value = part.split(",")  
            decoded_data.extend([int(value)] * int(count))

    img = Image.new('L', (width, height))  
    img.putdata(decoded_data)

    decoded_image_path = f"{os.path.splitext(encoded_image_path)[0]}_decoded{original_extension}"
    img.save(decoded_image_path)

    return decoded_image_path