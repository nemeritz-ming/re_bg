


import os
import cv2
import os
from PIL import Image
import numpy as np
import Zip


# img = cv2.imread('OK-IMG_3870_output.png', 0)#转化为灰度图
# x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
# y = cv2.Sobel(img, cv2.CV_16S, 0, 1)
# # cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])
# # 可选参数alpha是伸缩系数，beta是加到结果上的一个值，结果返回uint类型的图像
# Scale_absX = cv2.convertScaleAbs(x)  # convert 转换  scale 缩放
# Scale_absY = cv2.convertScaleAbs(y)
# result = cv2.addWeighted(Scale_absX, 0.5, Scale_absY, 0.5, 0)
# cv2.namedWindow("result",0) #可调大小
# cv2.namedWindow("1",0) #可调大小
# cv2.imshow('1', img)
# cv2.imshow('result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def close(box, bg, mur_2):
    return abs(box[0] - bg[0]) <= mur_2 and abs(box[1] - bg[1]) <= mur_2 and abs(box[2] - bg[2]) <= mur_2
cur_img = 'OK-IMG_6398.jpg'
img = Image.open(cur_img)
img = img.convert("RGBA")  # 转换获取信息
pixdata = img.load()
r = pixdata[0, 0][0]
g = pixdata[0, 0][1]
b = pixdata[0, 0][2]
a = pixdata[0, 0][3]
bg = (r, g, b, a)
print(bg)
bg = (228, 228, 228, 255)

mur = 5
mur_2 = 0
for x in range(img.size[0]):
    for y in range(img.size[1]):
        if abs(pixdata[x, y][0] - r) <= mur and abs(pixdata[x, y][1] - g) <= mur and abs(
                pixdata[x, y][2] - b) <= mur:
            num = 0
            if x - 1 >= 0:
                if close(pixdata[x - 1, y], bg, mur_2):
                    num += 1
            if y - 1 >= 0:
                if close(pixdata[1, y - 1], bg, mur_2):
                    num += 1
            if y + 1 < img.size[1]:
                if close(pixdata[x, y + 1], bg, mur_2):
                    num += 1
            if x + 1 < img.size[0]:
                if close(pixdata[x + 1, y], bg, mur_2):
                    num += 1
            if num >= 2:
                pixdata[x, y] = (255, 255, 255, 0)
img_p = Image.open(cur_img)
img_p = img_p.convert("RGBA")
copy_pixdata = img_p.load()
k = 5
for x in range(img.size[0]):
    for y in range(img.size[1]):
        if pixdata[x, y] == (255, 255, 255, 0):
            if x - 1 > 0 and y - 1 > 0 and x + 1 < img.size[0] and y + 1 < img.size[1]:
                if not (pixdata[x - 1, y] == (255, 255, 255, 0) and pixdata[x, y + 1] == (
                255, 255, 255, 0) and
                        pixdata[x + 1, y] == (255, 255, 255, 0) and pixdata[x, y - 1] == (
                        255, 255, 255, 0)):
                    num = 0
                    bigbox = []
                    if x - k >= 0 and y - k >= 0 and x + k < img.size[0] and y + k < img.size[1]:
                        for i in range(x - k, x + k + 1):
                            for j in range(y - k, y + k + 1):
                                if pixdata[i, j] != (255, 255, 255, 0):
                                    bigbox.append(pixdata[i, j])
                                    num += 1
                    if num >= int(((2 * k + 1) ** 2) * 0.55):
                        pixdata[x, y] = copy_pixdata[x, y]

img.save('output3.png')
