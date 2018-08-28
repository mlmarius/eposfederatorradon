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

# for query_name, query_data in QUERIES.items():
#     for nfo_id, nfo_data in query_data.get('nfos').items():
#         serviceindex.add(
#             serviceindex.WebservicePointer(
#                 nfo_id=nfo_id,
#                 geometry=geometry.Polygon(nfo_data['geometry']),
#                 service_id=ID,
#                 url=nfo_data['url'],
#                 handler=federator
#             )
#         )


# # install webservice pointers made available by this plugin
# serviceindex.add(
#     serviceindex.WebservicePointer(
#         nfo_id='NIEP',
#         geometry=geometry.Polygon([(19.50, 49.00), (30.00, 49.00), (30.00, 42.0), (19.50, 42.0), (19.50, 49.00)]),
#         service_id=ID,
#         url="https://radon.infp.ro/",
#         schema=federator.RequestSchema,
#         response_type='application/json'
#     )
# )
# serviceindex.add(
#     serviceindex.WebservicePointer(
#         nfo_id='INGV',
#         geometry=geometry.Polygon([(11.78, 43.95), (13.61, 43.95), (13.61, 42.8), (11.78, 42.8), (11.78, 43.95)]),
#         service_id=ID,
#         url="http://webservices.ingv.it/ingvws/nfo_taboo/radon/1/query",
#         schema=federator.RequestSchema,
#         response_type='application/json'
#     )
# )
