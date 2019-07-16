import io
import re
from setuptools import setup, find_packages

with io.open("hyde/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \'(.*?)\'", f.read()).group(1)

setup(
    name="hyde",
    version=version,
    packages=['hyde', 'hyde.lib']
)