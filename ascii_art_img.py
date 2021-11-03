from PIL import Image, ImageDraw, ImageFont
import argparse
import numpy as np
import glob2 as glob

sample_rate = 0.4


def ascii_art(file):
    # 打开给定图片
    im = Image.open(file)

    # Compute letter aspect ratio
    font = ImageFont.load_default()
    aspect_ratio = font.getsize("x")[0] / font.getsize("x")[1]
    new_im_size = np.array(
        [im.size[0] * sample_rate, im.size[1] * sample_rate * aspect_ratio]
    ).astype(int)

    # 图片降采样
    im = im.resize(new_im_size)

    # 保存图片副本
    im_color = np.array(im)

    # 转换为灰阶图
    im = im.convert("L")

    # 将图片转换为numpy数组
    im = np.array(im)

    # 定义所有将用于字符画中的字符，按照字符亮度升序排列
    symbols = np.array(list(" .-vM"))

    # 亮度0-5的索引，用于查阅定义的字符.[0,5),其中5指symbols中元素的个数
    im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

    # Generate the ascii art
    ascii = symbols[im.astype(int)]

    # 将字符画创建为图片
    letter_size = font.getsize("x")
    # 宽高为字符宽高乘图像的宽高
    im_out_size = new_im_size * letter_size
    bg_color = "black"
    # 创建一个Pillow的图像，im_out
    im_out = Image.new("RGB", tuple(im_out_size), bg_color)
    # 创建ImageDraw对象，完成对文本字符绘制
    draw = ImageDraw.Draw(im_out)

    # 使用循环每行每列绘制字符
    y = 0
    for i, line in enumerate(ascii):
        for j, ch in enumerate(line):
            color = tuple(im_color[i, j])  # 提取图片颜色
            draw.text((letter_size[0] * j, y), ch[0], fill=color, font=font)
        y += letter_size[1]  # increase y by letter height

    # 保存图片
    im_out.save(file + ".ascii.png")
    print("已生成为："+file+".ascii.png")


if __name__ == "__main__":
    # ascii_art("5.png")
    file_number = glob.glob(pathname="out/*.jpg")
    for i in file_number:
        ascii_art(i)