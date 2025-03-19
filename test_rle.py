import time
import tracemalloc
import psutil
import os
from rle_imperative import rle_encode, rle_decode, rle_encode_image, rle_decode_image
from rle_functional import rle_encode_functional, rle_decode_functional, rle_encode_image_functional, rle_decode_image_functional
from rle_oop import RLETextProcessor, RLEImageProcessor

def measure_time(func, *args):
    start_time = time.perf_counter_ns()
    result = func(*args)
    end_time = time.perf_counter_ns()
    elapsed_time = (end_time - start_time) / 1e9
    return result, elapsed_time

def measure_memory(func, *args, is_method=False, obj=None):

    process = psutil.Process(os.getpid())
    
    time.sleep(0.1)
    start_memory = process.memory_info().rss  
    tracemalloc.start() 
    
    if is_method and obj:
        result = func(obj, *args)  
    else:
        result = func(*args)  
    
    time.sleep(0.1)
    end_memory = process.memory_info().rss  
    current, peak = tracemalloc.get_traced_memory()  
    tracemalloc.stop()  
    
    memory_used = (end_memory - start_memory) / 1024  #
    python_memory_used = peak / 1024 
    
    return result, max(memory_used, python_memory_used)

def test_rle(encode_func, decode_func, data, paradigm_name):
    try:
        print(f"\nТестування {paradigm_name} підходу для тексту:")
        
        encoded, encode_time = measure_time(encode_func, data)
        _, encode_memory = measure_memory(encode_func, data)
        
        decoded, decode_time = measure_time(decode_func, encoded)
        _, decode_memory = measure_memory(decode_func, encoded)

        original_size = len(data.encode('utf-8'))
        original_size_kb = original_size/1024
        encoded_size = len(encoded.encode('utf-8'))
        encoded_size_kb = original_size/1024
        
        compression_ratio = original_size / encoded_size if encoded_size > 0 else float('inf')
        compression_throughput = original_size_kb / encode_time if encode_time > 0 else float('inf')
        decompression_throughput = original_size_kb / decode_time if decode_time > 0 else float('inf')

        if decoded == data:
            print("Тест успішний!")
            print(f"Оригінальний розмір: {original_size} байт")
            print(f"Стиснутий розмір: {encoded_size} байт")
            print(f"Ступінь стиснення: {compression_ratio:.2f}")
            print(f"Час стиснення: {encode_time:.9f} сек.")
            print(f"Час розпакування: {decode_time:.9f} сек.")
            print(f"Пропускна здатність (стиснення): {compression_throughput:.2f} КБ/сек.")
            print(f"Пропускна здатність (декодування): {decompression_throughput:.2f} КБ/сек.")
            print(f"Використання пам'яті (стиснення): {encode_memory:.2f} КБ")
            print(f"Використання пам'яті (розпакування): {decode_memory:.2f} КБ")
        else:
            print("Тест невдалий: дані не співпадають.")
    except Exception as e:
        print(f"Виникла помилка: {e}")

def test_image_rle(encode_func=None, decode_func=None, image_processor=None, paradigm_name=None):
    try:
        print(f"\nТестування {paradigm_name} підходу для зображень:")
        
        if image_processor:
            start_compression = time.perf_counter_ns()
            encoded_image_path, encoded_data = image_processor.encode_image()
            end_compression = time.perf_counter_ns()
            _, encode_memory = measure_memory(RLEImageProcessor.encode_image, is_method=True, obj=image_processor)
        else:
            start_compression = time.perf_counter_ns()
            encoded_image_path, encoded_data, width, height = encode_func(image_path)
            end_compression = time.perf_counter_ns()
            _, encode_memory = measure_memory(encode_func, image_path)

        compression_time = (end_compression - start_compression) / 1e9
        
        original_size = os.path.getsize(image_path)
        original_size_kb = original_size/1024
        compressed_file_size = os.path.getsize(encoded_image_path)
        compressed_file_size_kb = compressed_file_size/1024

        start_decompression = time.perf_counter_ns()
        if image_processor:
            decoded_image_path = image_processor.decode_image(encoded_image_path)
            _, decode_memory = measure_memory(RLEImageProcessor.decode_image, encoded_image_path, is_method=True, obj=image_processor)
        else:
            decoded_image_path = decode_func(encoded_image_path)
            _, decode_memory = measure_memory(decode_func, encoded_image_path)
        end_decompression = time.perf_counter_ns()

        decompression_time = (end_decompression - start_decompression) / 1e9

        compression_ratio = original_size / compressed_file_size if compressed_file_size > 0 else float('inf')
        compression_throughput = original_size_kb / compression_time if compression_time > 0 else float('inf')
        decompression_throughput = original_size_kb / decompression_time if decompression_time > 0 else float('inf')

        print(f"Розмір до стиснення: {original_size} байт")
        print(f"Розмір після стиснення: {compressed_file_size} байт")
        print(f"Ступінь стиснення: {compression_ratio:.2f}")
        print(f"Час стиснення: {compression_time:.9f} сек.")
        print(f"Час декодування: {decompression_time:.9f} сек.")
        print(f"Пропускна здатність (стиснення): {compression_throughput:.2f} КБ/сек.")
        print(f"Пропускна здатність (декодування): {decompression_throughput:.2f} КБ/сек.")
        print(f"Використання пам'яті (стиснення): {encode_memory:.2f} КБ")
        print(f"Використання пам'яті (декодування): {decode_memory:.2f} КБ")
    except Exception as e:
        print(f"Виникла помилка: {e}")

with open("test_data/test_data.txt", "r") as f:
    test_data = "".join(f.read().splitlines())

image_path = 'test_data/image2.jpg'

test_rle(rle_encode, rle_decode, test_data, "імперативного")
test_rle(rle_encode_functional, rle_decode_functional, test_data, "функціонального")
text_processor = RLETextProcessor(test_data)
test_rle(text_processor.encode, text_processor.decode, test_data, "ООП")

test_image_rle(encode_func=rle_encode_image, decode_func=rle_decode_image, paradigm_name="імперативного")
test_image_rle(encode_func=rle_encode_image_functional, decode_func=rle_decode_image_functional, paradigm_name="функціонального")
image_processor = RLEImageProcessor(image_path)
test_image_rle(image_processor=image_processor, paradigm_name="ООП")