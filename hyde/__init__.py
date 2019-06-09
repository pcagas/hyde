"""Hyde: The Gkyl Web-UX Package

Hyde (or HiGkyl) is a web user-interface package for Gkeyll 2.0 code.

License: 
    We follow a open-source but closed development model. Release
    zip-balls will be provided, but access to the source-code
    repository is restricted to those who need to modify the code. In
    practice, this means researchers at PPPL and our partner
    institutions. That is, those who have jointly funded projects or
    graduate students with us.

    Gkyl, Postgkyl and Hyde are copyrighted 2016-2019 by Ammar Hakim.

.. _documentation:
    http://gkyl.readthedocs.io/en/latest/

"""

__version__ = '1.0'

# import submodules
from . import sim

# import selected classes to the root
from .sim.User import User
