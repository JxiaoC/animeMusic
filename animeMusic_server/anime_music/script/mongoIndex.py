# coding=utf-8
from __future__ import absolute_import
from .import realpath

from models.anime_music import model

tb_anime_list = model.AnimeList()

music_list = model.MusicList()
music_list.ensure_index('anime_id')
music_list.ensure_index('atime')
music_list.ensure_index('recommend')