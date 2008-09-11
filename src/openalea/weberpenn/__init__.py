# Redirect path
import os
import vplants.weberpenn

__path__ = vplants.weberpenn.__path__ + __path__[:]

from vplants.weberpenn.__init__ import *
