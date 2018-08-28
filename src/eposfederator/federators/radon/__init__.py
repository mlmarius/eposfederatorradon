from eposfederator.libs import serviceindex
from shapely import geometry
from eposfederator.libs import appbuilder
import logging

NAME = 'Radon Federator'
ID = 'radon'
DESCRIPTION = "Federates Radon requests across compliant NFOs"
BASE_ROUTE = '/radon'

# collect all handlers from this plugin's 'handlers' module
HANDLERS = list(appbuilder.collect_handlers(f"{__name__}.handlers"))
