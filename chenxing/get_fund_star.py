import os

import requests
from PIL import Image

gif_name = './xingji.gif'
relation = {249599: "0",
            258278: '1',
            257152: '2',
            255456: '3',
            252316: '4',
            240630: '5'
            }


def get_star_by_url(url):
    """
    获取基金的星级
    """
    res = requests.get(url)
    with open(gif_name, 'wb') as f:
        f.write(res.content)
    image = Image.open(gif_name)
    pix = image.load()
    total = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            total += pix[i, j]
    image.close()
    os.remove(gif_name)
    return relation[total]


if __name__ == '__main__':
    print(get_star_by_url('https://www.morningstar.cn/sitedataapi/CryptogramAPI.asmx/GetData?data=GfaXTDpE8jQ%3d'))
