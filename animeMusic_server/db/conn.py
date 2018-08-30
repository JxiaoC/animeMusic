# -*- coding:utf-8 -*-

import os

from pymongo import (
    MongoReplicaSetClient,
    MongoClient,
    read_preferences
)
import gridfs

mc = MongoClient(host='localhost')
anime_music = mc['anime_music']