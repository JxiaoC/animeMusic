
from turbo import register

from .import app
from .import god

register.register_group_urls('/api/v1', [
    ('/music', app.MusicHeader),
    ('/music/([0-9a-f]{24})', app.MusicHeader),
])

register.register_group_urls('/god', [
    ('', god.MusicHeader),
])

register.register_group_urls('/god/api/v1', [
    ('/anime/list', god.AnimeListHeader),
    ('/anime/save/([0-9a-f]{24})', god.AnimeSaveHeader),
    ('/anime/del/([0-9a-f]{24})', god.AnimeDelHeader),
    ('/anime/upload/logo/([0-9a-f]{24})', god.AnimeUploadLogoHeader),
    ('/anime/upload/bg/([0-9a-f]{24})', god.AnimeUploadBgHeader),

    ('/music/list', god.MusicListHeader),
    ('/music/del', god.MusicListHeader),
])