from PIL import Image
import os
def PNG_ResizeKeepTransparency(SourceFile, ResizedFile, new_width=0, new_height=0, resample="ANTIALIAS", RefFile =''):
    """
    :param SourceFile: initial PNG file (including the path)
    :param ResizedFile: resized PNG file (including the path)
    :param new_width: the width after resizing
    :param new_height: the height after resizing
    :param resample: "NEAREST", "BILINEAR", "BICUBIC" and "ANTIALIAS"; default = "ANTIALIAS"
    :param RefFile: reference file to get the size for resize; default = ''
    """

    img = Image.open(SourceFile) # open PNG image path and name
    img = img.convert("RGBA")    # convert to RGBA channels
    width, height = img.size     # get initial size

    # if there is a reference file to get the new size
    if RefFile != '':
        imgRef = Image.open(RefFile)
        new_width, new_height = imgRef.size
    else:
        # if we use only the new_width to resize in proportion the new_height
        # if you want % of resize please use it into new_width (?% * initial width)
        if new_height == 0:
            new_height = new_width*width/height

    # split image by channels (bands) and resize by channels
    img.load()
    bands = img.split()
    # resample mode
    if resample=="NEAREST":
        resample = Image.NEAREST
    else:
        if resample=="BILINEAR":
            resample = Image.BILINEAR
        else:
            if resample=="BICUBIC":
                resample = Image.BICUBIC
            else:
                if resample=="ANTIALIAS":
                    resample = Image.ANTIALIAS
    bands = [b.resize((new_width, new_height), resample) for b in bands]
    # merge the channels after individual resize
    img = Image.merge('RGBA', bands)
    # save the image
    # img.save(ResizedFile)
    return img

if __name__ == '__main__':

    PNG_ResizeKeepTransparency('OK-IMG_2468_output.png', os.getcwd()+'/resized2.png', new_width= int(800*3450/4520), new_height=800)
    # imgo = Image.open('OK-IMG_0671_output.png')
    # imgo = imgo.convert("RGBA")  # 转换获取信息
    # pixdata = imgo.load()
    # print(imgo.size[0])
    # print(imgo.size[1])
    # img = Image.open('resized.png')
    # img = img.convert("RGBA")  # 转换获取信息
    # pixdata1 = img.load()
    # print(img.size[0])
    # print(img.size[1])
    # img.load()