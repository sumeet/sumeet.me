"""Serve the generated site, including byte-range requests for media seeking."""
import os
from pathlib import Path

from whitenoise import WhiteNoise


def not_found(environ, start_response):
    body = b'Not found\n'
    start_response('404 Not Found', [
        ('Content-Type', 'text/plain; charset=utf-8'),
        ('Content-Length', str(len(body))),
    ])
    return [] if environ['REQUEST_METHOD'] == 'HEAD' else [body]


def static_headers(headers, path, url):
    headers['Accept-Ranges'] = 'bytes'


application = WhiteNoise(
    not_found,
    root=str(Path(__file__).resolve().parent / 'build'),
    index_file=True,
    autorefresh=os.environ.get('SITE_DEV') == '1',
    max_age=0,
    add_headers_function=static_headers,
)
