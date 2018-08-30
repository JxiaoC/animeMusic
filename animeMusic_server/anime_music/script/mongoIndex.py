# coding=utf-8
from __future__ import absolute_import
import realpath

from models.anime_music import model

tb_anime_list = model.AnimeList()
tb_anime_list.ensure_index([('title', -1), ('atime', -1)])
tb_anime_list.ensure_index([('_id', -1), ('atime', -1)])

music_list = model.MusicList()
music_list.ensure_index('atime')
music_list.ensure_index('recommend')
tb_anime_list.ensure_index([('title', -1), ('atime', -1)])
tb_anime_list.ensure_index([('_id', -1), ('atime', -1)])
tb_anime_list.ensure_index([('anime_id', -1), ('atime', -1)])