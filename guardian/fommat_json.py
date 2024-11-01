# Đường dẫn đến file txt
file_path = 'product_data.txt'

# Đọc nội dung file
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Xóa tất cả dấu [ và ]
# content = content.replace(']\n[', ',').replace(',,', ',')
# content = content.replace('}\n,', '},')
content = content.replace('}\n{', '},\n{')

# Ghi lại nội dung đã chỉnh sửa vào file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

print("Đã xóa tất cả các dấu [ và ] trong file.")