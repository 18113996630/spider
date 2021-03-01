from PIL import Image
import requests

res = requests.get('https://www.morningstar.cn/sitedataapi/CryptogramAPI.asmx/GetData?data=GfaXTDpE8jQ%3d')
with open('./xingji.gif', 'wb') as f:
    f.write(res.content)
relation = {249599: "零星",
            258278: '一星',
            257152: '二星',
            255456: '三星',
            252316: '四星',
            240630: '五星'
            }
image = Image.open('./xingji.gif')
# image = Image.open('D:/tmp/t1.png')
pix = image.load()
total = 0
for i in range(image.size[0]):
    for j in range(image.size[1]):
        total += pix[i, j]

print('星级: {level}'.format(level=relation[total]), total)
print('-' * 20)
