from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


# 验证码生成

def check_code(width=120, height=32, char_length=5, font_file='./user/static/fonts/Monaco.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndchar():
        """
        生成随机字母
        :return:
        """
        # return chr(random.randint(65, 90))
        return str(random.randint(0, 9))

    def rndcolor():
        """
        生成随机颜色
        :return:
        """
        return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndchar()
        code.append(char)
        h = random.randint(0, 4)
        # draw.text([i * width / char_length, h], char, font=font, fill=rndcolor())
        draw.text((i * width / char_length, h), char, font=font, fill=rndcolor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndcolor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndcolor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndcolor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndcolor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
