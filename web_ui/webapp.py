import logging
import pathlib
import time

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette.templating import Jinja2Templates


html_templates = Jinja2Templates(directory=pathlib.Path(__file__).parent.joinpath('templates').absolute())


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        start_time = time.time()

        response: Response = await call_next(request)

        wall_timing = time.time() - start_time
        client_ip = request.client.host
        endpoint = request.get('endpoint')
        endpoint_name = 'unknown'
        if endpoint:
            endpoint_name = endpoint.__name__

        path = request.get('path')
        method = request.get('method')
        status_code = response.status_code

        logging.info(f'request_stats: {endpoint_name=} {method=} {path=} {wall_timing=} {client_ip=} {status_code=}')
        return response


async def index_html(request):
    logging.info('index page request')

    return html_templates.TemplateResponse('index.html', {
        'request': request,
    })


routes = [
    Route('/', index_html, methods=['GET'], name='homepage'),
]

middleware = [
    Middleware(RequestLogMiddleware),
]


app = Starlette(debug=False, routes=routes, middleware=middleware)

app_log = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)s %(levelname)s %(name)s %(message)s')  # noqa: WPS323
app_log.setFormatter(formatter)

logger = logging.getLogger()
logger.handlers = []
logger.addHandler(app_log)
logger.setLevel(logging.INFO)

__all__ = ['app']
