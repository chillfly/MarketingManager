import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

_lower_letter = "abcdefghjkmnqrtuy"
_upper_letter = _lower_letter.upper()
_numbers = ''.join(map(str, range(3, 10)))
init_chars = ''.join((_lower_letter, _upper_letter, _numbers))



def randomPointColor():
    """
    干扰点随机颜色
    :return:
    """
    res = (random.randint(64, 200), random.randint(64, 200), random.randint(64, 200))
    return res


def randomLineColor():
    """
    干扰线随机颜色
    :return:
    """
    res = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    return res


def randomStrColor():
    """
    验证码随机颜色
    :return:
    """
    res = (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
    return res


def create_captcha(
        size=(120, 30),
        chars=init_chars,
        img_type="PNG",
        mode="RGB",
        bg_color=(255, 255, 255),
        fg_color=(0, 0, 255),
        font_size=20,
        font_type="DejaVuSans.ttf",
        length=4,
        draw_lines=True,
        n_line=(1, 2),
        draw_points=True,
        point_chance=2):
    """
    @todo: 生成验证码图片
    :param size: 图片的大小，格式（宽，高）， 默认为（120,30）
    :param chars:允许的字符集合，格式字符串
    :param img_type:图片保存的格式，默认为GIF，JPEG,TIFF,PNG
    :param mode:图片模式，默认为RGB
    :param bg_color:背景色，默认为白色
    :param fg_color:前景色，即验证码字符颜色，默认为蓝色#0000FF
    :param font_size:验证码字体大小
    :param font_type:验证码字体，默认为ae_AlArabiya.ttf
    :param length:验证码字符个数
    :param draw_lines:是否画干扰线
    :param n_line:干扰性条数范围，格式元祖，默认为（1,2），只有draw_lines为True时有效
    :param draw_points:是否画干扰点
    :param point_chance:干扰点出现的概率，大小范围[0,100]
    :return:[0]:PIL Image实例
    :return:[1]:验证码图片中的字符串
    """
    width, height = size  # 宽， 高
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        """
        生成给定长度的字符串，返回列表格式
        :return:
        """
        return random.sample(chars, length)



    def create_lines():
        """
        绘制干扰线
        :return:
        """
        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=randomLineColor())

    def create_points():
        """
        绘制干扰点
        :return:
        """
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=randomPointColor())

    def create_strs():
        """
        绘制验证码字符
        :return:
        """
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

        try:
            font = ImageFont.truetype(font_type, font_size)
        except:
            font = ImageFont.load_default()
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=randomStrColor())

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    # img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
    # img = img.filter(ImageFilter.BLUR)  # 模糊处理

    return img, strs
