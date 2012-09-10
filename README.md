pypi-munin -- Track PyPI download stats with munin
==================================================

pypi-munin is a [munin](http://munin-monitoring.org/) plugin to track
the download stats of [PyPI](http://pypi.python.org/pypi) packages.

Installation
------------

### System-wide

```shell
$ sudo pip install pypi-munin
$ sudo ln -s /usr/local/bin/pypi /etc/munin/plugins/pypi

### Virtualenv

```shell
$ virtualenv --distribute ~/pypi-munin && cd ~/pypi-munin
$ ./bin/pip install pypi-munin
$ sudo ln -s $(pwd)/bin/pypi /etc/munin/plugins/pypi
```

Configuration
-------------

Put:

    [pypi]
    env.PYPI_USERNAME your_pypi_username

into `/etc/munin/plugin-conf.d/pypi.conf`.

If the PYPI_USERNAME environment variable is not set the plugin will
not run.

Once done, run `sudo restart munin-node`.

Test it
-------

```shell
$ sudo munin-run pypi config
$ sudo munin-run pypi
```
