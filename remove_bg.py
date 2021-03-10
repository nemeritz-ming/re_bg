import os
import zipfile
from PIL import Image
import Zip
import Resize


def close(box, bg, mur_2):
    return abs(box[0] - bg[0]) <= mur_2 and abs(box[1] - bg[1]) <= mur_2 and abs(box[2] - bg[2]) <= mur_2


def cut_image(path='/Users/edz/Documents', white=False):
    """
    :param path: 文件路径
    :param white: 处理白色为true
    """
    z = zipfile.ZipFile(path + "/1.zip", "r")
    z.extractall(path=path)
    z.close()
    mur = 10
    mur_2 = 6
    k = 2
    if white:
        mur = 5
        mur_2 = 0
        k = 6
    os.chdir(path)
    os.mkdir(path + '/pic_output2')
    for cur_img in z.namelist():
        if cur_img[-3:] == 'jpg':
            img = Image.open(cur_img)
            img = img.convert("RGBA")  # 转换获取信息
            pixdata = img.load()
            r = pixdata[0, 0][0]
            g = pixdata[0, 0][1]
            b = pixdata[0, 0][2]
            a = pixdata[0, 0][3]
            bg = (r, g, b, a)
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
            theta = 0.55
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
                                if num >= int(((2 * k + 1) ** 2) * theta):
                                    pixdata[x, y] = copy_pixdata[x, y]
            img.save(path + '/pic_output2/{0}_output.png'.format(cur_img.split('/')[-1].split('.j')[0]))
    Zip.zip_file_path(r"./pic_output2", path, '抠图结果.zip')


if __name__ == '__main__':
    cut_image()
