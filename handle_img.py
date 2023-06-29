import os
import re

import cv2


def check_image(image_path):
    # 检查图片文件是否存在
    if not os.path.exists(image_path):
        print(f"图片文件不存在：{image_path}")
        return False

    # 检查图片文件格式
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    file_extension = os.path.splitext(image_path)[1].lower()
    if file_extension not in valid_extensions:
        print(f"无效的图片文件格式：{file_extension}")
        return False

    # 检查图片文件大小
    file_size = os.path.getsize(image_path)
    if file_size == 0:
        print("图片文件大小为零")
        return False

    # 检查图片文件的完整性
    try:
        img = cv2.imread(image_path)
        if img is None:
            print("无法打开图片文件")
            return False
    except Exception as e:
        print(f"无法打开图片文件：{e}")
        return False

    # 检查图片尺寸
    height, width, _ = img.shape
    if height <= 0 or width <= 0:
        print("图片尺寸异常")
        return False

    # 检查图片的颜色通道
    num_channels = len(img.shape)
    if num_channels != 3:
        print(f"无效的颜色通道数：{num_channels}")
        return False

    # 检查图片像素值范围
    min_pixel_value = img.min()
    max_pixel_value = img.max()
    if min_pixel_value < 0 or max_pixel_value > 255:
        print("图片像素值异常")
        return False

    return True


if __name__ == '__main__':
    # 批量图片检查
    image_folder = './images'
    image_files = os.listdir(image_folder)

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        result = check_image(image_path)
        if result:
            print(f"图片检查通过：{image_path}")
            date = re.search(r'([0-9]{4})-([0-9]{2})-([0-9]{2})', image_path)
            if date:
                # 将图片移动到对应的日期文件夹下
                year = date.group(1)
                month = date.group(2)
                day = date.group(3)
                new_folder = os.path.join(image_folder, year, month, day)
                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)
                new_image_path = os.path.join(new_folder, image_file)
                os.rename(image_path, new_image_path)
        else:
            print(f"图片检查未通过, 删除图片：{image_path}")
            os.remove(image_path)
