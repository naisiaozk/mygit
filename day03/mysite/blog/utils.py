import random,string
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import hashlib
import hmac
from django.conf import settings

# 获取一个随机字符串，4位的
def getRandomChar(count=4):
    # 生成随机字符串
    # string模块包含各种字符串，以下为小写字母加数字
    ran = string.ascii_lowercase + string.ascii_uppercase + string.digits
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


# 返回一个随机的RGB颜色
def getRandomColor():
    return (random.randint(50,150),random.randint(50,150),random.randint(50,150))


def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new('RGB', (120,30), (255,255,255))
    #创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('arial.ttf', 25)

    code = getRandomChar()
    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30*t+5,0),code[t],getRandomColor(),font)

    # 生成干扰点
    for _ in range(random.randint(0,200)):
        # 位置，颜色
        draw.point((random.randint(0, 120),
random.randint(0, 30)),fill=getRandomColor())

    # 使用模糊滤镜使图片模糊
    img = img.filter(ImageFilter.BLUR)
    # 保存
    # img.save(''.join(code)+'.jpg','jpeg')
    return img,code


# hash加密
def hash_by_md5(pwd):
    md5 = hashlib.md5(pwd.encode("utf-8"))
    md5.update(settings.MD5_SALT.encode("utf-8"))
    return md5.hexdigest()


# hash加密，这种方法使用了对称加密和hash，安全性更高
def hmac_by_md5(pwd):
    return hmac.new(pwd.encode('utf-8'), settings.MD5_SALT.encode("utf-8"), "MD5").hexdigest()


if __name__ == '__main__':
    print(create_code())



