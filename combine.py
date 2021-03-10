import os
from PIL import Image, ImageDraw
import Resize


def max_len_of_img(img):
    """
    获取img上的衣服的最小轮廓
    :param img: 输如Image open打开的格式
    :return: 图片上衣服到上下左右边缘的距离
    """
    pix = img.load()
    heightmax, heightmin, widmax, widmin = 0, 0, 0, 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pix[x, y] != (255, 255, 255, 0) and pix[x, y] != (228, 228, 228, 255):
                heightmin = y
                break
        if heightmin != 0:
            break
    for y in range(img.size[1] - 1, -1, -1):
        for x in range(img.size[0] - 1, -1, -1):
            if pix[x, y] != (255, 255, 255, 0) and pix[x, y] != (228, 228, 228, 255):
                heightmax = y
                break
        if heightmax != 0:
            break
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pix[x, y] != (255, 255, 255, 0) and pix[x, y] != (228, 228, 228, 255):
                widmin = x
                break
        if widmin != 0:
            break

    for x in range(img.size[0] - 1, -1, -1):
        for y in range(img.size[1] - 1, -1, -1):
            if pix[x, y] != (255, 255, 255, 0) and pix[x, y] != (228, 228, 228, 255):
                widmax = x
                break
        if widmax != 0:
            break
    # draw = ImageDraw.Draw(img)
    # draw.line([(widmin, heightmin), (widmax, heightmin), (widmax, heightmax), (widmin, heightmax), (widmin, heightmin)],
    #           width=8, fill='red')

    return heightmax, heightmin, widmax, widmin


def concat_img(img1_name, img2_name, bg_name, size = 1000):
    """
    :param img1_name: img1的位置
    :param img2_name: img2的位置
    :param bg_name: 背景的位置
    :param size: 背景希望调成的大小
    """
    img1 = Image.open(img1_name)
    img1 = img1.convert("RGBA")  # 转换获取信息
    img3 = Image.open(img2_name)
    img3 = img3.convert("RGBA")
    img2 = Image.open(bg_name)
    img2 = img2.convert("RGBA")  # 转换获取信息
    img2 = img2.resize([size, size], Image.ANTIALIAS)
    center_width_ratio = (1.4 + 7.6 / 2) / (1.4 + 7.6 * 2 + 0.25)
    half_outer_width = 0.5 * 7.6 / (1.4 + 7.6 * 2 + 0.25) * img2.size[0]
    half_outer_height = 0.5 * img2.size[1]
    ratio0 = half_outer_height/ half_outer_width
    print(ratio0)
    img1_center_x = img2.size[0] * center_width_ratio
    img1_center_y = img2.size[1] * 0.5

    heightmax, heightmin, widmax, widmin = max_len_of_img(img1)
    cropped = img1.crop((widmin, heightmin, widmax, heightmax))  # (left, upper, right, lower)
    cropped_name = 'cur.png'
    cropped.save(cropped_name)
    ratio = cropped.size[1] / cropped.size[0]
    print(ratio)
    if ratio < 1.5:
        cropped = Resize.PNG_ResizeKeepTransparency(cropped_name, cropped_name, int(half_outer_width * 1.8),
                                                    int(1.8 * half_outer_width * ratio))
    else:
        cropped = Resize.PNG_ResizeKeepTransparency(cropped_name, cropped_name, int(half_outer_height * 1.5 / ratio),
                                                     int(1.5 * half_outer_height))

    os.remove(cropped_name)
    if 0.5 * cropped.size[0] < half_outer_width and 0.5 * cropped.size[1] < half_outer_height:
        left_conner = (int(img1_center_x - 0.5 * cropped.size[0]), int(img1_center_y - 0.5 * cropped.size[1]))
        r, g, b, a = cropped.split()
        img2.paste(cropped, left_conner, mask=a)
        print('finish')

    center_width_ratio_2 = (1.4 + 7.6 + 0.25 + 7.6 / 2) / (1.4 + 7.6 * 2 + 0.25)
    img2_center_x = img2.size[0] * center_width_ratio_2
    img2_center_y = img2.size[1] * 0.5

    heightmax, heightmin, widmax, widmin = max_len_of_img(img3)
    cropped2 = img3.crop((widmin, heightmin, widmax, heightmax))  # (left, upper, right, lower)
    cropped2.save(cropped_name)
    ratio = cropped2.size[1] / cropped2.size[0]
    if ratio < 1.5:
        cropped2 = Resize.PNG_ResizeKeepTransparency(cropped_name, cropped_name, int(half_outer_width * 1.8),
                                                    int(1.8 * half_outer_width * ratio))
    else:
        cropped2 = Resize.PNG_ResizeKeepTransparency(cropped_name, cropped_name, int(half_outer_height * 1.5 / ratio),
                                                     int(1.5 * half_outer_height))

    if 0.5 * cropped2.size[0] < half_outer_width and 0.5 * cropped2.size[1] < half_outer_height:
        left_conner = (int(img2_center_x - 0.5 * cropped2.size[0]), int(img2_center_y - 0.5 * cropped2.size[1]))
        r, g, b, a = cropped2.split()
        img2.paste(cropped2, left_conner, mask=a)
        print('finish')

    img2.save(os.getcwd() + '/3/CombinePic_{0}_and_{1}.png'.format(img1_name.split('/')[-1].split('.')[0],
                                                                 img2_name.split('/')[-1].split('.')[0]))


def possible_combination(file_dir):
    res = []
    file_list = os.listdir(file_dir)
    for i in range(len(file_list)):
        for j in range(i + 1, len(file_list)):
            res.append((file_list[i], file_list[j]))
    return res

def combine_all(file_path, bg_path):
    file_list = possible_combination(file_path)
    for tup in file_list:
        concat_img(file_path +"/" + tup[0], file_path +'/' + tup[1], 'back.jpg')


if __name__ == '__main__':
    # concat_img('OK-IMG_4996_output.png', 'OK-IMG_5006_output.png', 'back.jpg')
    file_list = possible_combination(os.getcwd()  + '/pic_output')
    for tup in file_list:
        concat_img(os.getcwd()  + '/pic_output/' + tup[0], os.getcwd()  + '/pic_output/'+ tup[1], 'back.jpg')


