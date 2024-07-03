from PIL import Image

def create_icon(input_image_path, output_icon_path, sizes):
    # 打开图像并转换为RGBA格式
    img = Image.open(input_image_path).convert('RGBA')

    # 创建一个新的图像列表
    images = []

    # 为每个尺寸创建一个新的图像
    for size in sizes:
        new_img = img.resize(size, Image.LANCZOS)  # 使用Image.LANCZOS代替Image.ANTIALIAS
        images.append(new_img)

    # 保存图像为.ico文件
    new_img.save(output_icon_path, format='ICO', sizes=sizes)

# 调用函数来创建.ico文件
create_icon('Lotus.jpg', 'Lotus.ico', [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
