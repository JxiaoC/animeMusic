# coding=utf-8
from __future__ import absolute_import
import realpath
import requests
import os

from models.anime_music import model
from helper import tietuku

tb_anime_list = model.AnimeList()


def downloadAndUpload(title, url, filename):
    print('download for', title, url)
    with open("./" + filename, "wb") as code:
        code.write(requests.get(url).content)
    print('uploading...')
    img_url = tietuku.uploadImgToTieTuKu("./" + filename)
    try:
        os.remove("./" + filename)
    except:
        pass
    return img_url


skip = 0
limit = 100
total = tb_anime_list.find({'tietukuname': None}).count()
complete_num = 0
while True:
    i = 0
    _list = tb_anime_list.find({'tietukuname': None}).limit(limit).skip(skip)
    for f in _list:
        i += 1
        try:
            logo = f['logo']
            bg = f['bg']
            if not logo and not bg:
                continue
            title = f['title']
            filename = '%s.jpg' % f['_id']

            new_logo = ''
            new_bg = ''

            if logo:
                new_logo = downloadAndUpload(title, logo, filename)
                if not new_logo:
                    print('logo upload error')
                    continue
            if bg:
                new_bg = downloadAndUpload(title, bg, filename)
                if not new_bg:
                    print('bg upload error')
                    continue

            tb_anime_list.update({'_id': f['_id']}, {'$set': {
                'bg': new_bg,
                'logo': new_logo,
                'tietukuname': '419067339@qq.com',
            }})

            complete_num += 1
            print('(', complete_num, '/', total, ')', title)
        except Exception as e:
            print(e)
            pass
    if i == 0:
        print('complete')
        break
    skip += limit