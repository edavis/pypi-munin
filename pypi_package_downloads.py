#!/usr/bin/env python

import re
import os
import xmlrpclib

PYPI_CACHE = os.environ.get("PYPI_CACHE", "/var/run/munin/pypi_package_downloads_cache.txt")

client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')

def packages(username):
    """
    Return a generator of packages attributed to your PyPI account.
    """
    for (attr, package) in client.user_packages(username):
        yield package

def releases(package):
    """
    Return a generator of all releases for a given package.
    """
    for release in client.package_releases(package, True):
        yield release

def downloads(package, release):
    """
    Return either download_count, or a tuple of (packagetype, download_count)

    Note: The packages must be hosted on PyPI for this to do anything.
    If you've just registered the package but keep the actual package
    archives elsewhere, this will return an empty list.
    """
    resp = client.release_urls(package, release)
    if len(resp) == 1:
        return resp[0]['downloads']
    else:
        ret = []
        for stat in resp:
            ret.append((stat['packagetype'], stat['downloads']))
        return ret

def generate_package_info():
    username = os.environ.get("PYPI_USERNAME")
    assert username, "Need a username.  Please run with: PYPI_USERNAME=<name> pypi_package_downloads.py"
    for package in packages(username):
        for release in releases(package):
            download_info = downloads(package, release)
            if isinstance(download_info, int):
                yield ("%s-%s" % (package, release), download_info)
            else:
                for (packagetype, download_count) in download_info:
                    yield ("%s-%s (%s)" % (package, release, packagetype), download_count)

def config():
    c = []
    c.append("graph_title PyPI Package Downloads")
    c.append("graph_vlabel Number of Downloads")
    for (name, downloads) in read_from_cache():
        c.append("%(name)s.label %(name)s" % {"name": name})
    return "\n".join(c)

def cache():
    def clean(s):
        return re.sub('[^A-Za-z0-9_]', '_', s)

    with open(PYPI_CACHE, 'w') as fp:
        for (name, downloads) in generate_package_info():
            fp.write("%s\t%s\n" % (clean(name), downloads))
    return fp

def read_from_cache():
    if not os.path.isfile(PYPI_CACHE):
        cache()

    with open(PYPI_CACHE) as fp:
        for line in fp:
            line = line.strip()
            (name, downloads) = line.split('\t')
            yield (name, int(downloads))

def execute():
    ret = []
    for (name, downloads) in read_from_cache():
        ret.append("%s.value %d" % (name, downloads))
    return "\n".join(ret)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print execute()
    else:
        if sys.argv[1] == 'config':
            print config()
        elif sys.argv[1] == 'cache':
            cache()
    sys.exit(0)
