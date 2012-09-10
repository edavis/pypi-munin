from setuptools import setup

setup(
    name = "pypi-munin",
    version = "0.1",
    author = "Eric Davis",
    author_email = "ed@npri.org",
    url = "https://github.com/edavis/pypi-munin",
    py_modules = ["pypi"],
    entry_points = {
        "console_scripts": [
            "pypi=pypi:main",
        ],
    }
)
