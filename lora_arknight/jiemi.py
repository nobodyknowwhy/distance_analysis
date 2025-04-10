import cv2
import numpy as np
from PIL import Image
import requests

# 加载图片
url = "https://ak.hypergryph.com/future"
response = requests.get(url)
image_content = response.content

# 将图片内容转换为NumPy数组
image_array = np.frombuffer(image_content, np.uint8)
image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

# 获取图片的高度和宽度
height, width, _ = image.shape

# 确定裁剪的边长（取最小边长）
crop_size = min(height, width)

# 计算裁剪的起始点和结束点
start_x = (width - crop_size) // 2
start_y = (height - crop_size) // 2
end_x = start_x + crop_size
end_y = start_y + crop_size

# 裁剪图片
cropped_image = image[start_y:end_y, start_x:end_x].copy()

# 提取上三角部分（左上到右下对角线）
size = crop_size
for i in range(size):
    for j in range(i + 1, size):
        # 将上三角部分的像素值与下三角部分按0.3透明度叠加
        cropped_image[j, i] = (cropped_image[i, j].astype(np.float32) * 0.7 + cropped_image[j, i].astype(np.float32) * 0.3).astype(np.uint8)

# 将颜色通道从BGR转换为RGB
cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

# 保存结果
result_image = Image.fromarray(cropped_image_rgb)
result_image.save("folded_image.png")


import cv2
import numpy as np
from PIL import Image
import requests

# 加载图片
url = "https://ak.hypergryph.com/future"
response = requests.get(url)
image_content = response.content

# 将图片内容转换为NumPy数组
image_array = np.frombuffer(image_content, np.uint8)
image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

# 获取图片的高度和宽度
height, width, _ = image.shape

# 确定裁剪的边长（取最小边长）
crop_size = min(height, width)

# 计算裁剪的起始点和结束点
start_x = (width - crop_size) // 2
start_y = (height - crop_size) // 2
end_x = start_x + crop_size
end_y = start_y + crop_size

# 裁剪图片
cropped_image = image[start_y:end_y, start_x:end_x].copy()

# 提取下三角部分（右上到左下对角线）
size = crop_size
for i in range(size):
    for j in range(size - i - 1):
        # 将上三角部分的像素值与下三角部分按0.3透明度叠加
        cropped_image[i, j] = (cropped_image[i, j].astype(np.float32) * 0.7 + cropped_image[size - j - 1, size - i - 1].astype(np.float32) * 0.3).astype(np.uint8)

# 将颜色通道从BGR转换为RGB
cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

# 保存结果
result_image = Image.fromarray(cropped_image_rgb)
result_image.save("folded_image2.png")