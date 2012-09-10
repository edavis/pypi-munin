import re
import os
import sys
import xmlrpclib

PYPI_CACHE = "/var/lib/munin/plugin-state/pypi"
PYPI_USERNAME = os.environ.get("PYPI_USERNAME")
SHOW_PAST_VERSIONS = os.environ.get("SHOW_PAST_VERSIONS", False)

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
    Return the total number of downloads for a given release.

    Some packages upload multiple package types (e.g., sdists, eggs,
    zips, etc).  This sums them all together.

    Note: The packages must be hosted on PyPI for this to do anything.
    If you've just registered the package but keep the actual package
    archives elsewhere, this will return an empty list.
    """
    return sum(info['downloads'] for info in client.release_urls(package, release))

def cache():
    """
    Store the package releases and their download counts in a tab-delimited file.
    """
    def clean(s):
        # http://munin-monitoring.org/wiki/notes_on_datasource_names
        s = re.sub('^[^A-Za-z_]', '_', s)
        return re.sub('[^A-Za-z0-9_]', '_', s)

    with open(PYPI_CACHE, 'w') as fp:
        for (package, release) in get_package_releases():
            name = clean("%s_%s" % (package, release))
            downloads = get_release_downloads(package, release)
            fp.write("%s\t%d\n" % (name, downloads))

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
    for (name, downloads) in get_package_stats():
        c.append("%(name)s.label %(name)s" % {"name": name})
    sys.stdout.write("\n".join(c) + '\n')

def execute():
    ret = []
    for (name, downloads) in get_package_stats():
        ret.append("%s.value %d" % (name, downloads))
    sys.stdout.write("\n".join(ret) + '\n')

def main():
    if len(sys.argv) == 1:
        execute()
    else:
        if sys.argv[1] == 'config':
            config()
        elif sys.argv[1] == 'cache':
            cache()
