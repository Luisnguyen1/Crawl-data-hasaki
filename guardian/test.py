import json

# Đường dẫn đến file JSON
file_path = 'product_data.json'

# Đọc nội dung file
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Đếm số lượng phần tử
count = len(data)

print(f"Số lượng phần tử trong file JSON là: {count}")