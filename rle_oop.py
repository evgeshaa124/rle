from PIL import Image
import os
import sys

sys.set_int_max_str_digits(1000000)

class RLEProcessor:
    @staticmethod
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

    @staticmethod
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

class RLETextProcessor:
    def __init__(self, data=None):
        self.data = data

    def encode(self, data=None):
        if data is None:
            if self.data is None:
                raise ValueError("Дані для кодування відсутні.")
            data = self.data
        return RLEProcessor.rle_encode(data)

    def decode(self, encoded_data):
        return RLEProcessor.rle_decode(encoded_data)


class RLEProcessor:
    @staticmethod
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

    @staticmethod
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

class RLEImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.original_extension = os.path.splitext(image_path)[1]  # Зберігаємо розширення оригінального зображення

    def encode_image(self):
        """
        Кодує чорно-біле зображення за допомогою RLE.
        """
        img = Image.open(self.image_path).convert('1')  # Перетворюємо зображення у чорно-біле
        self.width, self.height = img.size
        pixels = list(img.getdata())
        pixel_str = ''.join('1' if pixel == 255 else '0' for pixel in pixels)
        encoded_data = RLEProcessor.rle_encode(pixel_str)

        encoded_image_path = f"{os.path.splitext(self.image_path)[0]}_oop.txt"
        with open(encoded_image_path, 'w') as f:
            f.write(f"{self.width},{self.height}\n")  # Зберігаємо розміри зображення
            f.write(encoded_data)  # Зберігаємо закодовані дані

        return encoded_image_path, encoded_data

    def decode_image(self, encoded_image_path):
       
        with open(encoded_image_path, 'r') as f:
            width, height = map(int, f.readline().strip().split(','))  
            encoded_data = f.read() 

        decoded_data = RLEProcessor.rle_decode(encoded_data)
        pixels = [255 if char == '1' else 0 for char in decoded_data]

        img = Image.new('1', (width, height))
        img.putdata(pixels)

        decoded_image_path = f"{os.path.splitext(encoded_image_path)[0]}_decoded{self.original_extension}"
        img.save(decoded_image_path)

        return decoded_image_path
