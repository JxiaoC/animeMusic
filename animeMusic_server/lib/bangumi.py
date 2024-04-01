# bangumi API
import datetime
import json
from urllib.parse import quote
from cPython import cPython as cp

default_ua = 'xiaoc/AnimeMusic/1.0.0 (Web) (https://github.com/JxiaoC/animeMusic)'
host = 'https://api.bgm.tv'


def search(keywords: str):
    url = '%s/search/subject/%s?type=2&max_results=25&responseGroup=large' % (host, quote(keywords))
    html = cp.get_html(url, headers={'user-agent': default_ua})
    json_data = json.loads(html)
    res = []
    for f in json_data.get('list', []):
        if f.get('air_date').startswith('0000'):
            air_date = datetime.datetime(1970, 1, 1)
        else:
            air_date = datetime.datetime.strptime(f.get('air_date'), '%Y-%m-%d')
        images = f.get('images', {})
        res.append({
            'id': f['id'],
            'name': f.get('name', ''),
            'name_cn': f.get('name_cn', ''),
            'desc': f.get('summary', ''),
            'year': air_date.year,
            'month': air_date.month,
            'img': images.get('medium', '') if images else '',
        })
    return res


if __name__ == '__main__':
    print(search('蓝色监狱'))
