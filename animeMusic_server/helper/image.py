# -*- coding:utf-8 -*-
# 图片处理代码基于http://fc-lamp.blog.163.com/blog/static/174566687201282424018946/小幅度修改

from PIL import Image as image


def resizeImg(**args):
    args_key = {'path': '', 'out_path': '', 'width': '', 'height': '', 'quality': 75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
        else:
            arg[key] = None

    im = image.open(arg['path'])
    ori_w, ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (arg['width'] and ori_w and ori_w > arg['width']) or (arg['height'] and ori_h and ori_h > arg['height']):
        if arg['width'] and ori_w > arg['width']:
            widthRatio = float(arg['width']) / ori_w  # 正确获取小数的方式
        if arg['height'] and ori_h > arg['height']:
            heightRatio = float(arg['height']) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth, newHeight), image.ANTIALIAS).convert('RGB').save(arg['out_path'], quality=arg['quality'])


def clipResizeImg(**args):
    args_key = {'path': '', 'out_path': '', 'width': '', 'height': '', 'quality': 75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = image.open(arg['path'])
    ori_w, ori_h = im.size

    dst_scale = float(arg['height']) / arg['width']  # 目标高宽比
    ori_scale = float(ori_h) / ori_w  # 原高宽比

    if ori_scale >= dst_scale:
        # 过高
        width = ori_w
        height = int(width * dst_scale)

        x = 0
        y = (ori_h - height) / 3

    else:
        # 过宽
        height = ori_h
        width = int(height * dst_scale)

        x = (ori_w - width) / 2
        y = 0

    # 裁剪
    box = (x, y, width + x, height + y)
    # 这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    # 所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    # 压缩
    ratio = float(arg['width']) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth, newHeight), image.ANTIALIAS).convert('RGB').save(arg['out_path'], quality=arg['quality'])