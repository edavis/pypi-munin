pypi-munin -- Track PyPI download stats with munin
==================================================================

pypi-munin is a [munin](http://munin-monitoring.org/) plugin to track
the download stats of [PyPI](http://pypi.python.org/pypi) packages.

Install/Configure
-----------------

```shell
$ cd ~/src/
$ git clone git://github.com/edavis/munin-pypi && cd munin-pypi/
$ sudo ln -s $(pwd)/pypi_package_downloads.py /etc/munin/plugins/pypi_package_downloads
$ sudo cp pypi_package_downloads.conf /etc/munin/plugin-conf.d/ # make sure to set username
$ sudo cp pypi_package_downloads.cron /etc/cron.d/pypi_package_downloads # set the username here, too
$ sudo /etc/init.d/munin-node restart
```

Test it
-------

```shell
$ telnet localhost 4949
[...]
config pypi_package_downloads
[...]
fetch pypi_package_downloads
[...]
```
