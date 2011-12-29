#!/usr/bin/env python

import re
import os
import sys
import xmlrpclib

PYPI_CACHE = os.environ.get("PYPI_CACHE", "/tmp/pypi_package_downloads_cache.txt")
PYPI_USERNAME = os.environ.get("PYPI_USERNAME")
SHOW_PAST_VERSIONS = os.environ.get("SHOW_PAST_VERSIONS", True)

if not PYPI_USERNAME:
    sys.stdout.write("Need a PYPI_USERNAME environment variable. Aborting.\n")
    sys.exit(1)

client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')

def get_package_releases():
    """
    Return a generator of (package, release) tuples for all packages
    and releases (including old releases if SHOW_PAST_VERSIONS is
    True) belonging to the PYPI_USERNAME environment variable.
    """
    for (attr, package) in client.user_packages(PYPI_USERNAME):
        for release in client.package_releases(package, SHOW_PAST_VERSIONS):
            yield (package, release)

def get_release_downloads(package, release):
    """
    Return either download_count, or a tuple of (packagetype, download_count)

    Note: The packages must be hosted on PyPI for this to do anything.
    If you've just registered the package but keep the actual package
    archives elsewhere, this will return an empty list.
    """
    resp = client.release_urls(package, release)
    if len(resp) == 1:
        return int(resp[0]['downloads'])
    else:
        ret = []
        for stat in resp:
            ret.append((stat['packagetype'], int(stat['downloads'])))
        return ret

def cache():
    """
    Store the package releases and their download counts in a tab-delimited file.
    """
    def clean(s):
        return re.sub('[^A-Za-z0-9_]', '_', s)

    with open(PYPI_CACHE, 'w') as fp:
        for (package, release) in get_package_releases():
            name = clean("%s_%s" % (package, release))
            downloads = get_release_downloads(package, release)
            if isinstance(downloads, int):
                fp.write("%s\t%d\n" % (name, downloads))
            else:
                for (packagetype, download_count) in downloads:
                    fp.write("%s_%s\t%d\n" % (name, clean(packagetype), download_count))

def get_package_stats():
    if not os.path.isfile(PYPI_CACHE):
        cache()

    with open(PYPI_CACHE) as fp:
        for line in fp:
            line = line.strip()
            (name, downloads) = line.split('\t')
            yield (name, int(downloads))

def config():
    c = []
    c.append("graph_title PyPI Package Downloads")
    c.append("graph_vlabel Number of Downloads")
    c.append("graph_printf %d")
    for (name, downloads) in get_package_stats():
        c.append("%(name)s.label %(name)s" % {"name": name})
    sys.stdout.write("\n".join(c) + '\n')

def execute():
    ret = []
    for (name, downloads) in get_package_stats():
        ret.append("%s.value %d" % (name, downloads))
    sys.stdout.write("\n".join(ret) + '\n')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        execute()
    else:
        if sys.argv[1] == 'config':
            config()
        elif sys.argv[1] == 'cache':
            cache()
