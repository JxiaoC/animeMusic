# -*- coding:utf-8 -*-

from db.conn import (
    anime_music as _anime_music,
)

MONGO_DB_MAPPING = {
    'db': {
        'anime_music': _anime_music,
    },
    'db_file': {
    }
}
