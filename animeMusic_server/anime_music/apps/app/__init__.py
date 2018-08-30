
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
    ('/music/list', god.MusicListHeader),
])