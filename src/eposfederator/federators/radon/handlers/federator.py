import logging
from eposfederator.libs.base.requesthandler import RequestHandler
from eposfederator.libs import downloader, serviceindex
from eposfederator.libs.base.schema import Schema
import tornado.iostream
from marshmallow import fields, validate
from webargs.tornadoparser import use_args
from shapely import geometry
import urllib


logger = logging.getLogger(__name__)


class RequestSchema(Schema):

    class Meta():
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'
        strict = True

    mintime = fields.DateTime(
        required=True,
        metadata={
            "label": "Minimum time"
        },
        description="Start data selection from this UTC datetime"
    )

    maxtime = fields.DateTime(
        required=True,
        metadata={
            "label": "Maximum time"
        },
        description="End data selection at this UTC datetime"
    )

    maxlat = fields.Float(
        validate=validate.Range(max=90, min=-90),
        required=True,
        metadata={
            "label": "Maximum latitude"
        },
        description="Maximum latitude"
    )

    minlat = fields.Float(
        validate=validate.Range(max=90, min=-90),
        required=True,
        metadata={
            "label": "Minimum latitude"
        },
        description="Minimum latitude"
    )

    maxlon = fields.Float(
        validate=validate.Range(max=180, min=-180),
        required=True,
        metadata={
            "label": "Maximum longitude"
        },
        description="Maximum longitude"
    )

    minlon = fields.Float(
        validate=validate.Range(max=180, min=-180),
        required=True,
        metadata={
            "label": "Minimum longitude"
        },
        description="Minimum longitude"
    )

    minperiod = fields.Float(
        required=False,
        metadata={
            "label": 'Minimum "sampling period" allowed to extract data [minutes]'
        }
    )

    maxperiod = fields.Float(
        required=False,
        metadata={
            "label": 'Maximum "sampling period" allowed to extract data [minutes]'
        },
    )

    type_site = fields.String(
        validate=validate.OneOf(["indoor", "shelter", "borehole", "soil"]),
        default="indoor",
        metadata={
            "label": "Nickname of type of installation"
        }
    )

    max_radon_err = fields.Float(
        required=False,
        validate=validate.Range(max=-180, min=180),
        metadata={
            "label": 'maximum % uncertainty of the measure accepted for extraction'
        },
    )

    max_int_delta = fields.Float(
        required=False,
        validate=validate.Range(min=0),
        metadata={
            "label": 'maximum distance in time between internal temperature'
        },
    )


class Handler(RequestHandler):

    ID = 'query'
    DESCRIPTION = 'Federated Radon counts endpoint'
    RESPONSE_TYPE = 'application/json'
    REQUEST_SCHEMA = RequestSchema
    ROUTE = ""

    @use_args(RequestSchema)
    async def get(self, reqargs):

        logger.info('getting radon data ...')

        try:
            # attempt to define the geographic area for this query
            bounds = geometry.Polygon([
                (reqargs['minlon'], reqargs['minlat']), (reqargs['maxlon'], reqargs['minlat']),
                (reqargs['maxlon'], reqargs['maxlat']), (reqargs['minlon'], reqargs['maxlat'])
            ])
        except Exception as e:
            bounds = None

        reqargs['mintime'] = reqargs['mintime'].strftime('%Y-%m-%dT%H:%M:%S.000Z')
        reqargs['maxtime'] = reqargs['maxtime'].strftime('%Y-%m-%dT%H:%M:%S.000Z')

        args = urllib.parse.urlencode(reqargs, safe=':')

        def ffunc(wspointer):
            logger.info(f"filter_func is filtering {wspointer}")
            logger.info(self.__class__)
            return wspointer.handler == self.__class__

        urls = serviceindex.get(geometry=bounds, filter_func=ffunc)
        urls = [f"{url.url}?{args}" for url in urls]

        self.write('{"results": [')

        dlmgr = None
        try:
            # ask a dload manager to perform the downloads for us
            # and store the download errors
            dlmgr = downloader.DownloadManager(*urls)
            async for chunk in dlmgr.fetch():
                self.write(chunk)
                await self.flush()
        except tornado.iostream.StreamClosedError:
            logger.warning("Client left. Aborting download from upstream.")
            return

        if dlmgr is not None and len(dlmgr.errors) > 0:
            self.write('], "errors":[')
            self.write(','.join(err.to_json() for err in dlmgr.errors))

        self.write(']}')

        await self.flush()
