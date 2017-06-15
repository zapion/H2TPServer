#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import os
import re
import stat
import tempfile
import urllib.request

class WinNightlyDownloader:
    CONFIG = {
        'protocol': 'https',
        'host': 'archive.mozilla.org',
        'path': '/pub/firefox/nightly/latest-mozilla-central',
    }

    def __init__(self, platform):
        self.config = self.CONFIG.copy()

        self.config['platform'] = platform
        self.config['lang'] = 'en-US'
        self.config['version'] = self._check_version()
        self.config['installer'] = 'firefox-%(version)s.%(lang)s.%(platform)s.installer.exe' % (self.config)

        self.checksums = {}
        self.digests = {}
        self.path = ''
        self.filesize = 0

    def __del__(self):
        self.reset()

    def _check_version(self):
        url = '%(protocol)s://%(host)s%(path)s/' % (self.config)
        res = urllib.request.urlopen(url)
        data = res.read()
        for line in data.split(b'\n'):
            str_line = str(line, 'utf-8')
            str_pat = 'firefox-(\d+.\w+).%(lang)s.%(platform)s.installer.exe' % self.config 
            m = re.search(str_pat, str_line)
            if m:
                return m.group(1)
        return None

    def _prepare_checksums(self):
        url = '%(protocol)s://%(host)s%(path)s/firefox-%(version)s.%(lang)s.%(platform)s.checksums' % (self.config)
        res = urllib.request.urlopen(url)

        checksums = {}
        for line in res.read().split(b'\r\n'):
            if not line: continue
            str_line = str(line, 'utf-8')
            checksum, name, size, filename = str_line.split()
            checksum = checksum.lower()
            name = name.lower()
            size = int(size, 10)
            filename = filename.split('/')[-1]

            if filename != self.config['installer']: continue
            checksums[name] = {
                'checksum': checksum.lower(),
                'size': int(size),
            }
        self.checksums = checksums

    def fetch(self):
        self._prepare_checksums()

        url = '%(protocol)s://%(host)s%(path)s/%(installer)s' % (self.config)
        req = urllib.request.urlopen(url)

        fd, path = tempfile.mkstemp(prefix='nightly-', suffix='.exe')
        filesize = 0
        hashes = dict((m, hashlib.new(m)) for m in self.checksums)

        with os.fdopen(fd, 'wb', 65536) as f:
            while True:
                buf = req.read(65536)
                if not buf: break;

                filesize += len(buf)
                for m in hashes.values():
                    m.update(buf)
                
                f.write(buf)
                print('downloading: %d bytes\r' % filesize)
        print('')

        for k, v in hashes.items():
            self.digests[k] = v.hexdigest().lower()

        self.path = path
        self.filesize = filesize
        return True

    def check(self):
        for k, v in self.digests.items():
            if self.checksums[k]['checksum'] != v:
                print('checksum %s mismatch' % k)
                return False
            if self.checksums[k]['size'] != self.filesize:
                print('size %s mismatch' % k)
                return False
        return True

    def reset(self):
        if os.path.exists(self.path):
            os.remove(self.path)

def main():
    for platform in ['win64']:
        f = WinNightlyDownloader(platform)

        if f.fetch() and f.check():
            print('installing...')
            os.system(f.path + ' -ms')
            print(f.path)

if __name__ == '__main__':
    main()