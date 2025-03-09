import numpy as np
import openai
import json
import os

key = 'key'

# Set up OpenAI API client
client = openai.OpenAI(api_key=key)

def load_json_file(file_path):
    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
    
# Embedding function
def get_embedding(input):
    return client.embeddings.create(
        input=input,
        model="text-embedding-3-small"
    ).data[0].embedding


def resize_embedding(embedding, target_size):
    """
    Hàm này sẽ cắt hoặc thêm phần tử vào embedding sao cho chiều dài bằng target_size.
    """
    if len(embedding) > target_size:
        return embedding[:target_size]  # Cắt nếu embedding dài hơn target_size
    else:
        # Thêm 0 vào cuối nếu embedding ngắn hơn target_size
        return np.pad(embedding, (0, target_size - len(embedding)), mode='constant')


def flatten_json(data):
    def recursive_flatten(item, parent_key=""):
        items = []
        if isinstance(item, dict):  # Xử lý nếu là dictionary
            for k, v in item.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                items.extend(recursive_flatten(v, new_key))
        elif isinstance(item, list):  # Xử lý nếu là danh sách
            for i, v in enumerate(item):
                new_key = f"{parent_key}[{i}]" if parent_key else f"[{i}]"
                items.extend(recursive_flatten(v, new_key))
        else:  # Nếu là giá trị cơ bản
            items.append((parent_key, item))
        return items

    def remove_prefix_keys(flattened_data):
        return {key.split('.', 1)[-1]: value for key, value in flattened_data.items()}

    # Nếu đầu vào là danh sách, xử lý từng phần tử
    if isinstance(data, list):
        return [remove_prefix_keys(dict(recursive_flatten(item))) for item in data]
    elif isinstance(data, dict):  # Trường hợp đặc biệt là dictionary đơn
        return [remove_prefix_keys(dict(recursive_flatten(data)))]
    else:
        raise ValueError("Input must be a list of dictionaries or a single dictionary.")


def prepare_data(data):
    # Các key không cần tạo embedding
    exclude_keys = ["name", "original_price", "discount_price"]
    
    for d in data:
        embeddings = []  # Danh sách để lưu trữ tất cả embedding cần thiết
        for key, value in d.items():
            if key not in exclude_keys and isinstance(value, str):  # Chỉ xử lý giá trị dạng chuỗi
                embeddings.extend(get_embedding(value))  # Thêm embedding vào danh sách
        d["embedding"] = embeddings  # Gộp tất cả embedding vào một trường duy nhất
    return data
    

def save_json_file(data, file_path):
    # Lưu dữ liệu vào file JSON
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # Đảm bảo rằng các ký tự không phải ASCII được lưu đúng cách


def embedding_data(file_path):
    product_data = flatten_json(load_json_file(file_path))

    data = prepare_data(product_data)

    output_file_path = "product_data_with_embeddings.json"
    save_json_file(data, output_file_path)
    return data

