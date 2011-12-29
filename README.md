pypi_package_downloads.py -- Track PyPI download counts with munin
==================================================================

`pypi_package_downloads.py` is a [munin](http://munin-monitoring.org/)
plugin to track the download counts of [PyPI](http://pypi.python.org/pypi) packages.

```shell
$ cd ~/src/
$ git clone git://github.com/edavis/munin-pypi && cd munin-pypi/
$ sudo ln -s $(pwd)/pypi_package_downloads.py /etc/munin/plugins/pypi_package_downloads
$ sudo cp pypi_package_downloads.conf /etc/munin/plugin-conf.d/ # make sure to set username
$ sudo cp pypi_package_downloads.cron /etc/cron.d/pypi_package_downloads # set the username here, too
$ sudo /etc/init.d/munin-node restart
$ # test it
$ munin-run --debug pypi_package_downloads
$ munin-run --debug pypi_package_downloads config
$ telnet localhost 4949
fetch pypi_package_downloads
config pypi_package_downloads
$ # that's all, folks!
```
