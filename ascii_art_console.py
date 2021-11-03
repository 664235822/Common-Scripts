from PIL import Image, ImageDraw, ImageFont
import argparse
import numpy as np

sample_rate = 0.4


def ascii_art(file):
    # 打开给定图片
    im = Image.open(file)

    # 转换为灰阶图
    im = im.convert("L")

    # 图片降采样
    sample_rate=0.15
    # 得到字符的宽高比
    font = ImageFont.load_default()
    aspect_ratio = font.getsize("x")[0] / font.getsize("x")[1]
    # 将图片高度乘上这个宽高比
    new_im_size = np.array(
        [im.size[0] * sample_rate, im.size[1] * sample_rate * aspect_ratio]
    ).astype(int)

    im = im.resize(new_im_size)

    # 将图片转换为numpy数组
    im = np.array(im)

    # 定义所有将用于字符画中的字符，按照字符亮度升序排列
    symbols = np.array(list(" .-vM"))

    # 亮度0-5的索引，用于查阅定义的字符.[0,5),其中5指symbols中元素的个数
    im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

    # Generate the ascii art
    ascii = symbols[im.astype(int)]
    lines="\n".join(("".join(r)for r in ascii))
    print(lines)


if __name__ == "__main__":
    ascii_art("5.png")