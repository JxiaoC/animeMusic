
from turbo import register

from .import app
from .import appv2
from .import god

register.register_group_urls('/api/v1', [
    ('/music', app.MusicHeader),
    ('/music/([0-9a-f]{24})', app.MusicHeader),
])

register.register_group_urls('/api/v2', [
    ('/music', appv2.MusicHeader),
    ('/music/([0-9a-f]{24})', appv2.MusicHeader),
    ('/music/list', appv2.MusicListHeader),
    ('/music/search', appv2.MusicSearchHeader),
    ('/anime/search', appv2.AnimeSearchHeader),
])

register.register_group_urls('/god', [
    ('', god.GodHeader),
])

register.register_group_urls('/god/api/v1', [
    ('/anime/list', god.AnimeListHeader),
    ('/anime/add', god.AnimeAddHeader),
    ('/anime/search_bangumi', god.AnimeSearchBangumiHeader),
    ('/anime/(save|del)/([0-9a-f]{24})', god.AnimeHeader),
    ('/anime/upload/(logo|bg)/([0-9a-f]{24})', god.AnimeUploadHeader),

    ('/music/list', god.MusicListHeader),
    ('/music/add/([0-9a-f]{24})', god.MusicAddHeader),
    ('/music/(save|del)/([0-9a-f]{24})', god.MusicHeader),
    ('/music/upload/([0-9a-f]{24})', god.MusicUploadHeader),
])