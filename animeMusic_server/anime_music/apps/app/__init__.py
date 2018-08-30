
from turbo import register

from .import app

register.register_group_urls('/api/v1', [
    ('/music', app.MusicHeader),
    ('/music/([0-9a-f]{24})', app.MusicHeader),
])