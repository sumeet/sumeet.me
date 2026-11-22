"""HTTP integration checks for the same server used by Dokku and make serve."""
import http.client
from contextlib import closing
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / 'build/projects/solsolver-full.mp4'


class StaticServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not VIDEO.exists():
            raise RuntimeError('Run make html before these tests')
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            cls.port = listener.getsockname()[1]
        cls.log = tempfile.TemporaryFile()
        cls.server = subprocess.Popen([
            sys.executable, '-m', 'gunicorn', 'site_server:application',
            '--bind', f'127.0.0.1:{cls.port}', '--workers', '1', '--threads', '4',
        ], cwd=ROOT, stdout=cls.log, stderr=cls.log)
        cls.addClassCleanup(cls.cleanup_server)
        for _ in range(100):
            if cls.server.poll() is not None:
                cls.log.seek(0)
                raise RuntimeError(cls.log.read().decode())
            try:
                with socket.create_connection(('127.0.0.1', cls.port), timeout=.1):
                    return
            except OSError:
                time.sleep(.05)
        raise RuntimeError('Static server did not start')

    @classmethod
    def cleanup_server(cls):
        cls.server.terminate()
        cls.server.wait(timeout=10)
        cls.log.close()

    def request(self, method, path, headers=None):
        with closing(http.client.HTTPConnection('127.0.0.1', self.port, timeout=5)) as connection:
            connection.request(method, path, headers=headers or {})
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()

    def test_seeking_reads_only_requested_bytes(self):
        size = VIDEO.stat().st_size
        for start, end, header in [
            (0, 31, 'bytes=0-31'),
            (size - 1024, size - 1, f'bytes={size - 1024}-'),
            (size - 512, size - 1, 'bytes=-512'),
        ]:
            with self.subTest(range=header):
                status, headers, body = self.request('GET', '/projects/solsolver-full.mp4', {'Range': header})
                self.assertEqual(status, 206)
                self.assertEqual(headers['Content-Range'], f'bytes {start}-{end}/{size}')
                self.assertEqual(int(headers['Content-Length']), end - start + 1)
                with VIDEO.open('rb') as source:
                    source.seek(start)
                    self.assertEqual(body, source.read(end - start + 1))

    def test_unsatisfiable_range(self):
        size = VIDEO.stat().st_size
        status, headers, _ = self.request('GET', '/projects/solsolver-full.mp4', {'Range': f'bytes={size}-'})
        self.assertEqual(status, 416)
        self.assertEqual(headers['Content-Range'], f'bytes */{size}')

    def test_head_advertises_ranges_without_sending_body(self):
        status, headers, body = self.request('HEAD', '/projects/solsolver-full.mp4')
        self.assertEqual(status, 200)
        self.assertEqual(headers['Accept-Ranges'], 'bytes')
        self.assertEqual(int(headers['Content-Length']), VIDEO.stat().st_size)
        self.assertEqual(body, b'')

    def test_existing_pages_and_editor_assets(self):
        wasm = next((ROOT / 'projects/rejectsynth/assets').glob('*.wasm'))
        for path, content_type in [
            ('/', 'text/html'), ('/resume/', 'text/html'),
            ('/sumeet.pdf', 'application/pdf'),
            ('/projects/rejectsynth/', 'text/html'),
            ('/' + str(wasm.relative_to(ROOT)), 'application/wasm'),
        ]:
            with self.subTest(path=path):
                status, headers, _ = self.request('HEAD', path)
                self.assertEqual(status, 200)
                self.assertTrue(headers['Content-Type'].startswith(content_type))
        self.assertEqual(self.request('GET', '/requirements.txt')[0], 404)


if __name__ == '__main__':
    unittest.main()
